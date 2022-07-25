import sys

import os
from os import listdir

SCRIPT_DIR = os.path.abspath('./src/main/python/utils/')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils.cmd.git_cmd import *
from utils.cmd.io_cmd import *
from utils.cmd.mvn_cmd import *
from utils.cmd.json_cmd import *
from utils.constants import *
from utils.args.run_exp3_args import *
from utils.utils import *
from utils.statitics import *

import subprocess

import clone

def count_nb_changed_line_diff(diff):
    nb_changed_line = 0
    lines = diff.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('<') or line.startswith('>'):
            current_nb_changed_line = 0
            while not line.startswith('---') and i < len(lines):
                line = lines[i]
                current_nb_changed_line = current_nb_changed_line + 1
                i = i + 1
            i = i + current_nb_changed_line
            nb_changed_line = nb_changed_line + current_nb_changed_line
        else:
            i = i + 1
    return nb_changed_line
    
def get_decision(path_folder_result_commit, config):
    path_folder_result_commit_mark = path_folder_result_commit + '/' + config
    decision = read_file(path_folder_result_commit_mark + 'decision')
    current_nb_considered_test_methods = read_json(path_folder_result_commit_mark + '/consideredTestMethods.json')
    if len(current_nb_considered_test_methods) == 0:
        return 'non_applicable'
    elif decision == 'pass':
        return 'pass'
    else:
        return 'break'

