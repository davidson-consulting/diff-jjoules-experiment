import sys
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from utils.graph_args import *
from utils.json_utils import *


def build_graph(array):
    fig, ax = plt.subplots()
    t = np.arange(0.0, len(array))
    ax.plot(t, array)
    plt.show()

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()
    project_name = args.project_name
    path_to_data = args.data_path
    mode = args.mode

    path_to_commit_folders = path_to_data + '/' + project_name + '/'

    commits_folder = sorted(os.listdir(path_to_commit_folders), key=lambda folder_name: int(folder_name.split('_')[0]))
    commits_folder.reverse()
    energies_v1, energies_v2, durations_v1, durations_v2 = [], [], [], []
    delta_energy, delta_duration = [], []
    for file in os.listdir(path_to_commit_folders):
        path_to_file = path_to_commit_folders + file
        if file == 'input':
            continue
        data_v1 = read_json(path_to_file  + '/avg_v1.json')
        data_v2 = read_json(path_to_file  + '/avg_v2.json')
        energy_v1, duration_v1, energy_v2, duration_v2  = 0, 0, 0, 0
        for data in data_v1:
            energy_v1 = energy_v1 + data_v1[data]['energy']
            energy_v2 = energy_v2 + data_v2[data]['energy']
            duration_v1 = duration_v1 + data_v1[data]['duration']
            duration_v2 = duration_v2 + data_v2[data]['duration']
        energies_v1.append(energy_v1)
        energies_v2.append(energy_v2)
        durations_v1.append(duration_v1)
        durations_v2.append(duration_v2)
        delta_energy.append(energy_v2 - energy_v1)
        delta_duration.append(duration_v2 - duration_v1)
    build_graph(delta_energy)