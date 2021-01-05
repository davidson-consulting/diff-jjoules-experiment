import sys
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from utils.graph_args import *
from utils.json_utils import *


def build_graph(array, output_path):
    fig, ax = plt.subplots()
    t = np.arange(0.0, len(array))
    ax.plot(t, array)
    plt.tight_layout()
    plt.savefig(output_path)

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()
    project_name = args.project_name
    path_to_data = args.data_path
    mode = args.mode

    path_to_commit_folders = path_to_data + '/' + project_name + '/'

    commits_folder = list(filter(lambda x: not (x == 'README.md' or x.endswith('.png')), os.listdir(path_to_commit_folders)))
    commits_folder = sorted(commits_folder, key=lambda folder_name: int(folder_name.split('_')[0]))
    commits_folder.reverse()
    energies_v1, energies_v2, durations_v1, durations_v2 = [], [], [], []
    delta_energy, delta_duration = [], []
    acc_delta_energy, acc_delta_duration = [], []
    for file in commits_folder:
        path_to_file = path_to_commit_folders + file
        data_v1 = read_json(path_to_file  + '/avg_v1.json')
        data_v2 = read_json(path_to_file  + '/avg_v2.json')
        energy_v1, duration_v1, energy_v2, duration_v2  = 0, 0, 0, 0
        for data in data_v1:
            if not data in data_v2:
                continue
            energy_v1 = energy_v1 + data_v1[data]['energy']
            duration_v1 = duration_v1 + data_v1[data]['duration']
            energy_v2 = energy_v2 + data_v2[data]['energy']
            duration_v2 = duration_v2 + data_v2[data]['duration']
        energies_v1.append(energy_v1)
        energies_v2.append(energy_v2)
        durations_v1.append(duration_v1)
        durations_v2.append(duration_v2)
        delta_energy.append(energy_v2 - energy_v1)
        delta_duration.append(duration_v2 - duration_v1)
        if len(acc_delta_energy) == 0:
            acc_delta_energy.append(energy_v2 - energy_v1)
            acc_delta_duration.append(duration_v2 - duration_v1)
        else:
            acc_delta_energy.append(acc_delta_energy[-1] + (energy_v2 - energy_v1))
            acc_delta_duration.append(acc_delta_duration[-1] + (duration_v2 - duration_v1))
    build_graph(acc_delta_energy, path_to_commit_folders + '/delta_energy_evolution.png')
    build_graph(acc_delta_duration, path_to_commit_folders + '/delta_duration_evolution.png')