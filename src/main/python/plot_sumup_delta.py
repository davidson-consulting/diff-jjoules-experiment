import math
import seaborn as sns
import os
import matplotlib.pyplot as plt
import numpy as np

from utils.json_utils import *

def to_test_name(json_file_name):
    return json_file_name[0:len(json_file_name) - len('.json')]

def to_array_for_violin(data):
    array = []
    for d in data:
        array.append(np.array(data[d]))
    return array

def to_array_for_violin_with_key(data, key):
    array = []
    for d in data:
        array.append(np.array(data[d][key]))
    return array

def read_json_iteration(path, factor=1):
    data = {}
    total = []
    sorted_iteration_folders = sorted(os.listdir(path), key= lambda x: int(x))
    for iteration_directory in sorted_iteration_folders[0:100]:
        current_energy_for_all = 0
        sorted_test_json_files = sorted(os.listdir(path + '/' + iteration_directory), key= lambda x: x)
        for json_test_file in sorted_test_json_files[0:20]:
            data_test_json = read_json(path + '/' + iteration_directory + '/' + json_test_file)
            test_name = to_test_name(json_test_file)
            if not test_name in data:
                data[test_name] = {}
                data[test_name]['energy'] = []
                data[test_name]['duration'] = []
                data[test_name]['power'] = []
            current_energy = data_test_json['package|uJ'] / factor
            current_duration = data_test_json['duration|ns'] / factor
            data[test_name]['energy'].append(current_energy)
            data[test_name]['duration'].append(current_duration)
            data[test_name]['power'].append(current_energy / current_duration)
            current_energy_for_all = current_energy_for_all + current_energy
        total.append(current_energy_for_all)
            
    for test_name in data:
        mediane = compute_mediane(data[test_name]['energy'])
        q1, q3 = compute_quartiles(data[test_name]['energy'])
        mean_energy = sum(data[test_name]['energy']) / len(data[test_name]['energy'])
        deviations = [ (x - mean_energy) ** 2 for x in data[test_name]['energy'] ]
        variance = sum(deviations) / len(deviations)
        stddev = math.sqrt(variance)
        data[test_name]['mediane'] = mediane
        data[test_name]['q1'] = q1
        data[test_name]['q3'] = q3
        data[test_name]['qcd'] = (q3 - q1) / (q3 + q1)
        data[test_name]['stddev'] = stddev
        data[test_name]['cv'] = stddev / mean_energy
    return data, total

def compute_quartiles(data):
    data = sorted(data)
    if len(data) % 2 == 0:
        cursor_middle = int(len(data) / 2)
        return compute_mediane(data[:cursor_middle]), compute_mediane(data[cursor_middle:])
    else:
        cursor_end_q1 = int((len(data) / 2) - 1)
        cursor_begin_q3 = int((len(data) / 2) + 1)
        return compute_mediane(data[:cursor_end_q1]), compute_mediane(data[cursor_begin_q3:])

def compute_mediane(data):
    data = sorted(data)
    if len(data) % 2 == 0:
        middle_cursor = int(len(data) / 2)
        return (data[middle_cursor - 1] + data[middle_cursor]) / 2
    else:
        return data[int(len(data)/2)]

def compute_medianes(data, nb_element, key):
    medianes_per_test = {}
    for test in data:
        medianes_per_test[test] = []
        current_data = data[test][key]
        nb_medianes = len(current_data) / nb_element
        for i in range(int(nb_medianes)):
            share = current_data[i*nb_element:(i+1)*nb_element]
            medianes_per_test[test].append(compute_mediane(share))
    return medianes_per_test

def compute_min(data):
    nb_element = 10
    min_energy = {}
    index_min_energy = {}
    for test in data:
        nb_min = int(len(data[test]['energy']) / 10)
        min_energy[test] = []
        index_min_energy[test] = []
        for i in range(0, nb_min):
            test_energy_sorted = sorted(data[test]['energy'][i * nb_element:(i+1) * nb_element])
            test_min_energy = test_energy_sorted[0]
            min_energy[test].append(test_min_energy)
            index_min_energy[test].append(data[test]['energy'].index(test_min_energy))
    return min_energy, index_min_energy

