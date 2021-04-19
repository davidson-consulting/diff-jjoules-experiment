import sys
import datetime
import time

from constants import *
from utils.args.main_args import *
from utils.cmd.git_cmd import *
from utils.cmd.io_cmd import *
from utils.cmd.mvn_cmd import *
from utils.logs.log import *

import clone

def reduce_sha(sha):
    return sha[:5]

def run_tests(path_v1, path_v2, output_path, nb_iteration, tests_to_execute):
    mkdir(output_path + '/v1/')
    mkdir(output_path + '/v2/')
    i = 0
    print(i)
    v1_result_folder = output_path + '/v1/' + str(i)
    delete_directory(v1_result_folder)
    mvn_clean_test(path_v1, tests_to_execute, v1_result_folder + '/mvn_test.log')
    copy_jjoules_result(path_v1, v1_result_folder)

    v2_result_folder = output_path + '/v2/' + str(i)
    delete_directory(v2_result_folder)
    mvn_clean_test(path_v2, tests_to_execute, v2_result_folder + '/mvn_test.log')
    copy_jjoules_result(path_v2, v2_result_folder)
    for i in range(1, nb_iteration):
        print(i)
        v1_result_folder = output_path + '/v1/' + str(i)
        delete_directory(v1_result_folder)
        mvn_test(path_v1, tests_to_execute, v1_result_folder + '/mvn_test.log')
        copy_jjoules_result(path_v1, v1_result_folder)

        v2_result_folder = output_path + '/v2/' + str(i)
        delete_directory(v2_result_folder)
        mvn_test(path_v2, tests_to_execute, v2_result_folder + '/mvn_test.log')
        copy_jjoules_result(path_v2, v2_result_folder)

def run(path_v1, path_v2, output_path, nb_iteration):
    code = mvn_install_skip_test_build_classpath(PATH_V1 if os.path.isfile(PATH_V1 + '/pom.xml') else path_v1)
    if not code == 0:
        log('mvn install failed on v1')
        return -1
    code = mvn_install_skip_test_build_classpath(PATH_V2 if os.path.isfile(PATH_V2 + '/pom.xml') else path_v2)
    if not code == 0:
        log('mvn install failed on v2')
        return -1

    start_time = time.time()
    code = mvn_diff_test_selection(path_v1, path_v2, output_path + '/mvn_diff_test_selection.log')
    if not code == 0:
        log('mvn diff-test-selection failed')
        return -1
    elasped_time = time.time() - start_time
    print_to_file_to_path(elasped_time, output_path + '/time_selection')

    copy_target_file(path_v1, output_path, VALUE_TEST_LISTS)
    tests_to_execute = get_tests_to_execute(output_path + '/' + VALUE_TEST_LISTS)
    if len(tests_to_execute) < 1:
        log('no test could be selected!')
        return -1

    start_time = time.time()
    code = mvn_diff_jjoules_instrument(path_v1, path_v2,  output_path + '/mvn_diff_jjoules_instrument.log')
    if not code == 0:
        log('mvn diff-jjoules-instrument failed')
        return -1
    elasped_time = time.time() - start_time
    print_to_file_to_path(elasped_time, output_path + '/time_instrumentation')

    run_tests(path_v1, path_v2, output_path, nb_iteration, tests_to_execute)
    return 0

if __name__ == '__main__':

    #   commit_sha_v1 = 'd26c8189182fa96691cc8e0d0f312469ee0627bb'
    #   commit_sha_v2 = '364de8061173b4b91f4477a55059f68e765fc3d1'

    args = RunArgs().build_parser().parse_args()
    project = args.project
    input_folder_path = args.input
    output_folder_path = args.output
    iteration = args.iteration
    skip_clone = args.skip_clone

    complete_input_folder_path = '/'.join([input_folder_path, project])
    commits = read_file_by_lines('/'.join([complete_input_folder_path, COMMITS_FILE_PATH]))
    module = read_file('/'.join([complete_input_folder_path, MODULE_FILE_PATH]))
    if not skip_clone:
        clone.remove_and_clone_both(commits[0])

    success_output_path = '/'.join([output_folder_path, project])
    error_output_path = '/'.join([output_folder_path, project + '_error/'])
    
    cursor_commits = 2

    while cursor_commits < len(commits):
        sha_v1 = reduce_sha(commits[cursor_commits])
        sha_v2 = reduce_sha(commits[cursor_commits-1])

        commit_folder = '/' + '_'.join([str(cursor_commits), sha_v1, sha_v2]) + '/'
        success_commit_folder = success_output_path + commit_folder
        error_commit_folder = error_output_path + commit_folder

        set_path_log(success_commit_folder + '/log')

        delete_dir_and_mkdir(success_commit_folder)
        delete_dir_and_mkdir(error_commit_folder)

        git_reset_hard_folder(PATH_V1, sha_v1)
        git_reset_hard_folder(PATH_V2, sha_v2)

        delete_module_info_java(PATH_V1)
        delete_module_info_java(PATH_V2)

        code = run(PATH_V1 + '/' + module, PATH_V2 + '/' + module, success_commit_folder, iteration)
        if code == 0:
            log('Success! ' + str(cursor_commits) + ' / ' + str(len(commits) - 1))
            print('zipping v1 and v2 result folders... and delete them')
            zip_folder(success_commit_folder + '/v1')
            delete_directory(success_commit_folder + '/v1')
            zip_folder(success_commit_folder + '/v2')
            delete_directory(success_commit_folder + '/v2')
        else:
            move_directory(success_commit_folder, error_commit_folder)
        cursor_commits = cursor_commits + 1
        
