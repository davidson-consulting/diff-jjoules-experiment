
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

def get_methods_name_from_category(category_key, category_selected_methods_to_mutate):
    full_qualified_method_names = []
    for test_class in category_selected_methods_to_mutate:
        for test_method in category_selected_methods_to_mutate[test_class]:
            if category_selected_methods_to_mutate[test_class][test_method] == category_key:
                full_qualified_method_names.append(test_class + '_' + test_method)
    return full_qualified_method_names

def get_numbers_for_real(root_output_path, test_filter, cohen_s_d, mark_strategy):
    nb_passing, nb_breaking, nb_non_applicable = 0, 0, 0
    for project in PROJECTS:
        root_output_path_project ='/'.join([root_output_path, project])
        path_folder_result_commits = listdir(root_output_path_project + '/exp2')
        path_folder_result_commits = [commit_folder for commit_folder in path_folder_result_commits if not commit_folder.split('_')[0] == 'minus']
        path_folder_result_commits.sort(key=lambda commit_folder: int(commit_folder.split('_')[0]))
        nb_done = 0
        for path_folder_result_commit in path_folder_result_commits:
            if not '.' in path_folder_result_commit:
                nb_done = nb_done + 1
                path_folder_result_exp1 = root_output_path_project + '/exp1/' + path_folder_result_commit + '/diff-jjoules'
                path_folder_result_exp2 = root_output_path_project + '/exp2/' + path_folder_result_commit
                path_folder_mark_results = path_folder_result_exp2 + '/' + '_'.join([test_filter, mark_strategy]) + ('' if cohen_s_d == '' else ('_' + cohen_s_d))
                decision = read_file(path_folder_mark_results + '/decision')
                considered_test_methods = read_json(path_folder_mark_results + '/consideredTestMethods.json')
                if len(considered_test_methods) == 0:
                    nb_non_applicable = nb_non_applicable + 1
                elif decision == 'pass':
                    nb_passing = nb_passing + 1
                elif decision == 'break':
                    nb_breaking = nb_breaking + 1
                else:
                    print('ERROR, unrecognized decision', decision, len(current_nb_considered_test_methods))
            if nb_done >= 50:
                break
    return nb_passing, nb_breaking, nb_non_applicable

def build_cell(nb_passing, nb_breaking, nb_non_applicable):
    return  ' '.join([
                '\\begin{tabular}{l}',
                '\\cmark{}', str(nb_passing + nb_non_applicable),
                '('+ str(nb_non_applicable) +')'
                '\\\\',
                '\\xmark{}', str(nb_breaking),
                '/', str(nb_passing + nb_breaking + nb_non_applicable),
                '\\end{tabular}'
            ])

'''
def build_cell(nb_passing, nb_breaking, nb_non_applicable):
    return  ' '.join([
                '\\begin{tabular}{l}',
                '\\xmark{}', str(nb_breaking),
                '\\cmark{}', str(nb_passing),
                '\\\\',
                '--', str(nb_non_applicable),
                '/', str(nb_passing + nb_breaking + nb_non_applicable),
                '\\end{tabular}'
            ])
    
def build_cell_real_test_filter(nb_passing, nb_breaking, nb_non_applicable):
    return  ' '.join([
                '\\begin{tabular}{l}',
                compute_and_format_perc(nb_passing + nb_breaking + nb_non_applicable, nb_breaking + nb_passing),
                '\\\\',
                compute_and_format_perc(nb_passing + nb_breaking + nb_non_applicable, nb_non_applicable),
                '\\end{tabular}'
            ])
    
def build_cell_real_mark(nb_passing, nb_breaking, nb_non_applicable):
    return  ' '.join([
                '\\begin{tabular}{l}',
                compute_and_format_perc(nb_passing + nb_breaking + nb_non_applicable, nb_breaking),
                '\\\\',
                compute_and_format_perc(nb_passing + nb_breaking + nb_non_applicable, nb_passing + nb_non_applicable),
                '\\end{tabular}'
            ])
'''


