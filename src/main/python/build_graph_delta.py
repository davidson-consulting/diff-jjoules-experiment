import sys
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from utils.graph_args import *
from utils.json_utils import *


def get_max(arrayv1, arrayv2):
    current_max = -1
    for i in range(0, len(arrayv1)):
        if arrayv1[i] > current_max:
            if arrayv2[i] > arrayv1[i]:
                current_max = arrayv2[i]
            else:
                current_max = arrayv1[i]
        elif arrayv2[i] > current_max:
            current_max = arrayv2[i]
    return current_max

def build_graph(energies_v1, energies_v2, labels, colors, classfier, unit, output='graph.png'):
    classifier_v1 = classfier + 'V1'
    classifier_v2 = classfier + 'V2'
    df = pd.DataFrame({'Test': labels,
                    classifier_v1: energies_v1,
                    classifier_v2: energies_v2,
                }, index=labels)
    '''
    bar_plot = sns.barplot(x=classifier_v1, y="Test", data=df, order=labels, color=colors[0])
    bar_plot = sns.barplot(x=classifier_v2, y='Test', data=df, order=labels, color=colors[1])
    bar_plot.set(xlabel=classfier + ' in ' + unit, ylabel="Test")
    plt.tight_layout()
    plt.savefig(output + '.png')
    plt.clf()
    '''

    bar_plot = sns.barplot(x="Test", y=classifier_v1, data=df, order=labels, color=colors[0])
    bar_plot = sns.barplot(x='Test', y=classifier_v2, data=df, order=labels, color=colors[1])
    bar_plot.set(ylabel=classfier + ' in ' + unit, xlabel="Test")
    plt.tight_layout()
    plt.savefig(output + '_v.png')
    plt.clf()

def get_test_class(key):
    return key.split('-')[0]

def build_data_per_class(data_v1, data_v2):
    energies_v1 = {}
    durations_v1 = {}
    energies_v2 = {}
    durations_v2 = {}
    labels = []
    done_test_class_names = []
    for key in data_v1:
        if not key in data_v2:
            continue
        test_class_name = get_test_class(key)
        if not test_class_name in done_test_class_names:
            labels.append(str(len(done_test_class_names)))
            done_test_class_names.append(test_class_name)
            energies_v1[test_class_name] = data_v1[key]['energy']
            durations_v1[test_class_name] = data_v1[key]['duration']
            energies_v2[test_class_name] = data_v2[key]['energy']
            durations_v2[test_class_name] = data_v2[key]['duration']
        else:
            energies_v1[test_class_name] = energies_v1[test_class_name] + data_v1[key]['energy']
            durations_v1[test_class_name] = durations_v1[test_class_name] + data_v1[key]['duration']
            energies_v2[test_class_name] = energies_v2[test_class_name] + data_v2[key]['energy']
            durations_v2[test_class_name] = durations_v2[test_class_name] + data_v2[key]['duration']

    delta_energies_v1 = []
    delta_energies_v2 = []
    energies_v1_values = list(energies_v1.values())
    energies_v2_values = list(energies_v2.values())
    delta_durations_v1 = []
    delta_durations_v2 = []
    durations_v1_values = list(durations_v1.values())
    durations_v2_values = list(durations_v2.values())

    delta_energies_v1_1 = []
    delta_energies_v2_1 = []

    for i in range(0, len(energies_v1)):
        delta_energy = energies_v1_values[i] - energies_v2_values[i]
        if delta_energy < 0:
            delta_energies_v1_1.append(0)
            delta_energies_v2_1.append(-delta_energy)
            delta_energies_v1.append(delta_energy)
            delta_energies_v2.append(0)
        else:
            delta_energies_v2_1.append(0)
            delta_energies_v1_1.append(-delta_energy)
            delta_energies_v2.append(delta_energy)
            delta_energies_v1.append(0)
        delta_duration = durations_v1_values[i] - durations_v2_values[i]
        if delta_energy < 0:
            delta_durations_v1.append(delta_duration)
            delta_durations_v2.append(0)
        else:
            delta_durations_v2.append(delta_duration)
            delta_durations_v1.append(0)
    return delta_energies_v1, delta_durations_v1, delta_energies_v2, delta_durations_v2, labels, delta_energies_v1_1, delta_energies_v2_1

def get_test_name(key):
    return key.split('-')[1]

def build_data_per_test(data_v1, data_v2):
    test_per_test_classes = {}
    energies_v1 = {}
    durations_v1 = {}
    energies_v2 = {}
    durations_v2 = {}
    for key in data_v1:
        if not key in data_v2:
            continue
        test_class_name = get_test_class(key)
        if not test_class_name in test_per_test_classes:
            test_per_test_classes[test_class_name] = []
        test_per_test_classes[test_class_name].append(get_test_name(key))
        energies_v1[key] = data_v1[key]['energy']
        durations_v1[key] = data_v1[key]['duration']
        energies_v2[key] = data_v2[key]['energy']
        durations_v2[key] = data_v2[key]['duration']

    fullqualified_name_test = []
    delta_energies_v1 = []
    delta_energies_v2 = []
    delta_durations_v1 = []
    delta_durations_v2 = []
    for test_class_name in test_per_test_classes:
        current_energies_v1 = []
        current_durations_v1 = []
        current_energies_v2 = []
        current_durations_v2 = []
        labels = []
        for test in test_per_test_classes[test_class_name]:
            labels.append(test)
            energy_v1 = energies_v1[test_class_name + '-' + test]
            energy_v2 = energies_v2[test_class_name + '-' + test]
            duration_v1 = durations_v1[test_class_name + '-' + test]
            duration_v2 = durations_v2[test_class_name + '-' + test]
            current_energies_v1.append(energy_v1)
            current_durations_v1.append(duration_v1)
            current_energies_v2.append(energy_v2)
            current_durations_v2.append(duration_v2)
            
            delta_energy = energy_v2 - energy_v1
            if delta_energy < 0:
                delta_energies_v1.append(delta_energy)
                delta_energies_v2.append(0)
            else:
                delta_energies_v1.append(0)
                delta_energies_v2.append(delta_energy)
                
            delta_duration = duration_v2 - duration_v1
            if delta_duration < 0:
                delta_durations_v2.append(0)
                delta_durations_v1.append(delta_duration)
            else:
                delta_durations_v2.append(delta_duration)
                delta_durations_v1.append(0)

            fullqualified_name_test.append(test_class_name + '-' + test)
    return fullqualified_name_test, delta_energies_v1, delta_energies_v2, delta_durations_v1, delta_durations_v2
    
