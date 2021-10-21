import sys
import os

from utils.cmd.git_cmd import *
from utils.cmd.io_cmd import *
from utils.cmd.mvn_cmd import *
from utils.cmd.json_cmd import *
from utils.constants import *
from utils.args.build_evolution_graph_args import *
from utils.utils import *
from utils.statitics import *
from utils.cmd.latex_cmd import *
from utils.cmd.graph_cmd import *

def accumulate_deltas(delta_1, delta_2):
    acc = {}
    for key in delta_1:
        acc[key] = delta_1[key] + delta_2[key]
    return acc

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()

    root_folder = args.output + '/' + args.project

    considered_commits = get_considered_commits_and_sort(root_folder)
    considered_commits.reverse()

    delta_omegas = [
        {
            'energy': 0, 
            'instructions': 0,
            'durations': 0,
            'cycles': 0,
            'caches': 0,
            'cacheMisses': 0,
            'branches': 0,
            'branchMisses': 0
        }
    ]

    for considered_commit in considered_commits:
        id = get_id_commit_function(considered_commit)
        path_to_delta_omega_json = considered_commit + DELTA_OMEGA_FILE_NAME
        if isfile(path_to_delta_omega_json):
            delta_omega = read_json(path_to_delta_omega_json)
            delta_omegas.append(accumulate_deltas(delta_omegas[-1], delta_omega))

    plot_graph(delta_omegas, [ENERGY_KEY, INSTR_KEY, DURATIONS_KEY])
