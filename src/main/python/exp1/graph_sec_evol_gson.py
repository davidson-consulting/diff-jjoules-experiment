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

def read_deltas(diff_jjoules_directory, units):
    deltas_per_test = read_json(diff_jjoules_directory + '/deltas.json')
    deltas_per_unit = {}
    for unit in units:
        deltas_per_unit[unit] = 0
    for test in deltas_per_test:
        for unit in units:
            deltas_per_unit[unit] = deltas_per_unit[unit] + deltas_per_test[test][unit]
    return deltas_per_unit
        

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()

    root_folder = args.output + 'gson'
    commit_folders = listdir(root_folder)
    commit_folders.sort(key=lambda commit_folder: -int(commit_folder.split('_')[0]) if commit_folder != 'rq2' else -1)

    units = [ENERGY_KEY, INSTR_KEY, CYCLES_KEY]
    acc_deltas_per_unit = {}
    for unit in units:
        acc_deltas_per_unit[unit] = [0]

    index_gray_line = []

    for commit_folder in commit_folders:
        if commit_folder == 'rq2':
            continue
        diff_jjoules_directory = root_folder + '/' + commit_folder + '/diff-jjoules'
        end_properly = check_if_end_properly(diff_jjoules_directory)
        if end_properly:
            deltas_per_unit = read_deltas(diff_jjoules_directory, units)
            index_gray_line.append(commit_folders.index(commit_folder))
            for unit in units:
                acc_deltas_per_unit[unit].append(acc_deltas_per_unit[unit][-1] + deltas_per_unit[unit])
        else:
            for unit in units:
                acc_deltas_per_unit[unit].append(acc_deltas_per_unit[unit][-1])
        
    fig, ax = plt.subplots()
    
    '''
    for xc in index_gray_line:
        ax.axvline(x=xc, color='gray', alpha=0.10)
    '''
        
    twin_x = ax.twinx()
    p1, = ax.plot(acc_deltas_per_unit[CYCLES_KEY], 'b-', label=CYCLES_KEY,)
    p2, = ax.plot(acc_deltas_per_unit[INSTR_KEY], 'r-', label=INSTR_KEY)
    p3, = twin_x.plot(acc_deltas_per_unit[ENERGY_KEY], 'g-', label=ENERGY_KEY)
    
    
    ax.set_xlabel("Commit")
    ax.set_ylabel("Number")
    twin_x.set_ylabel("SEC")

    ax.legend(handles=[p1, p2, p3])
    plt.show()