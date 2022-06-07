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
from utils.args.build_table_exp2_args import *
from utils.utils import *
from utils.statitics import *
from utils.cmd.latex_cmd import *
from utils.cmd.graph_cmd import *

import re

def get_methods_name_from_category(category_key, category_selected_methods_to_mutate):
    full_qualified_method_names = []
    for test_class in category_selected_methods_to_mutate:
        for test_method in category_selected_methods_to_mutate[test_class]:
            if category_selected_methods_to_mutate[test_class][test_method] == category_key:
                full_qualified_method_names.append(test_class + '_' + test_method)
    return full_qualified_method_names
                
def get_nb_test_in_json(data_json):
    nb_test = 0
    for test_class in data_json:
        nb_test = nb_test + len(data_json[test_class])
    return nb_test

def get_nb_test_in_csv(data_csv):
    nb_test = 0
    for line in data_csv:
        nb_test = nb_test + len(line.split(';')[1:])
    return nb_test

def get_nb_break_over_nb_commit_per_config(path_folder_results):
    errors_exp1 = []
    path_folder_results_exp1 = path_folder_results + '/exp1/'
    path_folder_results_exp2 = path_folder_results + '/exp2/'
    nb_break_per_config = {}
    nb_pass_per_config = {}
    nb_selected_methods_per_test_filter = {}
    nb_considered_methods_per_test_filter = {}
    for test_filter in TEST_FILTERS:
        inner_loop_values = COHEN_S_DS if test_filter == 'STUDENTS_T_TEST' else ['']
        for cohen_s_d in inner_loop_values:
            need_figure_test_filter = True
            for mark_strategy in MARK_STRATEGIES:
                config = test_filter + '-' + cohen_s_d + '-' + mark_strategy
                nb_break_per_config[config] = 0
                nb_pass_per_config[config] = 0
                results_exp2 = listdir(path_folder_results_exp2)
                results_exp2.sort(key=lambda commit_folder: int(commit_folder.split('_')[0]))
                nb_done = 0
                for result_exp2 in results_exp2:
                    if not '.' in result_exp2:
                        nb_done = nb_done + 1
                        base_path_result_exp2 = path_folder_results_exp2 + '/' + result_exp2
                        path_folder_mark_results = base_path_result_exp2 + '/' + '_'.join([test_filter, mark_strategy]) + ('' if cohen_s_d == '' else ('_' + cohen_s_d))
                        if not isfile(path_folder_mark_results + '/decision'):
                            errors_exp1.append('\t'.join([path_folder_results, test_filter, cohen_s_d, mark_strategy, result_exp2]))
                            continue
                        decision = read_file(path_folder_mark_results + '/decision')
                        if decision == 'break':
                            nb_break_per_config[config] = nb_break_per_config[config] + 1
                        else:
                            nb_pass_per_config[config] = nb_pass_per_config[config] + 1
                        path_folder_diff_jjoules_results = path_folder_results_exp1 + '/' + result_exp2 + '/diff-jjoules'
                        if isfile(path_folder_diff_jjoules_results + '/selected_tests.json'):
                            nb_selected_test_methods = get_nb_test_in_json(read_json(path_folder_diff_jjoules_results + '/selected_tests.json'))
                        else:
                            nb_selected_test_methods = get_nb_test_in_csv(read_file_by_lines(path_folder_diff_jjoules_results + '/testsThatExecuteTheChange.csv'))
                        nb_considered_test_methods = get_nb_test_in_json(read_json(path_folder_mark_results + '/consideredTestMethods.json'))
                        test_filter_key = test_filter + ('' if cohen_s_d == '' else ('_' + cohen_s_d))
                        if test_filter_key in nb_selected_methods_per_test_filter:
                            nb_selected_methods_per_test_filter[test_filter_key] = nb_selected_methods_per_test_filter[test_filter_key] + nb_selected_test_methods
                            nb_considered_methods_per_test_filter[test_filter_key] = nb_considered_methods_per_test_filter[test_filter_key] + nb_considered_test_methods    
                        else:
                            nb_selected_methods_per_test_filter[test_filter_key] = nb_considered_test_methods
                            nb_considered_methods_per_test_filter[test_filter_key] = nb_considered_test_methods
                        if nb_done == 50:
                            break
    
    return nb_break_per_config, nb_pass_per_config, nb_selected_methods_per_test_filter, nb_considered_methods_per_test_filter, errors_exp1

