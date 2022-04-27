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
        'coverage_first.json',
        'coverage_second.json',
        'deltaOmega.json',
        'exec_additions.json',
        'exec_deletions.json',
        'omega.json',
        'Omega.json',
        'theta.json'
    ]
    
    properly_ended = []
    
    for i in range(begin, end):#len(commits) - 1):
        
        if len(properly_ended) == 100:
            break
        
        commit_v1 = commits[i+1]
        commit_v2 = commits[i]

        current = str(i) + '_' + reduce_sha(commit_v1) + '_' + reduce_sha(commit_v2)
        print('trying', current)
        
        output_path = base_output_path + '/exp1/' +  str(i) + '_' + reduce_sha(commit_v1) + '_' + reduce_sha(commit_v2) + '/' 

        diff_jjoules_directory = output_path + '/diff-jjoules'
        end_properly = check_if_end_properly(diff_jjoules_directory)
        if not end_properly:
            continue            
        properly_ended.append(current)
        considered_test_method_path = '/'.join([output_path, 'diff-jjoules', 'consideredTestMethods.json'])
        if not isfile('/'.join([output_path, 'diff-jjoules', 'consideredTestMethods.json'])):
            print('skipping', current)
            continue
        considered_test_method = read_json(considered_test_method_path)
        if len(considered_test_method) == 0:
            print('skipping', current)
            continue

        print('running', current)
        
        deltas_json_path = '/'.join([output_path, 'diff-jjoules', 'deltas.json'])

        git_reset_hard_folder(PATH_V1, commit_v1)
        git_reset_hard_folder(PATH_V2, commit_v2)

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
    
        mvn_diff_jjoules_mark(
            PATH_V1,
            path_module_v1,
            PATH_V2,
            path_module_v2,
            path_module_v1 + 'logs',
            deltas_json_path,
            considered_test_method_path
        )
        for file in files_to_copy:
            copy(
                '/'.join([path_module_v1, 'diff-jjoules', file]),
                '/'.join([output_path, 'diff-jjoules', file])
            )
        delete_directory(path_module_v1 + 'diff-jjoules')
        
        