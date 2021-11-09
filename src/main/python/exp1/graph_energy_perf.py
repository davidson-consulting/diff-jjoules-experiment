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

import matplotlib.pyplot as plt

def plot_energy_perf(project, project_root_folder):
    for commit_folder in listdir(project_root_folder):
        diff_jjoules_directory = root_folder + '/' + commit_folder + '/diff-jjoules'
        end_properly = check_if_end_properly(diff_jjoules_directory)
        if end_properly:
            data_v1 = read_json(diff_jjoules_directory + DATA_V1_JSON_FILE_NAME)
            for test in data_v1:
                data_test = data_v1[test]
                energies = from_dict_to_array_rm_zero(data_test, ENERGY_KEY)
                cycles = from_dict_to_array_rm_zero(data_test, CYCLES_KEY)
                instructions = from_dict_to_array_rm_zero(data_test, INSTR_KEY)
                plt.plot(energies, cycles[0:len(energies)], 'bo', label='CYCLES',)
                plt.plot(energies, instructions[0:len(energies)], 'ro', label='INSTR',)
                plt.legend()
                plt.show()

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()

    for project in PROJECTS:
        root_folder = args.output + project
        plot_energy_perf(project, root_folder)