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

def get_methods_name_from_category(category_key, category_selected_methods_to_mutate):
    full_qualified_method_names = []
    for test_class in category_selected_methods_to_mutate:
        for test_method in category_selected_methods_to_mutate[test_class]:
            if category_selected_methods_to_mutate[test_class][test_method] == category_key:
                full_qualified_method_names.append(test_class + '_' + test_method)
    return full_qualified_method_names

def get_numbers_for_real(root_output_path, test_filter, cohen_s_d):
    nb_selected_test_methods_real, nb_considered_test_methods_real = 0, 0
    path_folder_result_commits = listdir(root_output_path + '/exp2')
    path_folder_result_commits.sort(key=lambda commit_folder: int(commit_folder.split('_')[0]))
    nb_done = 0
    nb_consider_at_least_one_test_real = 0
    tt_consider_at_least_one_test_real = 0
    for path_folder_result_commit in path_folder_result_commits:
        if not '.' in path_folder_result_commit:
            nb_done = nb_done + 1
            path_folder_result_exp1 = root_output_path + '/exp1/' + path_folder_result_commit + '/diff-jjoules'
            path_folder_result_exp2 = root_output_path + '/exp2/' + path_folder_result_commit
            path_folder_mark_results = path_folder_result_exp2 + '/' + '_'.join([test_filter, 'STRICT']) + ('' if cohen_s_d == '' else ('_' + cohen_s_d))
            if not isfile(path_folder_result_exp1 + '/selected_tests.json'):
                nb_selected_test_methods_real = nb_selected_test_methods_real + get_nb_test_in_csv(read_file_by_lines(path_folder_result_exp1 + '/testsThatExecuteTheChange.csv'))
            else:
                nb_selected_test_methods_real = nb_selected_test_methods_real + get_nb_test_in_json(read_json(path_folder_result_exp1 + '/selected_tests.json'))
            current_nb_considered_test_methods = get_nb_test_in_json(read_json(path_folder_mark_results + '/consideredTestMethods.json'))          
            nb_consider_at_least_one_test_real = nb_consider_at_least_one_test_real + (1 if current_nb_considered_test_methods > 0 else 0)
            tt_consider_at_least_one_test_real = tt_consider_at_least_one_test_real + 1
            nb_considered_test_methods_real = nb_considered_test_methods_real + current_nb_considered_test_methods
        if nb_done >= 50:
            break
    return nb_selected_test_methods_real, (nb_considered_test_methods_real if not test_filter == 'ALL' else nb_selected_test_methods_real), nb_consider_at_least_one_test_real, tt_consider_at_least_one_test_real

def to_tabular_double_cell(value_a, total_a, value_b, total_b):
    return '\\begin{tabular}{rr} ' + str(value_a) + '/' + str(total_a) + ' & ' + str(value_b) + '/' + str(total_b) + ' \\end{tabular}'

