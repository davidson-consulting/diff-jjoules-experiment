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
    commits_folders = commits_folders
    for i in range(len(commits_folders)):
        if not commits_folders[i].startswith('3_'):
            continue
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
        run_mvn_locate_and_analyze_jjoules(PATH_V1, PATH_V2, path_to_current_data_folder, path_to_data_v1, path_to_data_v2)