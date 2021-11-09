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

def compute_stats_and_add(data, key, medianes_per_unit, variances_per_unit):
    med, variance, stddev, cv, qcd = stats(data)
    medianes_per_unit[key].append(med)
    variances_per_unit[key].append(variance)
    return medianes_per_unit, variances_per_unit

def compute_med_and_var(diff_jjoules_directory, data, units, nb_test, medianes_per_unit, variances_per_unit):
    count_test = 0
    for test in data:
        energy_data, instr_data, cycles_data = from_dict_to_array_rm_zero_for_keys_array(data[test], units)
        stats_per_unit = stats_for_given_units(data[test], units)
        if len(energy_data) == 0 or len(instr_data) == 0 or len(cycles_data) == 0:
            print(diff_jjoules_directory, test)
            continue
        medianes_per_unit, variances_per_unit = compute_stats_and_add(energy_data, ENERGY_KEY, medianes_per_unit, variances_per_unit)
        medianes_per_unit, variances_per_unit = compute_stats_and_add(instr_data, INSTR_KEY, medianes_per_unit, variances_per_unit)
        medianes_per_unit, variances_per_unit = compute_stats_and_add(cycles_data, CYCLES_KEY, medianes_per_unit, variances_per_unit)
        count_test = count_test + 1
    return nb_test + count_test, medianes_per_unit, variances_per_unit

def compute_stats_for_commit(diff_jjoules_directory, units, medianes_per_unit, variances_per_unit):
    id_commit = get_id_commit_function(diff_jjoules_directory)
    data_V1 = read_json(diff_jjoules_directory + '/' + DATA_V1_JSON_FILE_NAME)
    data_V2 = read_json(diff_jjoules_directory + '/' + DATA_V2_JSON_FILE_NAME)
    nb_test = 0
    nb_test, medianes_per_unit, variances_per_unit = compute_med_and_var(diff_jjoules_directory + '/' + DATA_V1_JSON_FILE_NAME, data_V1, units, nb_test, medianes_per_unit, variances_per_unit)
    nb_test, medianes_per_unit, variances_per_unit = compute_med_and_var(diff_jjoules_directory + '/' + DATA_V2_JSON_FILE_NAME, data_V2, units, nb_test, medianes_per_unit, variances_per_unit)
    return nb_test, medianes_per_unit, variances_per_unit

def build_row_for_project(project, project_root_folder):
    commits = []
    medianes_per_unit, variances_per_unit = {}, {}
    units = [ENERGY_KEY, INSTR_KEY, CYCLES_KEY]
    for unit in units:
        medianes_per_unit[unit] = []
        variances_per_unit[unit] = []
    nb_test, nb_applicable_commit = 0, 0
    for commit_folder in listdir(project_root_folder):
        commits.append(commit_folder)
        diff_jjoules_directory = root_folder + '/' + commit_folder + '/diff-jjoules'
        end_properly = check_if_end_properly(diff_jjoules_directory)
        if end_properly:
            current_nb_test, medianes_per_unit, variances_per_unit = compute_stats_for_commit(diff_jjoules_directory, units, medianes_per_unit, variances_per_unit)
            nb_test = nb_test + current_nb_test
            nb_applicable_commit = nb_applicable_commit + 1
    corrcoef_instr = corrcoef_datas(medianes_per_unit[ENERGY_KEY], medianes_per_unit[INSTR_KEY])
    corrcoef_cycles = corrcoef_datas(medianes_per_unit[ENERGY_KEY], medianes_per_unit[CYCLES_KEY])
    avg_variance_per_unit, avg_stddev_per_unit = compute_avg_variance_avg_stddev_for_given_units(variances_per_unit, units)
    to_be_printed = [
        project,
        str(len(commits)),
        format_int(len(commits), nb_applicable_commit),
        str(nb_test),
        '{:.2f}'.format(corrcoef_instr[0][1]),
        '{:.2f}'.format(corrcoef_cycles[0][1]),
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
            '$\\rho_{instr}$',
            '$\\rho_{cycles}$',
            '$\\bar{x}_\\sigma(SEC)$',
            '$\\bar{x}_\\sigma(instr)$',
            '$\\bar{x}_\\sigma(cycles)$',
        ])
    )
    for project in PROJECTS:
        root_folder = args.output + project
        build_row_for_project(project, root_folder)
    print(to_footer_latex())