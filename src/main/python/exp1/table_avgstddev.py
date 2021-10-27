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

def compute_med_and_var(data, units, nb_test, medianes_per_unit, variances_per_unit):
    count_test = 0
    for test in data:
        stats_per_unit = stats_for_given_units(data[test], units)
        for unit in units:
            if len(stats_per_unit[unit]) > 0:
                medianes_per_unit[unit].append(stats_per_unit[unit][0])
                variances_per_unit[unit].append(stats_per_unit[unit][1])
        count_test = count_test + 1
    return nb_test + count_test, medianes_per_unit, variances_per_unit

def compute_stats_for_commit(diff_jjoules_directory, units, medianes_per_unit, variances_per_unit):
    id_commit = get_id_commit_function(diff_jjoules_directory)
    data_V1 = read_json(diff_jjoules_directory + '/' + DATA_V1_JSON_FILE_NAME)
    data_V2 = read_json(diff_jjoules_directory + '/' + DATA_V2_JSON_FILE_NAME)
    nb_test = 0
    nb_test, medianes_per_unit, variances_per_unit = compute_med_and_var(data_V1, units, nb_test, medianes_per_unit, variances_per_unit)
    nb_test, medianes_per_unit, variances_per_unit = compute_med_and_var(data_V2, units, nb_test, medianes_per_unit, variances_per_unit)
    return nb_test, medianes_per_unit, variances_per_unit

def build_row_for_project(project, project_root_folder):
    units = [ENERGY_KEY, INSTR_KEY, CYCLES_KEY]
    commits = []
    nb_applicable_commit = 0
    medianes_per_unit, variances_per_unit = {}, {}
    nb_test = 0
    for unit in units:
        medianes_per_unit[unit] = []
        variances_per_unit[unit] = []
    for commit_folder in listdir(project_root_folder):
        commits.append(commit_folder)
        diff_jjoules_directory = root_folder + '/' + commit_folder + '/diff-jjoules'
        end_properly = check_if_end_properly(diff_jjoules_directory)
        if end_properly:
            current_nb_test, medianes_per_unit, variances_per_unit = compute_stats_for_commit(diff_jjoules_directory, units, medianes_per_unit, variances_per_unit)
            nb_test = nb_test + current_nb_test
            nb_applicable_commit = nb_applicable_commit + 1
    avg_variance_per_unit, avg_stddev_per_unit = compute_avg_variance_avg_stddev_for_given_units(variances_per_unit, units)
    
    to_be_printed = [
        project,
        str(len(commits)),
        format_int(len(commits), nb_applicable_commit),
        str(nb_test),
    ]
    for unit in units:
        avg_mediane = average(medianes_per_unit[unit])
        to_be_printed.append(compute_and_format_perc(avg_mediane, avg_stddev_per_unit[unit]))
    print(to_row_latex(to_be_printed))

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()

    print(
        to_header_latex([
            'Project',
            '\#Commits',
            '\#CoCommits',
            '\#TestExec',
            'AVG$_\sigma(SEC)$',
            'AVG$_\sigma(Instr)$',
            'AVG$_\sigma(Cycles)$',
        ])
    )
    for project in PROJECTS:
        root_folder = args.output + project
        build_row_for_project(project, root_folder)
    print(to_footer_latex())
 