if __name__ == '__main__':
    
    args = RunArgs().build_parser().parse_args()
    
    projects = PROJECTS
    projects = [
        'gson',
        'jsoup',
        'commons-io',
        'commons-lang',
        'mustache.java'
    ]
    
    label_per_test_filter = {
        'ALL': 'all',
        'EMPTY_INTERSECTION': '$\\emptyset$ intersection',
        'STUDENTS_T_TEST': 't-test'
    }
    
    print(
        to_header_latex([
            '', '', '', '', '', '', ''
        ])
    )
    
    keys_mutation_intensities = ['zero', 'min', 'med', 'max']
    keys_category_methods = ['min', 'med']
    
    for project in projects:
        selected_methods_to_mutate = read_json(args.input + '/' + project + '/selected_methods_to_mutate.json')
        category_selected_methods_to_mutate = read_json(args.input + '/' + project + '/category_selected_methods.json')
        mutation_intensities = read_json(args.input + '/' + project + '/mutation_intensities.json')
        print(to_row_latex([project, '', '', '', '', '', '', '', '', '', '', '']))
        for test_filter in TEST_FILTERS:
            inner_loop_values = COHEN_S_DS if test_filter == 'STUDENTS_T_TEST' else ['']
            for cohen_s_d in inner_loop_values:
                config = label_per_test_filter[test_filter] + ' ' + cohen_s_d
                current_row = [config]
                mark_strategy = 'STRICT'
                nb_consider_at_least_one_test_for_config = 0
                for key_mutation_intensities in keys_mutation_intensities:
                    mutation_intensity = mutation_intensities[key_mutation_intensities]
                    nb_selected_test_methods = 0
                    nb_consider_at_least_one_test = 0
                    nb_considered_test_methods = 0
                    for key_category_methods in keys_category_methods:
                        full_qualified_method_names = get_methods_name_from_category(key_category_methods, category_selected_methods_to_mutate)
                        for full_qualified_method_name in full_qualified_method_names:
                            path_to_mutated_class_results = '/'.join([
                                args.output, 
                                project, 
                                'exp2', 
                                '_'.join([str(int(mutation_intensity)), full_qualified_method_name])
                            ]).replace('//', '/')
                            path_folder_diff_jjoules_results = path_to_mutated_class_results + '/diff-jjoules'
                            path_folder_mark_results = path_to_mutated_class_results + '/' + '_'.join([test_filter, mark_strategy]) + ('' if cohen_s_d == '' else ('_' + cohen_s_d))
                            current_nb_selected = get_nb_test_in_json(read_json(path_folder_diff_jjoules_results + '/selected_tests.json'))
                            current_nb_considered_test_methods = get_nb_test_in_json(read_json(path_folder_mark_results + '/consideredTestMethods.json'))
                            
                            nb_selected_test_methods = nb_selected_test_methods + current_nb_selected
                            nb_consider_at_least_one_test = nb_consider_at_least_one_test + (1 if current_nb_considered_test_methods > 0 else 0)
                            if not key_mutation_intensities == 'zero' and current_nb_considered_test_methods > 0:
                                nb_consider_at_least_one_test_for_config = nb_consider_at_least_one_test_for_config + 1
                            nb_considered_test_methods = nb_considered_test_methods + current_nb_considered_test_methods
                                
                    nb_considered_test_methods = nb_selected_test_methods if test_filter == 'ALL' else nb_considered_test_methods
                    current_row.append(str(nb_considered_test_methods) + '/' + str(nb_selected_test_methods))
                    current_row.append(str(nb_consider_at_least_one_test) + '/' + str(10))
                    
                current_row.append(str(nb_consider_at_least_one_test_for_config) + '/' + str(30))

                root_output_path ='/'.join([args.output, project])
                nb_selected_test_methods_real, nb_considered_test_methods_real, nb_consider_at_least_one_test_real, tt_consider_at_least_one_test_real = get_numbers_for_real(root_output_path, test_filter, cohen_s_d)
                current_row.append(str(nb_considered_test_methods_real) + '/' + str(nb_selected_test_methods_real))
                current_row.append(str(nb_consider_at_least_one_test_real) + '/' + str(tt_consider_at_least_one_test_real))
                print(to_row_latex(current_row))
        print('\\midrule')
    print('\\midrule')
    mark_strategy = 'STRICT'
    print(to_row_latex(['total', '', '', '', '', '', '', '', '', '', '', '']))
    for test_filter in TEST_FILTERS:
        inner_loop_values = COHEN_S_DS if test_filter == 'STUDENTS_T_TEST' else ['']
        for cohen_s_d in inner_loop_values:
            config = label_per_test_filter[test_filter] + ' ' + cohen_s_d
            current_row = [config]
            
            nb_selected_mutation_intensity_config = 0
            nb_considered_mutation_intensity_config = 0
            nb_consider_at_least_one_test_config = 0
            total_nb_consider_at_least_one_test_config = 0
            
            nb_selected_mutation_intensity_config_real = 0
            nb_considered_mutation_intensity_config_real = 0
            nb_consider_at_least_one_test_config_real = 0
            total_nb_consider_at_least_one_test_config_real = 0
            
            for key_mutation_intensities in keys_mutation_intensities:
                nb_selected_mutation_intensity = 0
                nb_considered_mutation_intensity = 0
                nb_consider_at_least_one_test = 0
                total_nb_consider_at_least_one_test = 0
                for project in projects:
                    selected_methods_to_mutate = read_json(args.input + '/' + project + '/selected_methods_to_mutate.json')
                    category_selected_methods_to_mutate = read_json(args.input + '/' + project + '/category_selected_methods.json')
                    mutation_intensities = read_json(args.input + '/' + project + '/mutation_intensities.json')
                    mutation_intensity = mutation_intensities[key_mutation_intensities]
                    for key_category_methods in keys_category_methods:
                        full_qualified_method_names = get_methods_name_from_category(key_category_methods, category_selected_methods_to_mutate)
                        for full_qualified_method_name in full_qualified_method_names:
                            path_to_mutated_class_results = '/'.join([
                                args.output, 
                                project, 
                                'exp2', 
                                '_'.join([str(int(mutation_intensity)), full_qualified_method_name])
                            ]).replace('//', '/')
                            path_folder_diff_jjoules_results = path_to_mutated_class_results + '/diff-jjoules'
                            path_folder_mark_results = path_to_mutated_class_results + '/' + '_'.join([test_filter, mark_strategy]) + ('' if cohen_s_d == '' else ('_' + cohen_s_d))

                            current_nb_selected = get_nb_test_in_json(read_json(path_folder_diff_jjoules_results + '/selected_tests.json'))
                            current_nb_considered_test_methods = get_nb_test_in_json(read_json(path_folder_mark_results + '/consideredTestMethods.json'))

                            nb_selected_mutation_intensity = nb_selected_mutation_intensity + current_nb_selected
                            nb_considered_mutation_intensity = nb_considered_mutation_intensity + (current_nb_considered_test_methods if not test_filter == 'ALL' else current_nb_selected)
                            nb_consider_at_least_one_test = nb_consider_at_least_one_test + (1 if current_nb_considered_test_methods > 0 else 0)
                            total_nb_consider_at_least_one_test = total_nb_consider_at_least_one_test + 1
                if not key_mutation_intensities == 'zero':                                
                    nb_selected_mutation_intensity_config = nb_selected_mutation_intensity_config + nb_selected_mutation_intensity
                    nb_considered_mutation_intensity_config = nb_considered_mutation_intensity_config + nb_considered_mutation_intensity
                    nb_consider_at_least_one_test_config = nb_consider_at_least_one_test_config + nb_consider_at_least_one_test
                    total_nb_consider_at_least_one_test_config = total_nb_consider_at_least_one_test_config + total_nb_consider_at_least_one_test
                current_row.append(str(nb_considered_mutation_intensity) + '/' + str(nb_selected_mutation_intensity))
                current_row.append(str(nb_consider_at_least_one_test) + '/' + str(total_nb_consider_at_least_one_test))
                
            for project in projects:
                root_output_path ='/'.join([args.output, project])
                nb_selected_test_methods_real, nb_considered_test_methods_real, nb_consider_at_least_one_test_real, tt_consider_at_least_one_test_real = get_numbers_for_real(root_output_path, test_filter, cohen_s_d)
                nb_selected_mutation_intensity_config_real = nb_selected_mutation_intensity_config_real + nb_selected_test_methods_real
                nb_considered_mutation_intensity_config_real = nb_considered_mutation_intensity_config_real + nb_considered_test_methods_real
                nb_consider_at_least_one_test_config_real = nb_consider_at_least_one_test_config_real + nb_consider_at_least_one_test_real
                total_nb_consider_at_least_one_test_config_real = total_nb_consider_at_least_one_test_config_real + tt_consider_at_least_one_test_real
            current_row.append(str(nb_consider_at_least_one_test_config) + '/' + str(total_nb_consider_at_least_one_test_config))
            current_row.append(str(nb_considered_mutation_intensity_config_real) + '/' + str(nb_selected_mutation_intensity_config_real))
            current_row.append(str(nb_consider_at_least_one_test_config_real) + '/' + str(total_nb_consider_at_least_one_test_config_real))
            print(to_row_latex(current_row))
    print('\\bottomrule')