def compute_mins(data_mvn_10, data_mvn_100, data_mvn_1000, data_mvn_2000):
    mins_10, index = compute_min(data_mvn_10)
    mins_100, index = compute_min(data_mvn_100)
    mins_1000, index = compute_min(data_mvn_1000)
    mins_2000, index = compute_min(data_mvn_2000)

    return mins_10, mins_100, mins_1000, mins_2000

def inner_compute_mediane(data):
    nb_element = 10
    mediane_energy = {}
    for test in data:
        nb = int(len(data[test]['energy']) / 10)
        mediane_energy[test] = []
        for i in range(0, nb):
            test_energy_sorted = sorted(data[test]['energy'][i * nb_element:(i+1) * nb_element])
            test_energy = compute_mediane(test_energy_sorted)
            mediane_energy[test].append(test_energy)
    return mediane_energy

def compute_medianes(data_mvn_10, data_mvn_100, data_mvn_1000, data_mvn_2000):
    mins_10 = inner_compute_mediane(data_mvn_10)
    mins_100 = inner_compute_mediane(data_mvn_100)
    mins_1000 = inner_compute_mediane(data_mvn_1000)
    mins_2000 = inner_compute_mediane(data_mvn_2000)

    return mins_10, mins_100, mins_1000, mins_2000

def compute_deltas(mins_10, mins_100, mins_1000, mins_2000, mins_10_2, mins_100_2, mins_1000_2, mins_2000_2):
    deltas_10, deltas_100, deltas_1000, deltas_2000 = {}, {}, {}, {}
    for test in mins_10:
        if not test in mins_100 or not test in mins_1000 or not test in mins_2000 or \
            not test in mins_10_2 or not test in mins_100_2 or not test in mins_1000_2 or not test in mins_2000_2:
            continue
        deltas_10[test] = []
        deltas_100[test] = []
        deltas_1000[test] = []
        deltas_2000[test] = []
        for i in range(0, len(mins_10[test])):
            deltas_10[test].append(mins_10_2[test][i] - mins_10[test][i])
            deltas_100[test].append(mins_100_2[test][i] - mins_100[test][i])
            deltas_1000[test].append(mins_1000_2[test][i] - mins_1000[test][i])
            deltas_2000[test].append(mins_2000_2[test][i] - mins_2000[test][i])
    return deltas_10, deltas_100, deltas_1000, deltas_2000

def compute_mean_stdev_variance_and_deviations_per_test(data):
    mean = sum(data) / len(data)
    deviations = [ (x - mean) ** 2 for x in data ]
    variance = sum(deviations) / len(deviations)
    stddev = math.sqrt(variance)
    return mean, stddev, variance, deviations

def compute_mean_stdev_variance_and_deviations(data):
    mean, stddev, variance, deviations = {}, {}, {}, {}
    for test in data:
        mean[test], stddev[test], variance[test], deviations[test] = compute_mean_stdev_variance_and_deviations_per_test(data[test])
    return mean, stddev, variance, deviations

