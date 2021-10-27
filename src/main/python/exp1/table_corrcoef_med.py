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

def compute_medianes_per_unit(data, nb_test, units, medianes_per_unit):
    count_test = 0
    for test in data:
        energy_data, instr_data, cycles_data = from_dict_to_array_rm_zero_for_keys_array(data[test], units)
        if len(energy_data) == 0 or len(instr_data) == 0 or len(cycles_data) == 0:
            print(test)
            continue
        medianes_per_unit[ENERGY_KEY].append(mediane(energy_data))
        medianes_per_unit[INSTR_KEY].append(mediane(instr_data))
        medianes_per_unit[CYCLES_KEY].append(mediane(cycles_data))
        count_test = count_test + 1
    if count_test == 0
        print('no test could be monitored properly')
    return nb_test + count_test, medianes_per_unit

def compute_stats_for_commit(diff_jjoules_directory, units, medianes_per_unit):
    id_commit = get_id_commit_function(diff_jjoules_directory)
    data_V1 = read_json(diff_jjoules_directory + '/' + DATA_V1_JSON_FILE_NAME)
    data_V2 = read_json(diff_jjoules_directory + '/' + DATA_V2_JSON_FILE_NAME)
    nb_test = 0
    print(diff_jjoules_directory)
    nb_test, medianes_per_unit = compute_medianes_per_unit(data_V1, nb_test, units, medianes_per_unit)
    nb_test, medianes_per_unit = compute_medianes_per_unit(data_V2, nb_test, units, medianes_per_unit)
    return nb_test, medianes_per_unit

def build_row_for_project(project, project_root_folder):
    commits = []
    medianes_per_unit = {}
    units = [ENERGY_KEY, INSTR_KEY, CYCLES_KEY]
    for unit in units:
        medianes_per_unit[unit] = []
    nb_test, nb_applicable_commit = 0, 0
    for commit_folder in listdir(project_root_folder):
        commits.append(commit_folder)
        diff_jjoules_directory = root_folder + '/' + commit_folder + '/diff-jjoules'
        end_properly = check_if_end_properly(diff_jjoules_directory)
        if end_properly:
            current_nb_test, medianes_per_unit = compute_stats_for_commit(diff_jjoules_directory, units, medianes_per_unit)
            nb_test = nb_test + current_nb_test
            nb_applicable_commit = nb_applicable_commit + 1
    corrcoef_instr = corrcoef_datas(medianes_per_unit[ENERGY_KEY], medianes_per_unit[INSTR_KEY])
    corrcoef_cycles = corrcoef_datas(medianes_per_unit[ENERGY_KEY], medianes_per_unit[CYCLES_KEY])
    print(to_row_latex([
        project,
        str(len(commits)),
        format_int(len(commits), nb_applicable_commit),
        str(nb_test),
        '{:.2f}'.format(corrcoef_instr[0][1]),
        '{:.2f}'.format(corrcoef_cycles[0][1]),
    ]))

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()

    print(
        to_header_latex([
            'Project',
            '\#Commits',
            '\#CoCommits',
            '\#TestExec',
            'CoeffCorrInstr',
            'CoeffCorrCycles'
        ])
    )
    for project in PROJECTS:
        root_folder = args.output + project
        build_row_for_project(project, root_folder)
    print(to_footer_latex())