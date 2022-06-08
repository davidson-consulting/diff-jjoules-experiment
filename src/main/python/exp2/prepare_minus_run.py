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
from utils.args.run_exp2_args import *
from utils.utils import *
from utils.statitics import *

import clone

def get_max_indices(sorted_survived_mutations):
    max_cursor = int(0.10 * len(sorted_survived_mutations))
    return [max_cursor - 2, max_cursor - 1, max_cursor, max_cursor + 1, max_cursor + 2]

def get_min_indices(sorted_survived_mutations):
    min_cursor = int(0.90 * len(sorted_survived_mutations)) - 1
    
    return [min_cursor - 2, min_cursor - 1, min_cursor, min_cursor + 1, min_cursor + 2]

def get_average_indices(sorted_survived_mutations):
    if len(sorted_survived_mutations) < 5:
        print('not enough data', len(sorted_survived_mutations))
        return list(range(0, len(sorted_survived_mutations)))
    middle_cursor = int(len(sorted_survived_mutations) / 2)
    return [middle_cursor - 2, middle_cursor - 1, middle_cursor, middle_cursor + 1, middle_cursor + 2]

def filter_method_name(method_name):
    discarded_method_names = ['equals', 'tostring', 'hashcode', 'pop', 'peek', 'poll', 'add', 'push', 'put', 'size', 'containskey', 'contains', 'clear']
    return not '<' in method_name and \
        not method_name[0].isupper() and \
        not method_name.startswith('is') and \
        not method_name.startswith('has') and \
        not method_name.startswith('get') and \
        not method_name.startswith('set') and \
        not method_name.lower() in discarded_method_names

def select_methods_to_mutate(path_module_v1, input_path):
    pit_report = read_json(input_path + '/mutations/exp2/pit-reports/mutations.json')
    survived_mutations = []
    for mutation in pit_report['mutations']:
        if mutation['detected'] == False and not mutation['status'] == 'NO_COVERAGE' and filter_method_name(mutation['method']['name']):
            survived_mutations.append(mutation)
    sorted_survived_mutations = sorted(survived_mutations, key=lambda mutation: int(mutation['tests']['run']), reverse=True)
    selected_methods_to_mutate = {}
    selected_methods_to_mutate['med'] = []
    for index in get_average_indices(sorted_survived_mutations):
        print(index)
        selected_methods_to_mutate['med'].append(sorted_survived_mutations[index])
    selected_methods_to_mutate['min'] = []
    for index in get_min_indices(sorted_survived_mutations):
        print(index)
        selected_methods_to_mutate['min'].append(sorted_survived_mutations[index])
    write_json(input_path + '/minus_selected_methods_to_mutate.json', selected_methods_to_mutate)

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()

    commits = read_file_by_lines(args.input + '/' + args.project + '/' + COMMITS_FILE_PATH)
    module = read_file(args.input + '/' + args.project + '/' + MODULE_FILE_PATH)
    module = ''
    base_output_path = args.output + '/' + args.project + '/'

    must_use_date_format = args.date_format

    if not args.no_clone:
        clone.remove_and_clone_both(commits[0])

    git_reset_hard_folder(PATH_V1, commits[1])
    path_module_v1 = PATH_V1 + '/' + module + '/'
    delete_module_info_java(path_module_v1)

    select_methods_to_mutate(path_module_v1, args.input + '/' + args.project)