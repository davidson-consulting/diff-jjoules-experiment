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

import matplotlib.pyplot as plt

def add_if_has_a_given_correlation(key, considered_tests, nb_correlation_all, nb_correlation_considered, correlation, correlation_to_reach):
    if abs(correlation[0][1]) >= correlation_to_reach or abs(correlation[1][0]) >= correlation_to_reach:
        nb_correlation_all = nb_correlation_all + 1
        test = key.split('_')[1]
        if test in considered_tests:
            nb_correlation_considered = nb_correlation_considered + 1
    return nb_correlation_all, nb_correlation_considered

def add_strong_and_mod_correlation(corrcoef_data, nb_strong, nb_mod):
    if abs(corrcoef_data[0][1]) >= 0.59 or abs(corrcoef_data[1][0]) >= 0.59:
        if abs(corrcoef_data[0][1]) >= 0.79 or abs(corrcoef_data[1][0]) >= 0.79:
            return nb_strong + 1, nb_mod + 1
        else:
            return nb_strong, nb_mod + 1
    else:
        return nb_strong, nb_mod

def has_any_zero(data):
    for d in data:
        if d[ENERGY_KEY] == 0.0:
            return True
    return False

def compute_nb_str_and_mod_corrcoef_for_data(data, nb_strong_instr, nb_mod_instr, nb_strong_cycles, nb_mod_cycles, nb_test):
    count_test = 0
    for test in data:
        corrcoef_instr, corrcoef_cycles = corrcoef(data[test])
        '''
        if abs(corrcoef_cycles[0][1]) >= 0.01 or abs(corrcoef_cycles[1][0]) >= 0.01:
            print(test)
            d_unit = {}
            for unit in [ENERGY_KEY, INSTR_KEY, CYCLES_KEY]:
                d_unit[unit] = []
            for d in data[test]:
                if d[ENERGY_KEY] > 0:
                    for unit in [ENERGY_KEY, INSTR_KEY, CYCLES_KEY]:
                        d_unit[unit].append(d[unit])
            markers = {}
            markers[INSTR_KEY] = 'bo'
            markers[CYCLES_KEY] = 'ro'
            print(sorted(d_unit[ENERGY_KEY]))
            for unit in [INSTR_KEY, CYCLES_KEY]:
                print(unit, sorted(d_unit[unit]))
                plt.plot(d_unit[ENERGY_KEY], d_unit[unit], markers[unit], label=unit,)
            plt.legend()
            plt.show()
            #sys.exit(1)
        '''
        count_test = count_test + 1
        nb_strong_instr, nb_mod_instr = add_strong_and_mod_correlation(corrcoef_instr, nb_strong_instr, nb_mod_instr)
        nb_strong_cycles, nb_mod_cycles = add_strong_and_mod_correlation(corrcoef_cycles, nb_strong_cycles, nb_mod_cycles)
    return nb_test + count_test, nb_strong_instr, nb_mod_instr, nb_strong_cycles, nb_mod_cycles

def compute_stats_for_commit(diff_jjoules_directory, nb_strong_instr, nb_mod_instr, nb_strong_cycles, nb_mod_cycles):
    id_commit = get_id_commit_function(diff_jjoules_directory)
    data_V1 = read_json(diff_jjoules_directory + '/' + DATA_V1_JSON_FILE_NAME)
    data_V2 = read_json(diff_jjoules_directory + '/' + DATA_V2_JSON_FILE_NAME)
    nb_test = 0
    nb_test, nb_strong_instr, nb_mod_instr, nb_strong_cycles, nb_mod_cycles = compute_nb_str_and_mod_corrcoef_for_data(data_V1, nb_strong_instr, nb_mod_instr, nb_strong_cycles, nb_mod_cycles, nb_test)
    nb_test, nb_strong_instr, nb_mod_instr, nb_strong_cycles, nb_mod_cycles = compute_nb_str_and_mod_corrcoef_for_data(data_V2, nb_strong_instr, nb_mod_instr, nb_strong_cycles, nb_mod_cycles, nb_test)
    return nb_test, nb_strong_instr, nb_mod_instr, nb_strong_cycles, nb_mod_cycles

def build_row_for_project(project, project_root_folder):
    commits = []
    nb_test, nb_strong_instr, nb_mod_instr, nb_strong_cycles, nb_mod_cycles = 0, 0, 0, 0, 0
    nb_applicable_commit = 0
    for commit_folder in listdir(project_root_folder):
        commits.append(commit_folder)
        diff_jjoules_directory = root_folder + '/' + commit_folder + '/diff-jjoules'
        end_properly = check_if_end_properly(diff_jjoules_directory)
        if end_properly:
            current_nb_test, nb_strong_instr, nb_mod_instr, nb_strong_cycles, nb_mod_cycles = compute_stats_for_commit(diff_jjoules_directory, nb_strong_instr, nb_mod_instr, nb_strong_cycles, nb_mod_cycles)
            nb_test = nb_test + current_nb_test
            nb_applicable_commit = nb_applicable_commit + 1
    print(to_row_latex([
        project,
        str(len(commits)),
        format_int(len(commits), nb_applicable_commit),
        str(nb_test),
        format_int(nb_test, nb_strong_instr),
        format_int(nb_test, nb_mod_instr),
        format_int(nb_test, nb_strong_cycles),
        format_int(nb_test, nb_mod_cycles),
    ]))

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()

    print(
        to_header_latex([
            'Project',
            '\#Commits',
            '\#CoCommits',
            '\#TestExec',
            '\#StrCorrInstr',
            '\#ModCorrIsntr',
            '\#StrCorrCycles',
            '\#ModCorrCycles',
        ])
    )
    for project in PROJECTS:
        root_folder = args.output + project
        build_row_for_project(project, root_folder)
    print(to_footer_latex())