if __name__ == '__main__':
    path_to_data_folder = 'data/output/sumup'
    
    data_mvn_10, total_10 = read_json_iteration('_'.join([path_to_data_folder, 'mvn', '10']), factor=10)
    data_mvn_100, total_100 = read_json_iteration('_'.join([path_to_data_folder, 'mvn', '100']), factor=100)
    data_mvn_1000, total_1000 = read_json_iteration('_'.join([path_to_data_folder, 'mvn', '1000']), factor=1000)
    data_mvn_2000, total_2000 = read_json_iteration('_'.join([path_to_data_folder, 'mvn', '2000']), factor=2000)

    data_mvn_10_2, total_10_2 = read_json_iteration('_'.join([path_to_data_folder, 'mvn', '10', '2']), factor=10)
    data_mvn_100_2, total_100_2 = read_json_iteration('_'.join([path_to_data_folder, 'mvn', '100', '2']), factor=100)
    data_mvn_1000_2, total_1000_2 = read_json_iteration('_'.join([path_to_data_folder, 'mvn', '1000', '2']), factor=1000)
    data_mvn_2000_2, total_2000_2 = read_json_iteration('_'.join([path_to_data_folder, 'mvn', '2000', '2']), factor=2000)

    mins_10, mins_100, mins_1000, mins_2000 = compute_mins(data_mvn_10, data_mvn_100, data_mvn_1000, data_mvn_2000)
    mins_10_2, mins_100_2, mins_1000_2, mins_2000_2 = compute_mins(data_mvn_10_2, data_mvn_100_2, data_mvn_1000_2, data_mvn_2000_2)
    deltas_10, deltas_100, deltas_1000, deltas_2000 = compute_deltas(mins_10, mins_100, mins_1000, mins_2000, mins_10_2, mins_100_2, mins_1000_2, mins_2000_2)

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
    #axes[0].violinplot(to_array_for_violin(deltas_10))
    #axes[0].violinplot(to_array_for_violin(deltas_100))
    axes[0].violinplot(to_array_for_violin(deltas_1000))
    axes[0].violinplot(to_array_for_violin(deltas_2000))

    mean_10, stddev_10, variance_10, deviations_10 = compute_mean_stdev_variance_and_deviations(deltas_10)
    mean_100, stddev_100, variance_100, deviations_100 = compute_mean_stdev_variance_and_deviations(deltas_100)
    mean_1000, stddev_1000, variance_1000, deviations_1000 = compute_mean_stdev_variance_and_deviations(deltas_1000)
    mean_2000, stddev_2000, variance_2000, deviations_2000 = compute_mean_stdev_variance_and_deviations(deltas_2000)

    medianes_10, medianes_100, medianes_1000, medianes_2000 = compute_medianes(data_mvn_10, data_mvn_100, data_mvn_1000, data_mvn_2000)
    medianes_10_2, medianes_100_2, medianes_1000_2, medianes_2000_2 = compute_medianes(data_mvn_10_2, data_mvn_100_2, data_mvn_1000_2, data_mvn_2000_2)
    deltas_10, deltas_100, deltas_1000, deltas_2000 = compute_deltas(medianes_10, medianes_100, medianes_1000, medianes_2000,medianes_10_2, medianes_100_2, medianes_1000_2, medianes_2000_2)

    #axes[1].violinplot(to_array_for_violin(deltas_10))
    #axes[1].violinplot(to_array_for_violin(deltas_100))
    axes[1].violinplot(to_array_for_violin(deltas_1000))
    axes[1].violinplot(to_array_for_violin(deltas_2000))

    plt.xticks(range(0, len(deltas_2000)))
    plt.tight_layout()
    plt.savefig('sumup_delta/distribution_min_vs_med.png')
    plt.clf()

    cv = [[], [], [], []]
    for test in mean_10:
        cv[0].append(stddev_10[test] / mean_10[test])
        cv[1].append(stddev_100[test] / mean_100[test])
        cv[2].append(stddev_1000[test] / mean_1000[test])
        cv[3].append(stddev_2000[test] / mean_2000[test])
    plt.plot(cv[0], 'o', color='blue')
    plt.plot(cv[1], 'o', color='orange')
    plt.plot(cv[2], 'o', color='green')
    plt.plot(cv[3], 'o', color='red')

    mean_10, stddev_10, variance_10, deviations_10 = compute_mean_stdev_variance_and_deviations(deltas_10)
    mean_100, stddev_100, variance_100, deviations_100 = compute_mean_stdev_variance_and_deviations(deltas_100)
    mean_1000, stddev_1000, variance_1000, deviations_1000 = compute_mean_stdev_variance_and_deviations(deltas_1000)
    mean_2000, stddev_2000, variance_2000, deviations_2000 = compute_mean_stdev_variance_and_deviations(deltas_2000)

    cv = [[], [], [], []]
    for test in mean_10:
        cv[0].append(stddev_10[test] / mean_10[test])
        cv[1].append(stddev_100[test] / mean_100[test])
        cv[2].append(stddev_1000[test] / mean_1000[test])
        cv[3].append(stddev_2000[test] / mean_2000[test])
    plt.plot(cv[0], 'x', color='blue')
    plt.plot(cv[1], 'x', color='orange')
    plt.plot(cv[2], 'x', color='green')
    plt.plot(cv[3], 'x', color='red')

    plt.xticks(range(0, len(deltas_2000)))
    plt.tight_layout()
    plt.savefig('sumup_delta/cv.png')
    plt.clf()
