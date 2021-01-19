import sys
from utils.cmd_utils import *
from utils.run_for_project_args import *
import csv
import datetime
import time
import os

PREFIX_TMP = '/tmp/'
FOLDER_PATH_V1 = 'v1'
FOLDER_PATH_V2 = 'v2'
ROOT_PATH_V1 = PREFIX_TMP + FOLDER_PATH_V1
ROOT_PATH_V2 = PREFIX_TMP + FOLDER_PATH_V2
PATH_V1 = ROOT_PATH_V1
PATH_V2 = ROOT_PATH_V2

def get_tests_to_execute(output_path):
    path = output_path + '/' + VALUE_TEST_LISTS
    tests_to_execute = []
    with open(path, 'r') as csvfile:
        file = csv.reader(csvfile, delimiter=';')
        for line in file:
            test_class = line[0]
            for test_method in line[1:]:
                tests_to_execute.append(test_class + '_' + test_method)
    return tests_to_execute

def run_tests(nb_iteration, output_path, tests_to_execute):
    mkdir(output_path + '/v1/')
    mkdir(output_path + '/v2/')
    for i in range(nb_iteration):
        print(i)
        v1_result_folder = output_path + '/v1/' + str(i)
        delete_directory(v1_result_folder)
        run_mvn_test_class(PATH_V1, tests_to_execute, v1_result_folder + '/mvn_test.log', True)
        copy_jjoules_result(PATH_V1, v1_result_folder)

        v2_result_folder = output_path + '/v2/' + str(i)
        delete_directory(v2_result_folder)
        run_mvn_test_class(PATH_V2, tests_to_execute, v2_result_folder + '/mvn_test.log', True)
        copy_jjoules_result(PATH_V2, v2_result_folder)

def init_commits(commits_file_path):
    commits = []
    with open(commits_file_path, 'r') as commits_file:
        lines = commits_file.readlines()
        repo_url = lines[0]
        for line in lines[1:]:
            commits.append(line[:-1])
    return commits, repo_url

def init_repositories(repo_url):
    delete_directory(PATH_V1)
    delete_directory(PATH_V2)
    clone(repo_url, PATH_V1)
    clone(repo_url, PATH_V2)

def init_current_paths(commit_sha_v1, commit_sha_v2, cursor_commits, success_output_path, error_output_path):
    current_output_path = success_output_path + '/' + '_'.join([str(cursor_commits), commit_sha_v1[:6], commit_sha_v2[:6]])
    current_err_output_path = error_output_path + '/'
    current_output_path_log = current_output_path + '/log'
    current_output_path_time = current_output_path + '/time'
    try:
        delete_directory(current_output_path)
    except FileExistsError:
        print('pass...')
    try:
        mkdir(current_output_path)
    except FileExistsError:
        print('pass...')
    try:
        mkdir(current_err_output_path)
    except FileExistsError:
        print('pass...')
    return current_output_path, current_err_output_path, current_output_path_log, current_output_path_time


def copy_test_list(output_path):
    for dirName, subdirList, fileList in os.walk(PATH_V1):
        for file in fileList:
            if file == VALUE_TEST_LISTS:
                print('copy', dirName + '/' + VALUE_TEST_LISTS, output_path + '/' + VALUE_TEST_LISTS)
                copy(dirName + '/' + VALUE_TEST_LISTS, output_path + '/' + VALUE_TEST_LISTS)
                return

def delete_java_files(tests_to_execute):
    for test_to_execute in tests_to_execute:
        java_file_path = test_to_execute.replace('.', '/') + '.java'
        full_java_file_path = PATH_V1 + '/src/test/java/' + java_file_path
        delete_file(full_java_file_path)
        full_java_file_path = PATH_V2 + '/src/test/java/' + java_file_path
        delete_file(full_java_file_path)

def run(nb_iteration, output_path, output_path_log):
    code = run_mvn_clean_test(ROOT_PATH_V1 if os.path.isfile(ROOT_PATH_V1 + '/pom.xml') else PATH_V1)
    if not code == 0:
        print_to_file('mvn test did not succeed on v1', output_path_log)
        return -1
    code = run_mvn_clean_test(ROOT_PATH_V2 if os.path.isfile(ROOT_PATH_V2 + '/pom.xml') else PATH_V2)
    if not code == 0:
        print_to_file('mvn test did not succeed on v2', output_path_log)
        return -1

    start_time = time.time()
    code = run_mvn_diff_select(PATH_V1, PATH_V2, output_path + '/mvn_test_selections.log')
    elasped_time = time.time() - start_time
    print_to_file(elasped_time, output_path + '/time_selection')

    if not code == 0:
        print_to_file('Error(s) while selecting tests with diff-test-selection', output_path_log)
        return -1

    copy_test_list(output_path)
    tests_to_execute = get_tests_to_execute(output_path)
    if len(tests_to_execute) == 0:
        print_to_file('No test could be selected', output_path_log)
        return -1

    run_mvn_clean_test_build_cp(PATH_V2)
    start_time = time.time()
    code = run_mvn_build_classpath_and_instrument_class(PATH_V1, PATH_V2, output_path + '/mvn_cp_instr.log')
    elasped_time = time.time() - start_time
    print_to_file(elasped_time, output_path + '/time_injection')

    if not code == 0:
        print_to_file('Error(s) while instrumenting tests with diff-jjoules', output_path_log)
        return -1

    run_tests(nb_iteration, output_path, tests_to_execute)

    delete_java_files(tests_to_execute)

    return 0