if __name__ == '__main__':
    
    args = RunArgs().build_parser().parse_args()
    
    projects = PROJECTS
    
    label_per_mark_strategy = {
        'STRICT': 'strict', 
        'AGGREGATE': 'agg',
        'CODE_COVERAGE': 'cocov',
        'DIFF_COVERAGE': 'dicov'
    }
    
    label_per_test_filter = {
        'ALL': 'all',
        'EMPTY_INTERSECTION': '$\\emptyset$ intersection',
        'STUDENTS_T_TEST': 't-test'
    }
    
    keys_mutation_intensities = ['zero', 'max']
    keys_category_methods = ['min', 'med']
    
    nb_passing_strategy_mutation, nb_breaking_strategy_mutation, nb_non_applicable_strategy_mutation = {}, {}, {}
    for mark_strategy in MARK_STRATEGIES:
        nb_passing_strategy_mutation[mark_strategy] = {}
        nb_breaking_strategy_mutation[mark_strategy] = {}
        nb_non_applicable_strategy_mutation[mark_strategy] = {}
        for key_mutation_intensities in ['zero_min', 'zero_med', 'max_min', 'max_med', 'real']:
            nb_passing_strategy_mutation[mark_strategy][key_mutation_intensities] = 0
            nb_breaking_strategy_mutation[mark_strategy][key_mutation_intensities] = 0
            nb_non_applicable_strategy_mutation[mark_strategy][key_mutation_intensities] = 0
            
    nb_passing_filter_mutation, nb_breaking_filter_mutation, nb_non_applicable_filter_mutation = {}, {}, {}
    for test_filter in TEST_FILTERS:
        inner_loop_values = COHEN_S_DS if test_filter == 'STUDENTS_T_TEST' else ['']
        for cohen_s_d in inner_loop_values:
            config = label_per_test_filter[test_filter] + ' ' + cohen_s_d
            nb_passing_filter_mutation[config] = {}
            nb_breaking_filter_mutation[config] = {}
            nb_non_applicable_filter_mutation[config] = {}
            for key_mutation_intensities in ['zero_min', 'zero_med', 'max_min', 'max_med', 'real']:
                nb_passing_filter_mutation[config][key_mutation_intensities] = 0
                nb_breaking_filter_mutation[config][key_mutation_intensities] = 0
                nb_non_applicable_filter_mutation[config][key_mutation_intensities] = 0
    
    for test_filter in TEST_FILTERS:
        inner_loop_values = COHEN_S_DS if test_filter == 'STUDENTS_T_TEST' else ['']
        for cohen_s_d in inner_loop_values:
            config = label_per_test_filter[test_filter] + ' ' + cohen_s_d
            print(to_row_latex([config, '', '', '', '', '']))
            for mark_strategy in MARK_STRATEGIES:
                current_row = [label_per_mark_strategy[mark_strategy]]
                total_nb_passing, total_nb_breaking, total_nb_non_applicable = 0, 0, 0
                for key_mutation_intensities in keys_mutation_intensities:
                    for key_category_methods in keys_category_methods:
                        nb_passing, nb_breaking, nb_non_applicable = 0, 0, 0
                        for project in projects:
                            selected_methods_to_mutate = read_json(args.input + '/' + project + '/selected_methods_to_mutate.json')
                            category_selected_methods_to_mutate = read_json(args.input + '/' + project + '/category_selected_methods.json')
                            mutation_intensities = read_json(args.input + '/' + project + '/mutation_intensities.json')
                            mutation_intensity = mutation_intensities[key_mutation_intensities]
                            full_qualified_method_names = get_methods_name_from_category(key_category_methods, category_selected_methods_to_mutate)
                            for full_qualified_method_name in full_qualified_method_names:
                                if project == 'xwiki':
                                    path_to_mutated_class_results = '/'.join([
                                        args.output, 
                                        project, 
                                        'exp2', 
                                        '_'.join([str(int(mutation_intensity)), '_'.join(full_qualified_method_name.split('_')[1:])])
                                    ]).replace('//', '/')
                                else:
                                    path_to_mutated_class_results = '/'.join([
                                        args.output, 
                                        project, 
                                        'exp2', 
                                        '_'.join([str(int(mutation_intensity)), full_qualified_method_name])
                                    ]).replace('//', '/')
                                path_folder_mark_results = path_to_mutated_class_results + '/' + '_'.join([test_filter, mark_strategy]) + ('' if cohen_s_d == '' else ('_' + cohen_s_d))
                                decision = read_file(path_folder_mark_results + '/decision')
                                current_nb_considered_test_methods = read_json(path_folder_mark_results + '/consideredTestMethods.json')
                                if len(current_nb_considered_test_methods) == 0:
                                    nb_non_applicable = nb_non_applicable + 1
                                    total_nb_non_applicable = total_nb_non_applicable + 1
                                    nb_non_applicable_filter_mutation[config][key_mutation_intensities + '_' + key_category_methods] = nb_non_applicable_filter_mutation[config][key_mutation_intensities + '_' + key_category_methods] + 1
                                    nb_non_applicable_strategy_mutation[mark_strategy][key_mutation_intensities + '_' + key_category_methods] = nb_non_applicable_strategy_mutation[mark_strategy][key_mutation_intensities + '_' + key_category_methods] + 1
                                elif decision == 'pass':
                                    nb_passing = nb_passing + 1
                                    total_nb_passing = total_nb_passing + 1
                                    nb_passing_filter_mutation[config][key_mutation_intensities + '_' + key_category_methods] = nb_passing_filter_mutation[config][key_mutation_intensities + '_' + key_category_methods] + 1
                                    nb_passing_strategy_mutation[mark_strategy][key_mutation_intensities + '_' + key_category_methods] = nb_passing_strategy_mutation[mark_strategy][key_mutation_intensities + '_' + key_category_methods] + 1
                                elif decision == 'break':
                                    nb_breaking = nb_breaking + 1
                                    total_nb_breaking = total_nb_breaking + 1
                                    nb_breaking_filter_mutation[config][key_mutation_intensities + '_' + key_category_methods] = nb_breaking_filter_mutation[config][key_mutation_intensities + '_' + key_category_methods] + 1
                                    nb_breaking_strategy_mutation[mark_strategy][key_mutation_intensities + '_' + key_category_methods] = nb_breaking_strategy_mutation[mark_strategy][key_mutation_intensities + '_' + key_category_methods] + 1
                                else:
                                    print('ERROR, unrecognized decision', decision, len(current_nb_considered_test_methods))
                        current_row.append(build_cell(nb_passing, nb_breaking, nb_non_applicable))
                #current_row.append(build_cell(total_nb_passing, total_nb_breaking, total_nb_non_applicable))
                nb_passing, nb_breaking, nb_non_applicable = get_numbers_for_real(args.output, test_filter, cohen_s_d, mark_strategy)
                current_row.append(build_cell(nb_passing, nb_breaking, nb_non_applicable))
                #current_row.append(build_cell_real_mark(nb_passing, nb_breaking, nb_non_applicable))
                nb_passing_filter_mutation[config]['real'] = nb_passing_filter_mutation[config]['real'] + nb_passing
                nb_breaking_filter_mutation[config]['real'] = nb_breaking_filter_mutation[config]['real'] + nb_breaking
                nb_non_applicable_filter_mutation[config]['real'] = nb_non_applicable_filter_mutation[config]['real'] + nb_non_applicable
                nb_passing_strategy_mutation[mark_strategy]['real'] = nb_passing_strategy_mutation[mark_strategy]['real'] + nb_passing
                nb_breaking_strategy_mutation[mark_strategy]['real'] = nb_breaking_strategy_mutation[mark_strategy]['real'] + nb_breaking
                nb_non_applicable_strategy_mutation[mark_strategy]['real'] = nb_non_applicable_strategy_mutation[mark_strategy]['real'] + nb_non_applicable
                print(to_row_latex(current_row))
            print('\\midrule')
    '''            
    print('\\midrule')
    for mark_strategy in MARK_STRATEGIES:
        current_row = [' '.join([ '\\begin{tabular}{l}', 'total', '\\\\', label_per_mark_strategy[mark_strategy], '\\end{tabular}'])]
        total_mark_strategy_nb_passing, total_mark_strategy_nb_breaking, total_mark_strategy_nb_non_applicable = 0, 0, 0
        for key_mutation_intensities in keys_mutation_intensities:
            for key_category_methods in keys_category_methods:
                current_row.append(
                    build_cell(
                        nb_passing_strategy_mutation[mark_strategy][key_mutation_intensities + '_' + key_category_methods],
                        nb_breaking_strategy_mutation[mark_strategy][key_mutation_intensities + '_' + key_category_methods],
                        nb_non_applicable_strategy_mutation[mark_strategy][key_mutation_intensities + '_' + key_category_methods]
                    )
                )
                if not key_mutation_intensities == 'zero':
                    total_mark_strategy_nb_passing = total_mark_strategy_nb_passing + nb_passing_strategy_mutation[mark_strategy][key_mutation_intensities + '_' + key_category_methods]
                    total_mark_strategy_nb_breaking = total_mark_strategy_nb_breaking + nb_breaking_strategy_mutation[mark_strategy][key_mutation_intensities + '_' + key_category_methods]
                    total_mark_strategy_nb_non_applicable = total_mark_strategy_nb_non_applicable + nb_non_applicable_strategy_mutation[mark_strategy][key_mutation_intensities + '_' + key_category_methods]
        current_row.append(
            build_cell(total_mark_strategy_nb_passing, total_mark_strategy_nb_breaking, total_mark_strategy_nb_non_applicable)
        )        
        current_row.append(
            build_cell(
                nb_passing_strategy_mutation[mark_strategy]['real'],
                nb_breaking_strategy_mutation[mark_strategy]['real'],
                nb_non_applicable_strategy_mutation[mark_strategy]['real']
            )
        )
        current_row.append(
            build_cell_real_mark(
                nb_passing_strategy_mutation[mark_strategy]['real'],
                nb_breaking_strategy_mutation[mark_strategy]['real'],
                nb_non_applicable_strategy_mutation[mark_strategy]['real']
            )
        )
        print(to_row_latex(current_row))
    print('\\midrule')
    print('\\midrule')
    for test_filter in TEST_FILTERS:
        inner_loop_values = COHEN_S_DS if test_filter == 'STUDENTS_T_TEST' else ['']
        for cohen_s_d in inner_loop_values:
            config = label_per_test_filter[test_filter] + ' ' + cohen_s_d
            current_row = [' '.join([ '\\begin{tabular}{l}', 'total', '\\\\', config, '\\end{tabular}'])]
            total_test_filter_nb_passing, total_test_filter_nb_breaking, total_test_filter_nb_non_applicable = 0, 0, 0
            for key_mutation_intensities in keys_mutation_intensities:
                for key_category_methods in keys_category_methods:
                    current_row.append(build_cell(
                        nb_passing_filter_mutation[config][key_mutation_intensities + '_' + key_category_methods], 
                        nb_breaking_filter_mutation[config][key_mutation_intensities + '_' + key_category_methods], 
                        nb_non_applicable_filter_mutation[config][key_mutation_intensities + '_' + key_category_methods]
                    ))
                    if not key_mutation_intensities == 'zero':
                        total_test_filter_nb_passing = total_test_filter_nb_passing + nb_passing_filter_mutation[config][key_mutation_intensities + '_' + key_category_methods]
                        total_test_filter_nb_breaking = total_test_filter_nb_breaking + nb_breaking_filter_mutation[config][key_mutation_intensities + '_' + key_category_methods]
                        total_test_filter_nb_non_applicable = total_test_filter_nb_non_applicable + nb_non_applicable_filter_mutation[config][key_mutation_intensities + '_' + key_category_methods]
            current_row.append(build_cell(total_test_filter_nb_passing, total_test_filter_nb_breaking, total_test_filter_nb_non_applicable))
            current_row.append(build_cell(
                nb_passing_filter_mutation[config]['real'],
                nb_breaking_filter_mutation[config]['real'],
                nb_non_applicable_filter_mutation[config]['real']
            ))
            current_row.append(build_cell_real_test_filter(
                nb_passing_filter_mutation[config]['real'],
                nb_breaking_filter_mutation[config]['real'],
                nb_non_applicable_filter_mutation[config]['real']
            ))
            print(to_row_latex(current_row))
    '''
    
            
    
                    
                                