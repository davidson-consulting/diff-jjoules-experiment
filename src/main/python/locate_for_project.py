import sys
from utils.json_utils import *
from utils.cmd_utils import *
from utils.locate_args import *
import csv
import datetime
import time
import os

PATH_V1 = '/tmp/v1'
PATH_V2 = '/tmp/v2'

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

def select_test_to_locate(path_json_v1, path_json_v2):
    data_v1 = read_json(path_json_v1)
    data_v2 = read_json(path_json_v2)

    delta_per_test = {}
    delta_acc = 0
    for test in data_v1:
        if test in data_v2:
            current_delta = data_v2[test]['energy'] - data_v1[test]['energy']
            delta_acc = delta_acc + current_delta
            delta_per_test[test] = current_delta

    selected_test = {}
    for test in delta_per_test:
        print(test, delta_per_test[test], delta_acc, (delta_per_test[test] / delta_acc) * 100)
        if (delta_per_test[test] / delta_acc) * 100 > 25:
            test_name_splitted = test.split('-')
            if not test_name_splitted[0] in selected_test:
                selected_test[test_name_splitted[0]] = []
            selected_test[test_name_splitted[0]].append(test_name_splitted[1])
    
    for test in selected_test:
        print(test, selected_test[test])
    return selected_test

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()

    project_name = args.project_name
    data_path = args.data_path
    commits_file_path = args.commit_path + '/' + project_name + '/input'
    path_to_data_project = data_path + '/' + project_name

    commits, repo_url = init_commits(commits_file_path)
    #init_repositories(repo_url[:-1])

    main_module_name = read_module_name(args.commit_path + '/' + project_name)
    PATH_V1 = PATH_V1 + '/' + main_module_name
    PATH_V2 = PATH_V2 + '/' + main_module_name

    #commits_folders = sorted([subfolder for subfolder in os.listdir(path_to_data_project) if not subfolder.endswith('.png') and not subfolder == 'README.md'], key=lambda folder_name: int(folder_name.split('_')[0]))[62:]
    commits_folders = sorted([subfolder for subfolder in os.listdir(path_to_data_project) if not subfolder.endswith('.png') and not subfolder == 'README.md'], key=lambda folder_name: int(folder_name.split('_')[0]))
    commits_folders = [commits_folders[0]]
    for i in range(len(commits_folders)):
        print(i, '/', len(commits_folders), commits_folders[i])

        commit_sha_v1 = commits_folders[i].split('_')[1]
        commit_sha_v2 = commits_folders[i].split('_')[2]
        reset_hard(commit_sha_v1, PATH_V1)
        reset_hard(commit_sha_v2, PATH_V2)

        delete_module_info_java(PATH_V1)
        delete_module_info_java(PATH_V2)
        delete_module_info_java(PATH_V1)
        delete_module_info_java(PATH_V2)

        path_to_current_data_folder = path_to_data_project + '/' + commits_folders[i]
        path_to_data_v1 = path_to_current_data_folder + '/data_v1.json'
        path_to_data_v2 = path_to_current_data_folder + '/data_v2.json'
        '''
        selected_tests = select_test_to_locate(path_to_data_v1, path_to_data_v2)
        formatted_tests = ','.join([test_class_name + '#' + '+'.join(selected_tests[test_class_name]) for test_class_name in selected_tests])
        print(formatted_tests)
        '''
        run_mvn_locate_jjoules(PATH_V1, PATH_V2, path_to_current_data_folder, path_to_data_v1, path_to_data_v2)