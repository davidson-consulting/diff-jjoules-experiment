import sys

import os
from os import listdir

SCRIPT_DIR = os.path.abspath('./src/main/python/utils/')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils.cmd.git_cmd import *
from utils.cmd.io_cmd import *
from utils.cmd.mvn_cmd import *
from utils.constants import *
from utils.args.run_exp1_args import *

import clone

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()

    commits = read_file_by_lines(args.input + '/' + args.project + '/' + COMMITS_FILE_PATH)
    module = read_file(args.input + '/' + args.project + '/' + MODULE_FILE_PATH)
    base_output_path = args.output + '/' + args.project + '/'

    must_use_date_format = args.date_format

    if not args.no_clone:
        clone.remove_and_clone_both(commits[0])

    begin = args.begin if args.begin != -1 else 1 
    end = args.end if args.end != -1 else len(commits) - 1
    print(begin, end)

    for i in range(begin, end):#len(commits) - 1):
        
        commit_v1 = commits[i+1]
        commit_v2 = commits[i]

        output_path = base_output_path + str(i) + '_' + reduce_sha(commit_v1) + '_' + reduce_sha(commit_v2) + '/' 
        delete_dir_and_mkdir(output_path)

        git_reset_hard_folder(PATH_V1, commit_v1)
        git_reset_hard_folder(PATH_V2, commit_v2)

        path_module_v1 = PATH_V1 + '/' + module + '/'
        path_module_v2 = PATH_V2 + '/' + module + '/'

        delete_module_info_java(path_module_v1)
        delete_module_info_java(path_module_v2)

        mvn_install_skip_test_build_classpath(path_module_v1, must_use_date_format)
        mvn_install_skip_test_build_classpath(path_module_v2, must_use_date_format)

        mvn_diff_jjoules_no_mark(
            PATH_V1,
            path_module_v1,
            PATH_V2,
            path_module_v2,
            path_module_v1 + 'logs',
            must_use_date_format
        )

        for file in FILES_TO_COPY:
            copy(
                path_module_v1 + file,
                output_path + file
            )
            delete_file(path_module_v1 + file)
        
        for dir in DIRECTORIES_TO_COPY:
            copy_directory(
                path_module_v1 + dir,
                output_path + dir
            )
            delete_directory(path_module_v1 + dir)