
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
    path_folder_result_commits = listdir(root_output_path + '/exp2')
    path_folder_result_commits.sort(key=lambda commit_folder: int(commit_folder.split('_')[0]))
    nb_done = 0
    for path_folder_result_commit in path_folder_result_commits:
        if not '.' in path_folder_result_commit:
            nb_done = nb_done + 1
            path_folder_result_exp1 = root_output_path + '/exp1/' + path_folder_result_commit + '/diff-jjoules'
            path_folder_result_exp2 = root_output_path + '/exp2/' + path_folder_result_commit
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
    
    print(
        to_header_latex([
            '', '', '', '', '', '', ''
        ])
    )
    
    selected_test_filter = 'STUDENTS_T_TEST'
    cohen_s_d = '0.20'
    
    keys_mutation_intensities = ['zero', 'min', 'med', 'max']
    keys_category_methods = ['min', 'med']
    
    nb_passing_per_mutation_per_strategy, nb_breaking_per_mutation_per_strategy, nb_non_applicable_per_mutation_per_strategy = {}, {}, {}
    for mark_strategy in MARK_STRATEGIES:
        nb_passing_per_mutation_per_strategy[mark_strategy] = {}
        nb_breaking_per_mutation_per_strategy[mark_strategy] = {}
        nb_non_applicable_per_mutation_per_strategy[mark_strategy] = {}
        for key_mutation_intensities in keys_mutation_intensities:
            nb_passing_per_mutation_per_strategy[mark_strategy][key_mutation_intensities] = 0
            nb_breaking_per_mutation_per_strategy[mark_strategy][key_mutation_intensities] = 0
            nb_non_applicable_per_mutation_per_strategy[mark_strategy][key_mutation_intensities] = 0

        nb_passing_per_mutation_per_strategy[mark_strategy]['total'] = 0
        nb_breaking_per_mutation_per_strategy[mark_strategy]['total'] = 0
        nb_non_applicable_per_mutation_per_strategy[mark_strategy]['total'] = 0
        nb_passing_per_mutation_per_strategy[mark_strategy]['real'] = 0
        nb_breaking_per_mutation_per_strategy[mark_strategy]['real'] = 0
        nb_non_applicable_per_mutation_per_strategy[mark_strategy]['real'] = 0
    
    for project in projects:
        selected_methods_to_mutate = read_json(args.input + '/' + project + '/selected_methods_to_mutate.json')
        category_selected_methods_to_mutate = read_json(args.input + '/' + project + '/category_selected_methods.json')
        mutation_intensities = read_json(args.input + '/' + project + '/mutation_intensities.json')
        print(to_row_latex([project, '', '', '', '', '', '']))
        for mark_strategy in MARK_STRATEGIES:
            current_row = [label_per_mark_strategy[mark_strategy]]
            nb_passing, nb_breaking, nb_non_applicable = 0, 0, 0
            for key_mutation_intensities in keys_mutation_intensities:
                nb_passing_per_mutation, nb_breaking_per_mutation, nb_non_applicable_per_mutation = 0, 0, 0
                mutation_intensity = mutation_intensities[key_mutation_intensities]
                cell_methods = ['\\begin{tabular}{r}']
                for key_category_methods in keys_category_methods:
                    full_qualified_method_names = get_methods_name_from_category(key_category_methods, category_selected_methods_to_mutate)
                    for full_qualified_method_name in full_qualified_method_names:
                        path_to_mutated_class_results = '/'.join([
                            args.output, 
                            project, 
                            'exp2', 
                            '_'.join([str(int(mutation_intensity)), full_qualified_method_name])
                        ]).replace('//', '/')
                        path_folder_mark_results = path_to_mutated_class_results + '/' + '_'.join([selected_test_filter, mark_strategy]) + ('' if cohen_s_d == '' else ('_' + cohen_s_d))
                        decision = read_file(path_folder_mark_results + '/decision')
                        current_nb_considered_test_methods = read_json(path_folder_mark_results + '/consideredTestMethods.json')
                        if len(current_nb_considered_test_methods) == 0:
                            cell_methods.append('--')
                            nb_non_applicable = nb_non_applicable + 1
                            nb_non_applicable_per_mutation = nb_non_applicable_per_mutation + 1
                        elif decision == 'pass':
                            cell_methods.append('\\cmark{}')
                            nb_passing = nb_passing + 1
                            nb_passing_per_mutation = nb_passing_per_mutation + 1
                        elif decision == 'break':
                            cell_methods.append('\\xmark{}')
                            nb_breaking = nb_breaking + 1
                            nb_breaking_per_mutation = nb_breaking_per_mutation + 1
                        else:
                            print('ERROR, unrecognized decision', decision, len(current_nb_considered_test_methods))
                    cell_methods.append('\\\\')
                cell_methods.append('\\end{tabular}')
                current_row.append(' '.join(cell_methods))
                nb_passing_per_mutation_per_strategy[mark_strategy][key_mutation_intensities] = nb_passing_per_mutation_per_strategy[mark_strategy][key_mutation_intensities] + nb_passing_per_mutation
                nb_breaking_per_mutation_per_strategy[mark_strategy][key_mutation_intensities] = nb_breaking_per_mutation_per_strategy[mark_strategy][key_mutation_intensities] + nb_breaking_per_mutation
                nb_non_applicable_per_mutation_per_strategy[mark_strategy][key_mutation_intensities] = nb_non_applicable_per_mutation_per_strategy[mark_strategy][key_mutation_intensities] + nb_non_applicable_per_mutation
            current_row.append(
                ' '.join([
                    '\\begin{tabular}{l}',
                    '\\xmark{}', str(nb_breaking),
                    '\\cmark{}', str(nb_passing),
                    '\\\\',
                    '--', str(nb_non_applicable),
                    '/', str(nb_passing + nb_breaking + nb_non_applicable),
                    '\\end{tabular}'
                ])
            )
            nb_passing_per_mutation_per_strategy[mark_strategy]['total'] = nb_passing_per_mutation_per_strategy[mark_strategy]['total'] + nb_passing
            nb_breaking_per_mutation_per_strategy[mark_strategy]['total'] = nb_breaking_per_mutation_per_strategy[mark_strategy]['total'] + nb_breaking
            nb_non_applicable_per_mutation_per_strategy[mark_strategy]['total'] = nb_non_applicable_per_mutation_per_strategy[mark_strategy]['total'] + nb_non_applicable
            root_output_path ='/'.join([args.output, project])
            nb_passing_real, nb_breaking_real, nb_non_applicable_real = get_numbers_for_real(root_output_path, selected_test_filter, cohen_s_d, mark_strategy)
            current_row.append(
                ' '.join([
                    '\\begin{tabular}{l}',
                    '\\xmark{}', str(nb_breaking_real),
                    '\\cmark{}', str(nb_passing_real),
                    '\\\\',
                    '--', str(nb_non_applicable_real),
                    '/', str(nb_passing_real + nb_breaking_real + nb_non_applicable_real),
                    '\\end{tabular}'
                ])
            )
            nb_passing_per_mutation_per_strategy[mark_strategy]['real'] = nb_passing_per_mutation_per_strategy[mark_strategy]['real'] + nb_passing_real
            nb_breaking_per_mutation_per_strategy[mark_strategy]['real'] = nb_breaking_per_mutation_per_strategy[mark_strategy]['real'] + nb_breaking_real
            nb_non_applicable_per_mutation_per_strategy[mark_strategy]['real'] = nb_non_applicable_per_mutation_per_strategy[mark_strategy]['real'] + nb_non_applicable_real
            print(to_row_latex(current_row))
        print('\\midrule')
    print('\\midrule')
    print(to_row_latex(['total', '', '', '', '', '', '']))
    for mark_strategy in MARK_STRATEGIES:
        current_row = [label_per_mark_strategy[mark_strategy]]
        for key_mutation_intensities in keys_mutation_intensities:
            current_row.append(
                ' '.join([
                    '\\begin{tabular}{l}',
                    '\\xmark{}', str(nb_breaking_per_mutation_per_strategy[mark_strategy][key_mutation_intensities]),
                    '\\cmark{}', str(nb_passing_per_mutation_per_strategy[mark_strategy][key_mutation_intensities]),
                    '\\\\',
                    '--', str(nb_non_applicable_per_mutation_per_strategy[mark_strategy][key_mutation_intensities]),
                    '/', str(nb_passing_per_mutation_per_strategy[mark_strategy][key_mutation_intensities] + nb_breaking_per_mutation_per_strategy[mark_strategy][key_mutation_intensities] + nb_non_applicable_per_mutation_per_strategy[mark_strategy][key_mutation_intensities]),
                    '\\end{tabular}'
                ])
            )
        current_row.append(
                ' '.join([
                    '\\begin{tabular}{l}',
                    '\\xmark{}', str(nb_breaking_per_mutation_per_strategy[mark_strategy]['total']),
                    '\\cmark{}', str(nb_passing_per_mutation_per_strategy[mark_strategy]['total']),
                    '\\\\',
                    '--', str(nb_non_applicable_per_mutation_per_strategy[mark_strategy]['total']),
                    '/', str(nb_passing_per_mutation_per_strategy[mark_strategy]['total'] + nb_breaking_per_mutation_per_strategy[mark_strategy]['total'] + nb_non_applicable_per_mutation_per_strategy[mark_strategy]['total']),
                    '\\end{tabular}'
                ])
            )
        current_row.append(
                ' '.join([
                    '\\begin{tabular}{l}',
                    '\\xmark{}', str(nb_breaking_per_mutation_per_strategy[mark_strategy]['real']),
                    '\\cmark{}', str(nb_passing_per_mutation_per_strategy[mark_strategy]['real']),
                    '\\\\',
                    '--', str(nb_non_applicable_per_mutation_per_strategy[mark_strategy]['real']),
                    '/', str(nb_passing_per_mutation_per_strategy[mark_strategy]['real'] + nb_breaking_per_mutation_per_strategy[mark_strategy]['real'] + nb_non_applicable_per_mutation_per_strategy[mark_strategy]['real']),
                    '\\end{tabular}'
                ])
            )
        print(to_row_latex(current_row))
    print(to_footer_latex())