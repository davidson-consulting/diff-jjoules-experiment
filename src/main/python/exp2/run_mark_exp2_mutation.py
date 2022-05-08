import sys

import os
from os import listdir

SCRIPT_DIR = os.path.abspath('./src/main/python/utils/')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils.cmd.json_cmd import *
from utils.cmd.git_cmd import *
from utils.cmd.io_cmd import *
from utils.cmd.mvn_cmd import *
from utils.utils import *
from utils.constants import *
from utils.args.run_exp1_args import *

import clone

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()

    commits = read_file_by_lines(args.input + '/' + args.project + '/' + COMMITS_FILE_PATH)
    module = read_file(args.input + '/' + args.project + '/' + MODULE_FILE_PATH)
    base_output_path = args.output + '/' + args.project + '/'

    dynamic_module = module == '--dynamic'

    must_use_date_format = args.date_format

    if not args.no_clone:
        clone.remove_and_clone_both(commits[0])

    begin = args.begin if args.begin != -1 else 1 
    end = args.end if args.end != -1 else len(commits) - 1
    print(begin, end)
    
    files_to_copy = [
       'consideredTestMethods.json',
       'decision'
    ]
    
    selected_methods_to_mutate = read_json(args.input + '/' + project + '/selected_methods_to_mutate.json')
    mutation_intensities = read_json(args.input + '/' + project + '/mutation_intensities.json')
    mutation_intensities = [str(int(mutation_intensities[key])) for key in ['min', 'max']]
    
    for mutation_intensity in mutation_intensities:
        for class_name in selected_methods_to_mutate:
            for method_name in selected_methods_to_mutate[class_name]:

                exp2_output_path = base_output_path + '/exp2/' + str(mutation_intensity) + '_' + class_name + '_' + method_name + '/'
                  
                deltas_json_path = '/'.join([exp2_output_path, 'diff-jjoules', 'deltas.json'])
                data_v1_json_path = '/'.join([exp2_output_path, 'diff-jjoules', 'data_v1.json'])
                data_v2_json_path = '/'.join([exp2_output_path, 'diff-jjoules', 'data_v2.json'])
                
                if dynamic_module:
                    module = find_most_impacted_module(PATH_V1 + '/', PATH_V2 + '/')
        
                if dynamic_module and len(module) == 0:
                    print('skipping', current, 'module', 'is', 'empty')
                    continue
                
                path_module_v1 = PATH_V1 + '/' + module + '/'
                path_module_v2 = PATH_V2 + '/' + module + '/'
                    
                delete_module_info_java(path_module_v1)
                delete_module_info_java(path_module_v2)
                
                mvn_install_skip_test_build_classpath(path_module_v1, must_use_date_format)
                mvn_install_skip_test_build_classpath(path_module_v2, must_use_date_format)
                
                 # MUTATION
                current_selected_methods_to_mutate = {}
                current_selected_methods_to_mutate[class_name] = [method_name]
                write_json(path_module_v2 +  '/selected_methods_to_mutate.json', current_selected_methods_to_mutate)

                mvn_diff_jjoules_mutate(path_module_v2, 'selected_methods_to_mutate.json', mutation_intensity)            
                git_commit(path_module_v2)
                
                mvn_install_skip_test_build_classpath(path_module_v1, must_use_date_format)
                mvn_install_skip_test_build_classpath(path_module_v2, must_use_date_format)

                mvn_diff_jjoules_mark(
                    PATH_V1,
                    path_module_v1,
                    PATH_V2,
                    path_module_v2,
                    path_module_v1 + 'logs',
                    deltas_json_path,
                    data_v1_json_path,
                    data_v2_json_path,
                    'ALL',
                    'CODE_COVERAGE',
                    '0.8'
                )
                
                copy(
                    '/'.join([path_module_v1, 'diff-jjoules', 'coverage_v1.json']),
                    '/'.join([path_module_v1, 'coverage_v1.json'])
                )
                
                copy(
                    '/'.join([path_module_v1, 'diff-jjoules', 'coverage_v2.json']),
                    '/'.join([path_module_v1, 'coverage_v2.json'])
                )
                
                exp2_output_path = base_output_path + '/exp2/' +  str(i) + '_' + reduce_sha(commit_v1) + '_' + reduce_sha(commit_v2) + '/'
                delete_dir_and_mkdir(exp2_output_path)
                
                for test_filter in TEST_FILTERS:
                    for mark_strategy in MARK_STRATEGIES:
                        inner_loop_values = COHEN_S_DS if test_filter == 'STUDENTS_T_TEST' else ['0.8']
                        for cohen_s_d in inner_loop_values:
                            current_output_path = exp2_output_path + '_'.join([test_filter, mark_strategy]) + ('_' + cohen_s_d if test_filter == 'STUDENTS_T_TEST' else '')
                            delete_dir_and_mkdir(current_output_path)
                            mvn_diff_jjoules_mark(
                                PATH_V1,
                                path_module_v1,
                                PATH_V2,
                                path_module_v2,
                                path_module_v1 + 'logs',
                                deltas_json_path,
                                data_v1_json_path,
                                data_v2_json_path,
                                test_filter,
                                mark_strategy,
                                cohen_s_d,
                                '/'.join([path_module_v1, 'coverage_v1.json']),
                                '/'.join([path_module_v1, 'coverage_v2.json'])
                            )
                            for file in files_to_copy:
                                copy(
                                    '/'.join([path_module_v1, 'diff-jjoules', file]),
                                    '/'.join([current_output_path, file])
                                )
                            delete_directory(path_module_v1 + 'diff-jjoules')
                
                input()