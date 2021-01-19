import sys
import os
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from utils.graph_args import *
from utils.json_utils import *

def build_graph_compare_to_stoa(indices, acc_delta_energy, output_path):
    every = pd.read_csv("every.csv")
    every.columns = ['CommitID', 'Energy','Number']
    #every["Energy"] = every["Energy"] / 1000000
    ax=sns.lineplot(x="Number", y="Energy", data=every,  color='red',)
    ax.set(xlabel='Commit number', ylabel='Energy consumption (J)')
    df = pd.DataFrame({'Number': indices,
                    'Energy': acc_delta_energy,
                })
    sns.lineplot(x="Number", y="Energy", data=df,  color='lightblue',)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.clf()

def build_graph(array, output_path):
    fig, ax = plt.subplots()
    t = np.arange(0.0, len(array))
    ax.plot(t, array)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.clf()

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
    acc_delta_energy, acc_delta_duration = [0], [0]
    min_delta, max_delta = 0, 0
    min_commit, max_commit = '', ''
    index_commit = [0]
    with open('data/input/january_2021/gson/input', 'r') as commits_file:
        lines = commits_file.readlines()
        nb_tt_commit = len(lines) - 1
    for file in commits_folder:
        path_to_file = path_to_commit_folders + file
        data_v1 = read_json(path_to_file  + '/data_v1.json')
        data_v2 = read_json(path_to_file  + '/data_v2.json')
        energy_v1, duration_v1, energy_v2, duration_v2  = 0, 0, 0, 0
        if len(data_v1) == 0 or len(data_v2) == 0:
            continue
        for data in data_v1:
            if not data in data_v2:
                continue
            energy_v1 = energy_v1 + data_v1[data]['energy']
            duration_v1 = duration_v1 + data_v1[data]['duration']
            energy_v2 = energy_v2 + data_v2[data]['energy']
            duration_v2 = duration_v2 + data_v2[data]['duration']
        #current_energy_v1 = energy_v1 / len(data_v1) 
        #current_energy_v2 = energy_v2 / len(data_v2) 
        energies_v1.append(energy_v1)
        energies_v2.append(energy_v2)
        #energies_v1.append(current_energy_v1)
        #energies_v2.append(current_energy_v2)
        durations_v1.append(duration_v1)
        durations_v2.append(duration_v2)
        current_delta_energy = energy_v2 - energy_v1
        #current_delta_energy = current_energy_v2 - current_energy_v1
        current_delta_duration = duration_v2 - duration_v1
        delta_energy.append(current_delta_energy)
        delta_duration.append(current_delta_duration)
        if len(acc_delta_energy) == 0:
            acc_delta_energy.append(current_delta_energy)
            acc_delta_duration.append(current_delta_duration)
        else:
            acc_delta_energy.append(acc_delta_energy[-1] + current_delta_energy)
            acc_delta_duration.append(acc_delta_duration[-1] + current_delta_duration)
        print(file, 
             '{:.2f}'.format(float(current_delta_energy/1E6)), 
            '{:.2f}'.format(float(acc_delta_energy[-2]/1E6)), 
            '{:.2f}'.format(float(acc_delta_energy[-1]/1E6))
        )
        if len(index_commit) == 0:
            index_commit.append(nb_tt_commit - int(file.split('_')[0])-1)
        index_commit.append(nb_tt_commit - int(file.split('_')[0]))
        if min_delta == 0:
            min_delta = acc_delta_energy[-1]
        if max_delta == 0:
            max_delta = acc_delta_energy[-1]
        if acc_delta_energy[-1] > max_delta:
            max_commit = file
            max_delta = acc_delta_energy[-1]
        if acc_delta_energy[-1] < min_delta:
            min_commit = file
            min_delta = acc_delta_energy[-1]
    print(min_commit, min_delta)
    print(max_commit, max_delta)
    for acc in acc_delta_energy:
        print(index_commit[acc_delta_energy.index(acc)], acc)
    build_graph(acc_delta_energy, path_to_commit_folders + '/delta_energy_evolution.png')
    build_graph(acc_delta_duration, path_to_commit_folders + '/delta_duration_evolution.png')
    if project_name == 'gson':
        build_graph_compare_to_stoa(index_commit, acc_delta_energy, path_to_commit_folders + '/compare_to_stoa.png')