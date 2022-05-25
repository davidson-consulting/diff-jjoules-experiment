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

import seaborn as sns

def get_cvs(data):
    units = [ENERGY_KEY, INSTR_KEY, CYCLES_KEY]
    cvs_cycles = []
    cvs_energies = []
    cvs_instr = []
    for test in data:
        energy_data, instr_data, cycles_data = from_dict_to_array_rm_zero_for_keys_array(data[test], units)
        if len(energy_data) == 0:
            print(test)
            continue
        energy_med, energy_variance, energy_stddev, energy_cv, energy_qcd, energy_avg_abs_dev, energy_rel_avg_dev = stats(energy_data)
        instr_med, instr_variance, instr_stddev, instr_cv, instr_qcd, instr_avg_abs_dev, instr_rel_avg_dev = stats(instr_data)
        cycles_med, cycles_variance, cycles_stddev, cycles_cv, cycles_qcd, cycles_avg_abs_dev, cycles_rel_avg_dev = stats(cycles_data)
        cvs_cycles.append(cycles_cv)
        cvs_energies.append(energy_cv)
        cvs_instr.append(instr_cv)
    return cvs_energies, cvs_instr, cvs_cycles

def draw_distribution(project, project_root_folder):
    cvs_cycles = []
    cvs_energies = []
    cvs_instr = []
    commit_folders = listdir(project_root_folder)
    commit_folders.sort(key=lambda commit_folder: int(commit_folder.split('_')[0]) if commit_folder != 'rq2' else -1)
    nb_properly_ended = 0
    for commit_folder in commit_folders:
        diff_jjoules_directory = root_folder + '/' + commit_folder + '/diff-jjoules'
        end_properly = check_if_end_properly(diff_jjoules_directory)
        if end_properly:
            data_v1 = read_json(diff_jjoules_directory + DATA_V1_JSON_FILE_NAME)
            data_v2 = read_json(diff_jjoules_directory + DATA_V2_JSON_FILE_NAME)
            energy_cv, instr_cv, cycles_cv = get_cvs(data_v1)
            cvs_cycles.extend(cycles_cv)
            cvs_energies.extend(energy_cv)
            cvs_instr.extend(instr_cv)
            energy_cv, instr_cv, cycles_cv = get_cvs(data_v2)
            cvs_cycles.extend(cycles_cv)
            cvs_energies.extend(energy_cv)
            cvs_instr.extend(instr_cv)
            nb_properly_ended = nb_properly_ended + 1
        if nb_properly_ended >= 50:
            break
            
    '''
    kwargs = dict(alpha=0.5, bins=100, density=True, stacked=True)
    plt.hist(cvs_energies, **kwargs,  color='g', label='SEC')
    plt.hist(cvs_instr, **kwargs,  color='b', label='Instr')
    plt.hist(cvs_cycles, **kwargs,  color='r', label='Cycles')
    '''
    kwargs = dict(hist_kws={'alpha':.6}, kde_kws={'linewidth':2})

    sns.distplot(cvs_instr, color="orange", label="Instr", **kwargs)
    sns.distplot(cvs_cycles, color="deeppink", label="Cycles", **kwargs)
    sns.distplot(cvs_energies, color="dodgerblue", label="SEC", **kwargs)
    plt.xlim(-0.1, 1.1)
    plt.legend()
    plt.title(project)
    plt.tight_layout()
    plt.savefig('pictures/exp1/dist_' + project + '.png', dpi='figure')
    plt.clf()

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()
    sns.set_style("white")

    for project in PROJECTS:
        root_folder = args.output + project + '/exp1'
        draw_distribution(project, root_folder)