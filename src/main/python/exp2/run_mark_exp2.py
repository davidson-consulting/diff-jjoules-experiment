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
    
    commits_todo = [
        '254_f89bf37_9464cc7',
        '503_0b5e555_7dc2a2c',
        '504_85df4f2_0b5e555',
        '505_534c59d_85df4f2',
        '2610_0f71877_c0b266b',
        '2617_2559713_5601494',
        '2636_a0b25ca_75dab6d',
        '2637_1b936ca_a0b25ca',
        '2638_a0e8b77_1b936ca',
        '2639_255dbbd_a0e8b77',
        '2784_cb81f0b_69a1e43',
        '2785_6fb3186_cb81f0b',
        '2789_1b79714_ae84cd3',
        '2790_6b19685_1b79714',
        '2794_7b9ed5a_6dc9059',
        '2795_4da5393_7b9ed5a',
        '2799_768b9b3_8f82e34',
        '2803_d051ca5_bd7f18e',
        '2880_cfee272_5f85426',
        '2885_6287cb5_7ee5210',
        '2886_d840365_6287cb5',
        '2887_68c081c_d840365',
        '2895_a564692_528404c',
        '2896_6ffadb2_a564692',
        '2907_d149869_3eb0562',
        '2909_fa9bd11_b2dc094',
        '2910_1aa8e40_fa9bd11',
        '2923_2fe671e_deae845',
        '2927_a306519_641c789'
    ]
    
    properly_ended = []
    
    for i in range(begin, end):#len(commits) - 1):
        
        if len(properly_ended) == 50:
            break
        
        commit_v1 = commits[i+1]
        commit_v2 = commits[i]

        current = str(i) + '_' + reduce_sha(commit_v1) + '_' + reduce_sha(commit_v2)
        
        if not current in commits_todo:
            continue
        
        print('trying', current)
        
        exp1_output_path = base_output_path + '/exp1/' +  str(i) + '_' + reduce_sha(commit_v1) + '_' + reduce_sha(commit_v2) + '/' 

        diff_jjoules_directory = exp1_output_path + '/diff-jjoules'
        end_properly = check_if_end_properly(diff_jjoules_directory)
        if not end_properly:
            continue            
        properly_ended.append(current)
       
        print('running', current)
        
        deltas_json_path = '/'.join([exp1_output_path, 'diff-jjoules', 'deltas.json'])
        data_v1_json_path = '/'.join([exp1_output_path, 'diff-jjoules', 'data_v1.json'])
        data_v2_json_path = '/'.join([exp1_output_path, 'diff-jjoules', 'data_v2.json'])

        git_reset_hard_folder(PATH_V1, commit_v1)
        git_reset_hard_folder(PATH_V2, commit_v2)

        if dynamic_module:
            module = find_most_impacted_module(PATH_V1 + '/', PATH_V2 + '/')
        
        if dynamic_module and len(module) == 0:
            print('skipping', current, 'module', 'is', 'empty')
            continue
        
        path_module_v1 = PATH_V1 + '/' + module + '/'
        path_module_v2 = PATH_V2 + '/' + module + '/'
        
        '''    
        delete_module_info_java(path_module_v1)
        delete_module_info_java(path_module_v2)
        '''

        mvn_install_skip_test_build_classpath(PATH_V1, must_use_date_format)
        mvn_install_skip_test_build_classpath(PATH_V2, must_use_date_format)

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
        #delete_dir_and_mkdir(exp2_output_path)
        
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