def build_graph_per_test(array_v1, array_v2, path_to_file, project_name, dimension, unit):
    nb_max_bar_per_graph = min(10, len(array_v1))
    if nb_max_bar_per_graph == 0:
        return
    nb_graph = int(len(array_v1) / nb_max_bar_per_graph)
    nb_bar_last_graph = int(len(array_v1) % nb_max_bar_per_graph) 
    if nb_bar_last_graph < 5:
        nb_max_bar_per_graph = nb_max_bar_per_graph + nb_bar_last_graph
    nb_graph = int(len(array_v1) / nb_max_bar_per_graph)
    nb_bar_last_graph = int(len(array_v1) % nb_max_bar_per_graph) 
    print(dimension,  len(array_v1), nb_graph, nb_max_bar_per_graph, nb_bar_last_graph)
    i = 0
    for i in range(0, nb_graph):
        labels_it = [str(l) for l in range(i*nb_max_bar_per_graph, (i+1)*nb_max_bar_per_graph)]
        print(i*nb_max_bar_per_graph, (i+1)*nb_max_bar_per_graph, array_v1[i*nb_max_bar_per_graph:(i+1)*nb_max_bar_per_graph])
        print(i*nb_max_bar_per_graph, (i+1)*nb_max_bar_per_graph, array_v2[i*nb_max_bar_per_graph:(i+1)*nb_max_bar_per_graph])
        build_graph(
            array_v1[i*nb_max_bar_per_graph:(i+1)*nb_max_bar_per_graph],
            array_v2[i*nb_max_bar_per_graph:(i+1)*nb_max_bar_per_graph], 
            labels_it, 
            ['blue', 'red'], 
            dimension,
            unit,
            output=path_to_file + '/'+ project_name +'_delta_'+ dimension + '_' + str(i)
        )
    print(len(array_v1), nb_graph, nb_max_bar_per_graph, nb_graph*nb_max_bar_per_graph, i)
    if len(array_v1) > nb_graph*nb_max_bar_per_graph:
        labels_it = [str(l) for l in range(nb_graph*nb_max_bar_per_graph, len(array_v1))]
        print(nb_graph*nb_max_bar_per_graph, array_v1[nb_graph*nb_max_bar_per_graph:])
        print(nb_graph*nb_max_bar_per_graph, array_v1[nb_graph*nb_max_bar_per_graph:])
        build_graph(
            array_v1[nb_graph*nb_max_bar_per_graph:],
            array_v2[nb_graph*nb_max_bar_per_graph:], 
            labels_it,
            ['blue', 'red'], 
            dimension,
            unit,
            output=path_to_file + '/'+ project_name +'_delta_'+ dimension + '_' + str(i+1)
        )

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()
    project_name = args.project_name
    path_to_data = args.data_path
    mode = args.mode

    path_to_commit_folders = path_to_data + '/' + project_name + '/'

    for file in os.listdir(path_to_commit_folders):
        #if not file.startswith('118_'):
        #    continue
        path_to_file = path_to_commit_folders + file
        if file == 'input' or file.endswith('.png') or file == 'README.md':
            continue
        print('generate', mode, 'for', file)
        data_v1 = read_json(path_to_file  + '/data_v1.json')
        data_v2 = read_json(path_to_file  + '/data_v2.json')

        if mode == mode.per_class:
            energies_v1, durations_v1, energies_v2, durations_v2, labels, delta_energies_v1_1, delta_energies_v2_1 = build_data_per_class(data_v1, data_v2)
            build_graph(energies_v1, durations_v1, energies_v2, durations_v2, labels, colors=['red', 'blue'], output=path_to_file + '/'+ project_name +'_delta')
            build_graph(delta_energies_v1_1, durations_v1, delta_energies_v2_1, durations_v2, labels, colors=['blue', 'red'], output=path_to_file + '/'+ project_name +'_delta_1')
        elif mode == mode.per_test:
            if not os.path.isfile(path_to_file + '/' + project_name + '_delta_duration_0_v.png'):
                fullqualified_name_test, delta_energies_v1, delta_energies_v2, delta_durations_v1, delta_durations_v2 = build_data_per_test(data_v1, data_v2)
                build_graph_per_test(delta_energies_v1, delta_energies_v2, path_to_file, project_name, 'energy', 'uJ')
                build_graph_per_test(delta_durations_v1, delta_durations_v2, path_to_file, project_name, 'duration', 's')
            else:
                print(path_to_file, 'already generated')
        else:
            print('unkown mode', mode)