if __name__ == '__main__':
    
    args = RunArgs().build_parser().parse_args()
    
    commits = read_file_by_lines(args.input + '/' + args.project + '/' + COMMITS_FILE_PATH)
    module = read_file(args.input + '/' + args.project + '/' + MODULE_FILE_PATH)
    base_output_path = args.output + '/' + args.project + '/'
    project = args.project

    dynamic_module = module == '--dynamic'
    must_use_date_format = args.date_format

    if not args.no_clone:
        clone.remove_and_clone_both(commits[0])
        
    project_root_folder = args.output + project + '/exp2/'
    commit_folders = listdir(project_root_folder)
    commit_folders.sort(key=lambda commit_folder: int(commit_folder.split('_')[0]))
    
    test_filter = 'STUDENTS_T_TEST'
    mark_strategy = 'CODE_COVERAGE'
    cohen_s_d = '0.80'
    
    smallest_passing_commit = None
    smallest_breaking_commit = None
    
    passing = []
    breaking = []
    
    for test_filter in ['EMPTY_INTERSECTION', 'STUDENTS_T_TEST']:
    #for test_filter in ['STUDENTS_T_TEST']:
        for mark_strategy in ['AGGREGATE', 'CODE_COVERAGE', 'DIFF_COVERAGE']:
        #for mark_strategy in ['CODE_COVERAGE']:
            inner_loop_values = COHEN_S_DS if test_filter == 'STUDENTS_T_TEST' else ['']
            #inner_loop_values = ['0.80'] if test_filter == 'STUDENTS_T_TEST' else ['']
            for cohen_s_d in inner_loop_values:
                config = '_'.join([test_filter, mark_strategy]) + ('' if cohen_s_d == '' else ('_' + cohen_s_d))
                
                done = 0
                nb_changed_line_per_commit_index = {}
                decision_per_commit_index = {}
                diff_per_commit_index = {}
                sha_v1_per_commit_index = {}
                sha_v2_per_commit_index = {}
                
                for path_folder_result_commit in commit_folders:
                    if not '.' in path_folder_result_commit:
                        splitted_commit_folder = path_folder_result_commit.split('_')
                        commit_index = splitted_commit_folder[0]
                        commit_v1 = splitted_commit_folder[1]
                        commit_v2 = splitted_commit_folder[2]
                        sha_v1_per_commit_index[commit_index] = commit_v1
                        sha_v2_per_commit_index[commit_index] = commit_v2
                        git_reset_hard_folder(PATH_V1, commit_v1)
                        git_reset_hard_folder(PATH_V2, commit_v2)
                        
                        '''
                        if dynamic_module:
                            module = find_most_impacted_module(PATH_V1 + '/', PATH_V2 + '/')
                        
                        if len(module) == 0:
                            print('skipping', current, 'module', 'is', 'empty')
                            continue
                        '''

                        path_diff_v1 = PATH_V1 + '/' + module + '/src'
                        path_diff_v2 = PATH_V2 + '/' + module + '/src'
                        diff = subprocess.Popen('diff -r ' + path_diff_v1 + ' ' + path_diff_v2, stdout=subprocess.PIPE, shell=True).stdout.read().decode('UTF-8')
                        nb_changed_line_per_commit_index[commit_index] = count_nb_changed_line_diff(diff)
                        unified_diff = diff = subprocess.Popen('diff -ru ' + path_diff_v1 + ' ' + path_diff_v2, stdout=subprocess.PIPE, shell=True).stdout.read().decode('UTF-8')
                        unified_diff = unified_diff.replace('/tmp/v1//', '')
                        unified_diff = unified_diff.replace('/tmp/v2//', '')
                        diff_per_commit_index[commit_index] = unified_diff
                        
                        decision_per_commit_index[commit_index] = get_decision(base_output_path + '/exp2/' + path_folder_result_commit, config + '/')

                        done = done + 1
                        if done == 50:
                            break

                sorted_keys_per_nb_changed_lines = sorted(nb_changed_line_per_commit_index, key=lambda index: nb_changed_line_per_commit_index[index])
                selected_commit_passing, selected_commit_breaking = None, None
                for key in sorted_keys_per_nb_changed_lines:
                    if not selected_commit_passing == None and not selected_commit_breaking == None:
                        break
                    if selected_commit_passing == None and decision_per_commit_index[key] == 'pass':
                        print(config, key, nb_changed_line_per_commit_index[key])
                        passing.append((config, key, nb_changed_line_per_commit_index[key]))
                        selected_commit_passing = key
                        continue
                    if selected_commit_breaking == None and decision_per_commit_index[key] == 'break':
                        breaking.append((config, key, nb_changed_line_per_commit_index[key]))
                        selected_commit_breaking = key
                        continue
                selected_commits = {}
                if not selected_commit_passing == None: 
                    selected_commits[selected_commit_passing] = {}
                    selected_commits[selected_commit_passing]['size'] = nb_changed_line_per_commit_index[selected_commit_passing]
                    selected_commits[selected_commit_passing]['decision'] = 'pass'
                    selected_commits[selected_commit_passing]['diff'] = diff_per_commit_index[selected_commit_passing]
                    selected_commits[selected_commit_passing]['sha1'] = sha_v1_per_commit_index[selected_commit_passing]
                    selected_commits[selected_commit_passing]['sha2'] = sha_v2_per_commit_index[selected_commit_passing]
                    if smallest_passing_commit == None or nb_changed_line_per_commit_index[selected_commit_passing] <= smallest_passing_commit['size']:
                        smallest_passing_commit = selected_commits[selected_commit_passing]
                        smallest_passing_commit['config'] = config
                    print(selected_commit_passing, nb_changed_line_per_commit_index[selected_commit_passing], decision_per_commit_index[selected_commit_passing])
                if not selected_commit_breaking == None: 
                    selected_commits[selected_commit_breaking] = {}
                    selected_commits[selected_commit_breaking]['size'] = nb_changed_line_per_commit_index[selected_commit_breaking]
                    selected_commits[selected_commit_breaking]['decision'] = 'break'
                    selected_commits[selected_commit_breaking]['diff'] = diff_per_commit_index[selected_commit_breaking]
                    selected_commits[selected_commit_breaking]['sha1'] = sha_v1_per_commit_index[selected_commit_breaking]
                    selected_commits[selected_commit_breaking]['sha2'] = sha_v2_per_commit_index[selected_commit_breaking]
                    if smallest_breaking_commit == None or nb_changed_line_per_commit_index[selected_commit_breaking] <= smallest_breaking_commit['size']:
                        smallest_breaking_commit = selected_commits[selected_commit_breaking]
                        smallest_breaking_commit['config'] = config
                    print(selected_commit_breaking, nb_changed_line_per_commit_index[selected_commit_breaking], decision_per_commit_index[selected_commit_breaking])
                
                #write_json(args.input + '/' + args.project + '/commit_selection/' +  config +'_selected_commits.json', selected_commits)
                #write_json(args.input + '/' + args.project + '/commit_selection/' +  'selected_commits.json', selected_commits)

    print(smallest_passing_commit)
    print(smallest_breaking_commit)
    
    for p in passing:
        print(p)
        
    for b in breaking:
        print(b)