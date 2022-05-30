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
    
    mvn_install_skip_test_build_classpath(PATH_V1, must_use_date_format)
    mvn_install_skip_test_build_classpath(PATH_V2, must_use_date_format)
    
    selected_methods_to_mutate = read_json(args.input + '/' + project + '/selected_methods_to_mutate.json')
    mutation_intensities = read_json(args.input + '/' + project + '/mutation_intensities.json')
    mutation_intensities = [str(int(mutation_intensities[key])) for key in ['zero', 'min', 'med', 'max']]
    
    for mutation_intensity in mutation_intensities:
        for module_class_name in selected_methods_to_mutate:
            split_module_class_name = module_class_name.split('_')
            module = split_module_class_name[0]
            class_name = split_module_class_name[1]
            for method_name in selected_methods_to_mutate[module_class_name]:
                
                output_path = base_output_path + '/exp2/' + str(mutation_intensity) + '_' + class_name + '_' + method_name + '/'
                delete_dir_and_mkdir(output_path)
                
                git_reset_hard_folder(PATH_V1, commits[49])
                git_reset_hard_folder(PATH_V2, commits[49])

                path_module_v1 = module
                path_module_v2 = module.replace('v1', 'v2')

                delete_module_info_java(path_module_v1)
                delete_module_info_java(path_module_v2)

                mvn_install_skip_test_build_classpath(path_module_v1, must_use_date_format)
                mvn_install_skip_test_build_classpath(path_module_v2, must_use_date_format)
                
                path_mutated_java_file = args.input + '/' + project + '/mutations/exp2/' +  str(mutation_intensity) + '_' + class_name + '_' + method_name
                package_path_name = '/'.join(class_name.split('.')[:-1])
                simple_class_name = class_name.split('.')[-1]
                path_dst_mutated_java_file = path_module_v2 + '/src/main/java/' + package_path_name + '/' + simple_class_name + '.java'
                print('copy', path_mutated_java_file, 'to', path_dst_mutated_java_file)
                copy(
                    path_mutated_java_file,
                    path_dst_mutated_java_file
                )
                
                copy(
                    path_mutated_java_file + '_pom.xml',
                    path_module_v2 + '/pom.xml'
                )
                git_commit(path_module_v2)
                
                mvn_install_skip_test_build_classpath(path_module_v1, must_use_date_format)
                mvn_install_skip_test_build_classpath(path_module_v2, must_use_date_format)

                mvn_diff_jjoules_no_mark(
                    PATH_V1,
                    path_module_v1,
                    PATH_V2,
                    path_module_v2,
                    path_module_v1 + '/logs',
                    must_use_date_format
                )
                
                for file in FILES_TO_COPY:
                    copy(
                        path_module_v1 + '/' + file,
                        output_path + file
                    )
                    delete_file(path_module_v1 + '/' + file)
                
                for dir in DIRECTORIES_TO_COPY:
                    copy_directory(
                        path_module_v1 + '/' + dir,
                        output_path + dir
                    )
                    delete_directory(path_module_v1 + '/' + dir)
