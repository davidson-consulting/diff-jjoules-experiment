import sys
from utils.cmd_utils import *
from utils.run_for_project_args import *
import csv
import datetime
import time

PREFIX_TMP = '/tmp/'
FOLDER_PATH_V1 = 'v1'
FOLDER_PATH_V2 = 'v2'
PATH_V1 = PREFIX_TMP + FOLDER_PATH_V1
PATH_V2 = PREFIX_TMP + FOLDER_PATH_V2

def get_tests_to_execute():
    path = PATH_V1 + '/' + VALUE_TEST_LISTS
    tests_to_execute = {}
    with open(path, 'r') as csvfile:
        file = csv.reader(csvfile, delimiter=';')
        for line in file:
            tests_to_execute[line[0]] = line[1:]
    return tests_to_execute

def run_tests(nb_iteration, output_path, tests_to_execute):
    mkdir(output_path + '/v1/')
    mkdir(output_path + '/v2/')
    for i in range(nb_iteration):
        print(i)
        v1_result_folder = output_path + '/v1/' + str(i)
        delete_directory(v1_result_folder)
        run_mvn_test(PATH_V1, tests_to_execute, v1_result_folder + '/mvn_test.log', True)
        copy_jjoules_result(PATH_V1, v1_result_folder)

        v2_result_folder = output_path + '/v2/' + str(i)
        delete_directory(v2_result_folder)
        run_mvn_test(PATH_V2, tests_to_execute, v2_result_folder + '/mvn_test.log', True)
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
        mkdir(current_output_path)
    except FileExistsError:
        print('pass...')
    try:
        mkdir(current_err_output_path)
    except FileExistsError:
        print('pass...')
    return current_output_path, current_err_output_path, current_output_path_log, current_output_path_time

def run(nb_iteration, output_path, output_path_log):
    code = run_mvn_clean_test(PATH_V1)
    if not code == 0:
        print_to_file('mvn test did not succeed on v1', output_path_log)
        return -1
    code = run_mvn_clean_test(PATH_V2)
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

    copy(PATH_V1 + '/' + VALUE_TEST_LISTS, output_path + '/' + VALUE_TEST_LISTS)
    tests_to_execute = get_tests_to_execute()
    if len(tests_to_execute) == 0:
        print_to_file('No test could be selected', output_path_log)
        return -1

    run_mvn_clean_test(PATH_V2)
    start_time = time.time()
    code = run_mvn_build_classpath_and_instrument(PATH_V1, PATH_V2, output_path + '/mvn_cp_instr.log')
    elasped_time = time.time() - start_time
    print_to_file(elasped_time, output_path + '/time_injection')

    if not code == 0:
        print_to_file('Error(s) while instrumenting tests with diff-jjoules', output_path_log)
        return -1

    run_tests(nb_iteration, output_path, tests_to_execute)

    return 0

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()

    project_name = args.project_name
    output_path = args.output
    commits_file_path = args.commits + '/' + project_name + '/input'
    nb_iteration = int(args.iteration)
    nb_commits = int(args.nb_commits)

    commits, repo_url = init_commits(commits_file_path)
    init_repositories(repo_url[:-1])
    create_if_does_not_exist(output_path + project_name)

    current_nb_completed_commits = 0
    cursor_commits = 1

    success_output_path = output_path + '/' + project_name + '/'
    error_output_path = output_path + '/' + project_name + '_error/'

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
        else:
            move_directory(current_output_path, current_err_output_path)
        cursor_commits = cursor_commits + 1