if __name__ == '__main__':
    
    args = RunArgs().build_parser().parse_args()
    
    projects = PROJECTS
    projects = ['xwiki']
    
    label_per_test_filter = {
        'ALL': 'all',
        'EMPTY_INTERSECTION': '$\\emptyset\cap$',
        'STUDENTS_T_TEST': 't-test'
    }
    
    label_per_mark_strategy = {
        'STRICT': 'strict', 
        'AGGREGATE': 'agg',
        'CODE_COVERAGE': 'cocov',
        'DIFF_COVERAGE': 'dicov'
    }

    errors_mutations = []
    errors_exp1 = []
    
    print(
        to_header_latex([
            'Config',
            'Zero',
            'Min',
            'Med',
            'Max',
            'Real'
        ])
    )

    for project in projects:
        nb_break_per_config, nb_pass_per_config, nb_selected_methods_per_test_filter, nb_considered_methods_per_test_filter, error = get_nb_break_over_nb_commit_per_config(args.output + '/' + project)
        errors_exp1 = errors_exp1 + error
        selected_methods_to_mutate = read_json(args.input + '/' + project + '/selected_methods_to_mutate.json')
        category_selected_methods_to_mutate = read_json(args.input + '/' + project + '/category_selected_methods.json')
        mutation_intensities = read_json(args.input + '/' + project + '/mutation_intensities.json')
        keys_mutation_intensities = ['zero', 'min', 'med', 'max']
        keys_category_methods = ['min', 'med']
        print(to_row_latex([project, 20*'']))
        for test_filter in TEST_FILTERS:
            inner_loop_values = COHEN_S_DS if test_filter == 'STUDENTS_T_TEST' else ['']
            for cohen_s_d in inner_loop_values:
                row_test_filter = [label_per_test_filter[test_filter] + ' ' + cohen_s_d]
                mark_lines = []
                row_test_filter_printed = False
                for mark_strategy in MARK_STRATEGIES:
                    mark_line = [label_per_mark_strategy[mark_strategy]]
                    for key_mutation_intensities in keys_mutation_intensities:
                        mutation_intensity = mutation_intensities[key_mutation_intensities]
                        mark_mutation_cell = ''
                        current_nb_considered_test_methods = 0
                        current_nb_selected_test_methods = 0
                        for key_category_methods in keys_category_methods:
                            full_qualified_method_names = get_methods_name_from_category(key_category_methods, category_selected_methods_to_mutate)
                            for raw_full_qualified_method_name in full_qualified_method_names:
                                full_qualified_method_name = '_'.join(raw_full_qualified_method_name.split('/')[-1].split('_')[1:])
                                path_to_mutated_class_results = '/'.join([
                                    args.output, 
                                    project, 
                                    'exp2', 
                                    '_'.join([str(int(mutation_intensity)), full_qualified_method_name])
                                ]).replace('//', '/')
                                path_folder_diff_jjoules_results = path_to_mutated_class_results + '/diff-jjoules'
                                path_folder_mark_results = path_to_mutated_class_results + '/' + '_'.join([test_filter, mark_strategy]) + ('' if cohen_s_d == '' else ('_' + cohen_s_d))
                                if not isfile(path_folder_diff_jjoules_results + '/selected_tests.json'):
                                    errors_mutations.append('\t'.join([project, test_filter, cohen_s_d, mark_strategy, str(int(mutation_intensity)), full_qualified_method_name]))
                                    continue
                                nb_selected_test_methods = get_nb_test_in_json(read_json(path_folder_diff_jjoules_results + '/selected_tests.json'))
                                current_nb_selected_test_methods = current_nb_selected_test_methods + nb_selected_test_methods
                                if not isfile(path_folder_mark_results + '/consideredTestMethods.json') or not isfile(path_folder_mark_results + '/decision'):
                                    errors_mutations.append('\t'.join([project, test_filter, cohen_s_d, mark_strategy, str(int(mutation_intensity)), full_qualified_method_name]))
                                    continue
                                nb_considered_test_methods = get_nb_test_in_json(read_json(path_folder_mark_results + '/consideredTestMethods.json'))
                                current_nb_considered_test_methods = current_nb_considered_test_methods + nb_considered_test_methods
                                decision = read_file(path_folder_mark_results + '/decision')
                                emoji_decision = '\\cmark{}' if decision == 'pass' else '\\xmark{}'
                                if nb_considered_test_methods == 0:
                                    emoji_decision = '\\textemdash{}'
                                mark_mutation_cell = mark_mutation_cell + emoji_decision
                        mark_line.append(mark_mutation_cell)
                        if not row_test_filter_printed:
                            row_test_filter.append(str(current_nb_considered_test_methods) + '/' + str(current_nb_selected_test_methods))
                    row_test_filter_printed = True
                    config = test_filter + '-' + cohen_s_d + '-' + mark_strategy
                    mark_line.append(
                        str(nb_break_per_config[config]) + '\\xmark{} / ' + str(nb_break_per_config[config] + nb_pass_per_config[config])
                    )
                    mark_lines.append(mark_line)
                nb_selected_test_methods = nb_selected_methods_per_test_filter[test_filter + ('' if cohen_s_d == '' else ('_' + cohen_s_d))]
                nb_considered_test_methods = nb_considered_methods_per_test_filter[test_filter + ('' if cohen_s_d == '' else ('_' + cohen_s_d))]
                row_test_filter.append(str(nb_considered_test_methods) + '/' + str(nb_selected_test_methods))
                print(to_row_latex(row_test_filter))
                print('\\midrule')
                for mark_line in mark_lines:
                    print(to_row_latex(mark_line))
            print('\\midrule')
    print(to_footer_latex())

    print('error mutations')
    for error in errors_mutations:
        print(error)
        
    print('error exp1')
    for error in errors_exp1:
        print(error)
                                