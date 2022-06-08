import sys

import os
from os import listdir

SCRIPT_DIR = os.path.abspath('./src/main/python/utils/')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils.cmd.git_cmd import *
from utils.cmd.io_cmd import *
from utils.cmd.mvn_cmd import *
from utils.constants import *
from utils.cmd.json_cmd import *
from utils.args.run_exp2_args import *

import clone

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()

    commits = read_file_by_lines(args.input + '/' + args.project + '/' + COMMITS_FILE_PATH)
    module = read_file(args.input + '/' + args.project + '/' + MODULE_FILE_PATH)
    base_output_path = args.output + '/' + args.project + '/'
    project = args.project

    must_use_date_format = args.date_format

    if not args.no_clone:
        clone.remove_and_clone_both(commits[0])
    
    delete_directory(PATH_V1 + '_running')
    delete_directory(PATH_V2 + '_running')
    
    copy_directory(PATH_V1, PATH_V1 + '_running')
    copy_directory(PATH_V2, PATH_V2 + '_running')
    
    PATH_V1 = PATH_V1 + '_running'
    PATH_V2 = PATH_V2 + '_running'
    
    path_to_mutated_classes = args.input + '/' + project + '/mutations/exp2/'
    mutated_class_files = listdir(path_to_mutated_classes)
    for mutated_class_file in mutated_class_files:
        if mutated_class_file.startswith('minus_'):
            
            split = mutated_class_file.split('_')
            class_name = split[1]
            method_name = split[2]
            mutator = split[3] if len(split) > 3 else ''
            
            output_path = base_output_path + '/exp2/minus_' + class_name + '_' + method_name + ('_' + split[3] if len(split) > 3 else '') + '/'
            delete_dir_and_mkdir(output_path)
            
            git_reset_hard_folder(PATH_V1, commits[2])
            git_reset_hard_folder(PATH_V2, commits[2])
            
            path_module_v1 = PATH_V1 + '/' + module + '/'
            path_module_v2 = PATH_V2 + '/' + module + '/'

            mvn_install_skip_test_build_classpath(path_module_v1, must_use_date_format)
            mvn_install_skip_test_build_classpath(path_module_v2, must_use_date_format)
            
            path_mutated_class_file = path_to_mutated_classes + '/' + mutated_class_file
            package_path_name = '/'.join(class_name.split('.')[:-1])
            simple_class_name = class_name.split('.')[-1]
            path_dst_mutated_java_file = path_module_v2+ '/src/main/java/' + package_path_name + '/' + simple_class_name + '.java'
            print('copy', path_mutated_class_file, 'to', path_dst_mutated_java_file)
            copy(
                path_mutated_class_file,
                path_dst_mutated_java_file
            )
            git_commit(path_module_v2)
            
            delete_module_info_java(path_module_v1)
            delete_module_info_java(path_module_v2)

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
