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
from utils.args.build_table_exp1_args import *
from utils.utils import *
from utils.statitics import *
from utils.cmd.latex_cmd import *

import numpy as np
import random

def from_dict_to_array_rm_zero_for_both(data, key1, key2):
    array1, array2 = [], []
    for d in data:
        if d[key1] > 0 and d[key2] > 0:
            array1.append(d[key1])
            array2.append(d[key2])
    return array1, array2

# for now, we check that energy and instructions are correlated
def corrcoef(data):
    energy_array, instr_array = from_dict_to_array_rm_zero_for_both(data, ENERGY_KEY, CYCLES_KEY)
    return np.corrcoef(np.array(energy_array).T, np.array(instr_array).T)

def get_all_test_and_correlated_map(diff_jjoules_directory, all_tests, correlated_map):
    id_commit = get_id_commit_function(diff_jjoules_directory)
    data_V1 = read_json(diff_jjoules_directory + '/' + DATA_V1_JSON_FILE_NAME)
    data_V2 = read_json(diff_jjoules_directory + '/' + DATA_V2_JSON_FILE_NAME)
    for test in data_V1:
        all_tests.append(test)
        correlated_map[str(id_commit) + '_' + test] = corrcoef(data_V1[test])

def get_test_considered(diff_jjoules_directory, considered_tests):
    current_considered_tests = read_json(diff_jjoules_directory + '/' + CONSIDERED_TEST_METHODS_JSON_FILE_NAME)
    for considered_test in current_considered_tests:
        considered_tests.extend([
            considered_test + '#' + test_method for test_method in current_considered_tests[considered_test]
        ])

def add_if_has_a_given_correlation(key, considered_tests, nb_correlation_all, nb_correlation_considered, correlation, correlation_to_reach):
    if abs(correlation[0][1]) >= correlation_to_reach or abs(correlation[1][0]) >= correlation_to_reach:
        nb_correlation_all = nb_correlation_all + 1
        test = key.split('_')[1]
        if test in considered_tests:
            nb_correlation_considered = nb_correlation_considered + 1
    return nb_correlation_all, nb_correlation_considered

def count_commits(root_folder):
    commits = []
    considered_commits = []
    considered_tests = []
    unstable_commits = []
    all_tests = []
    correlated_map = {}
    for commit_folder in listdir(root_folder):
        commits.append(commit_folder)
        if commit_folder.startswith('86') or commit_folder.startswith('88'):
            continue
        diff_jjoules_directory = root_folder + '/' + commit_folder + '/diff-jjoules'
        if os.path.isdir(diff_jjoules_directory):
            diff_jjoules_files = listdir(diff_jjoules_directory)
            did_end_properly = True
            for diff_jjoules_file in diff_jjoules_files:
                if diff_jjoules_file == 'end.txt':
                    did_end_properly = False
                    with open(diff_jjoules_directory + '/' + diff_jjoules_file, 'r') as end_file:
                        content = end_file.read()
                        if content == 'The energy consumption are too unstable, no method could be considered.\n':
                            unstable_commits.append(commit_folder)
                            get_all_test_and_correlated_map(diff_jjoules_directory, all_tests, correlated_map)
            if did_end_properly:
                considered_commits.append(commit_folder)
                get_test_considered(diff_jjoules_directory, considered_tests)

    nb_strong_correlation_for_considered_tests = 0
    nb_strong_correlation_for_all_tests = 0
    nb_moderate_correlation_for_considered_tests = 0
    nb_moderate_correlation_for_all_tests = 0
    for key in correlated_map:
        correlation = correlated_map[key]
        nb_moderate_correlation_for_all_tests, nb_moderate_correlation_for_considered_tests = add_if_has_a_given_correlation(
            key, 
            considered_tests, 
            nb_moderate_correlation_for_all_tests, 
            nb_moderate_correlation_for_considered_tests, 
            correlation, 
            0.59
        )
        nb_strong_correlation_for_all_tests, nb_strong_correlation_for_considered_tests = add_if_has_a_given_correlation(
            key, 
            considered_tests, 
            nb_strong_correlation_for_all_tests, 
            nb_strong_correlation_for_considered_tests, 
            correlation, 
            0.79
        )

    print(
        to_row_latex([
            project,
            str(len(commits)), 
            format_int(len(commits), len(considered_commits)),
            str(len(considered_tests)),
            format_int(len(considered_tests), nb_strong_correlation_for_considered_tests),
            format_int(len(considered_tests), nb_moderate_correlation_for_considered_tests),
            format_int(len(commits), len(unstable_commits)),
            str(len(all_tests)),
            format_int(len(all_tests), nb_strong_correlation_for_all_tests),
            format_int(len(all_tests), nb_moderate_correlation_for_all_tests)
        ])
    )

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()

    print(
        to_header_latex([
            'Project',
            '\#Commits',
            '\#CoCommits',
            '\#Tests',
            '\#StrCorr',
            '\#ModCorr',
            '\#UnCommits',
            '\#Tests',
            '\#StrCorr',
            '\#ModCorr',
        ])
    )
    for project in PROJECTS:
        root_folder = args.output + '/' + project
        count_commits(root_folder)
    print(to_footer_latex())
 