def result_dir_exists_or_error_dir_exists(commit_sha_v1, commit_sha_v2, cursor_commits, success_output_path, error_output_path):
    print(success_output_path + '/' + '_'.join([str(cursor_commits), commit_sha_v1[:6], commit_sha_v2[:6]]))
    print(error_output_path + '/' + '_'.join([str(cursor_commits), commit_sha_v1[:6], commit_sha_v2[:6]]))
    return os.path.isdir(success_output_path + '/' + '_'.join([str(cursor_commits), commit_sha_v1[:6], commit_sha_v2[:6]])) or \
            os.path.isdir(error_output_path + '/' + '_'.join([str(cursor_commits), commit_sha_v1[:6], commit_sha_v2[:6]]))

def list_and_get_max(folder):
    commits_folders = sorted([subfolder for subfolder in os.listdir(folder) if not subfolder.endswith('.png') and not subfolder.endswith('.md')], key=lambda folder_name: int(folder_name.split('_')[0]))
    return int(commits_folders[-1].split('_')[0]) + 25

def get_cursor_to_continue(folder_success, folder_error):
    cursor_success = list_and_get_max(folder_success)
    cursor_error = list_and_get_max(folder_error)
    return max(cursor_error, cursor_success)

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()

    project_name = args.project_name
    output_path = args.output
    commits_file_path = args.commits + '/' + project_name + '/input'
    nb_iteration = int(args.iteration)
    nb_commits = int(args.nb_commits)
    mode = args.mode
    main_module_name = read_module_name(args.commits + '/' + project_name).split('\n')[0]
    
    commits, repo_url = init_commits(commits_file_path)
    init_repositories(repo_url[:-1])
    create_if_does_not_exist(output_path + project_name)

    current_nb_completed_commits = 0
    cursor_commits = 1

    success_output_path = output_path + '/' + project_name + '/'
    error_output_path = output_path + '/' + project_name + '_error/'

    if mode == mode.continue_mode:
        cursor_commits = get_cursor_to_continue(success_output_path, error_output_path)
        print('continue at', str(cursor_commits))

    PATH_V1 = PATH_V1 + '/' + main_module_name
    PATH_V2 = PATH_V2 + '/' + main_module_name

    last_cursor_commit = cursor_commits

    while current_nb_completed_commits < nb_commits and cursor_commits < len(commits) - 1:
        commit_sha_v1 = commits[cursor_commits]
        commit_sha_v2 = commits[cursor_commits - 1]

        current_output_path, current_err_output_path, current_output_path_log, current_output_path_time = init_current_paths(
            commit_sha_v1, commit_sha_v2, cursor_commits, success_output_path, error_output_path
        )
        
        print_to_file(str(datetime.datetime.today()).split()[0], current_output_path_log)
        print_to_file(' '.join([
            'Run for', 
            str(project_name), 
            str(commit_sha_v1), 
            str(cursor_commits), 
            str(commit_sha_v2), 
            str(cursor_commits - 1), 
            'output_path', 
            str(output_path)
            ]
        ), current_output_path_log)
        print('Run for', project_name, commit_sha_v1, cursor_commits, commit_sha_v2, cursor_commits - 1, 'output_path', output_path)
        reset_hard(commit_sha_v1, PATH_V1)
        reset_hard(commit_sha_v2, PATH_V2)
        delete_module_info_java(PATH_V1)
        delete_module_info_java(PATH_V2)
        print(cursor_commits, '/', len(commits) - 1)
        print_to_file(str(cursor_commits) + ' / ' + str(len(commits) - 1), current_output_path_log)

        start_time = time.time()
        code = run(nb_iteration, current_output_path, current_output_path_log)
        elasped_time = time.time() - start_time
        print_to_file(elasped_time, current_output_path_time)

        if code == 0:
            current_nb_completed_commits = current_nb_completed_commits + 1
            print_to_file('Success! ' + str(current_nb_completed_commits) + ' / ' + str(nb_commits), current_output_path_log)
            print('Success!', current_nb_completed_commits, '/', nb_commits)
            print('zipping v1 and v2 result folders... and delete them')
            zip_folder(current_output_path + '/v1')
            delete_directory(current_output_path + '/v1')
            zip_folder(current_output_path + '/v2')
            delete_directory(current_output_path + '/v2')
            cursor_commits = cursor_commits + 25
        else:
            move_directory(current_output_path, current_err_output_path)
            cursor_commits = cursor_commits + 1