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
from utils.cmd.graph_cmd import *

import matplotlib.pyplot as plt

def compute_cv_for_test(energy_data, instr_data, cycles_data):
    energy_med, energy_variance, energy_stddev, energy_cv, energy_qcd, energy_avg_abs_dev, energy_rel_avg_dev = stats(energy_data)
    instr_med, instr_variance, instr_stddev, instr_cv, instr_qcd, instr_avg_abs_dev, instr_rel_avg_dev = stats(instr_data)
    cycles_med, cycles_variance, cycles_stddev, cycles_cv, cycles_qcd, cycles_avg_abs_dev, cycles_rel_avg_dev = stats(cycles_data)
    return energy_cv, instr_cv, cycles_cv

def compute_cv_for_version(data, units, energy_cvs, instr_cvs, cycles_cvs):
    for test in data:
        energy_data, instr_data, cycles_data = from_dict_to_array_rm_zero_for_keys_array(data[test], units)
        if len(energy_data) == 0:
            continue
        energy_cv, instr_cv, cycles_cv = compute_cv_for_test(energy_data, instr_data, cycles_data)
        energy_cvs.append(energy_cv)
        instr_cvs.append(instr_cv)
        cycles_cvs.append(cycles_cv)
    return energy_cvs, instr_cvs, cycles_cvs

def compute_cv_for_commit(diff_jjoules_directory, units, energy_cvs, instr_cvs, cycles_cvs):
    data_V1 = read_json(diff_jjoules_directory + '/' + DATA_V1_JSON_FILE_NAME)
    data_V2 = read_json(diff_jjoules_directory + '/' + DATA_V2_JSON_FILE_NAME)
    energy_cvs, instr_cvs, cycles_cvs = compute_cv_for_version(data_V1, units, energy_cvs, instr_cvs, cycles_cvs)
    return compute_cv_for_version(data_V2, units, energy_cvs, instr_cvs, cycles_cvs)

def init_dict_for_df(key, cvs, dict_for_dataframe):
    for cv in cvs:
        dict_for_dataframe['unit'].append(key)
        dict_for_dataframe['value'].append(cv)
    return dict_for_dataframe

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()

    root_folder = args.output + 'gson'
    commit_folders = listdir(root_folder)
    units = [ENERGY_KEY, INSTR_KEY, CYCLES_KEY]
    energy_cvs, instr_cvs, cycles_cvs = [], [], []

    for commit_folder in commit_folders:
        print(commit_folders.index(commit_folder), '/', len(commit_folders))
        if commit_folder == 'rq2':
            continue
        diff_jjoules_directory = root_folder + '/' + commit_folder + '/diff-jjoules'
        end_properly = check_if_end_properly(diff_jjoules_directory)
        if end_properly:
            energy_cvs, instr_cvs, cycles_cvs = compute_cv_for_commit(diff_jjoules_directory, units, energy_cvs, instr_cvs, cycles_cvs)

    dict_for_dataframe = {}
    dict_for_dataframe['unit'] = []
    dict_for_dataframe['value'] = []
    dict_for_dataframe = init_dict_for_df(ENERGY_KEY, energy_cvs, dict_for_dataframe)
    dict_for_dataframe = init_dict_for_df(INSTR_KEY, instr_cvs, dict_for_dataframe)
    dict_for_dataframe = init_dict_for_df(CYCLES_KEY, cycles_cvs, dict_for_dataframe)
    dataframe = pd.DataFrame.from_dict(dict_for_dataframe)
    print(dataframe)
    
    sns.set_theme(style='whitegrid')
    ax = sns.violinplot(x='unit', y='value', data=dataframe)
    plt.show()
        