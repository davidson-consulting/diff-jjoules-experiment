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
    for iteration_directory in os.listdir(path)[0:100]:
        current_energy_for_all = 0
        for json_test_file in os.listdir(path + '/' + iteration_directory)[0:20]:
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

def build_violin_plot_java_vs_maven(java_arrays, mvn_arrays):
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(9, 4))
    for i in range(len(java_arrays)):
        axes[i].violinplot(to_array_for_violin_with_key(java_arrays[i], 'energy'), showmeans=False, showmedians=True,  showextrema=False,)
        axes[i].violinplot(to_array_for_violin_with_key(mvn_arrays[i], 'energy'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.tight_layout()
    plt.savefig('sumup/java_vs_mvm.png')
    plt.clf()

    for i in range(len(java_arrays)):
        plt.violinplot(to_array_for_violin_with_key(java_arrays[i], 'energy'), showmeans=False, showmedians=True,  showextrema=False,)
        plt.violinplot(to_array_for_violin_with_key(mvn_arrays[i], 'energy'), showmeans=False, showmedians=True,  showextrema=False,)
        plt.tight_layout()
        plt.savefig('sumup/java_vs_mvm_' + str(i) + '.png')
        plt.clf()

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

def build_plot_diff_medianes(datas, prefix):
    for data in datas:
        diff_medianes = []
        medianes = compute_medianes(data, int(len(data) / 2), 'energy')
        for test in data:
            diff_medianes.append(abs(medianes[test][0] - medianes[test][1]))
        plt.plot(diff_medianes, 'o')
    plt.tight_layout()
    plt.savefig('sumup/'+ prefix + '_diff_medianes.png')
    plt.clf()

def build_violin_plot_separated(data_mvn_10, data_mvn_100, data_mvn_1000, data_mvn_2000, key):
    fig, axes = plt.subplots(nrows=2, ncols=2)
    axes[0][0].violinplot(to_array_for_violin_with_key(data_mvn_10, key), showmeans=False, showmedians=True,  showextrema=False,)
    axes[0][0].set_title('10 Duplications')
    axes[0][1].violinplot(to_array_for_violin_with_key(data_mvn_100, key), showmeans=False, showmedians=True,  showextrema=False,)
    axes[0][1].set_title('100 Duplications')
    axes[1][0].violinplot(to_array_for_violin_with_key(data_mvn_1000, key), showmeans=False, showmedians=True,  showextrema=False,)
    axes[1][0].set_title('1000 Duplications')
    axes[1][1].violinplot(to_array_for_violin_with_key(data_mvn_2000, key), showmeans=False, showmedians=True,  showextrema=False,)
    axes[1][1].set_title('2000 Duplications')
    plt.tight_layout()
    plt.savefig('sumup/separated_' + key + '.png')
    plt.clf()

    plt.violinplot(to_array_for_violin_with_key(data_mvn_10, key), showmeans=False, showmedians=True,  showextrema=False,)
    plt.tight_layout()
    plt.savefig('sumup/mvn_10_' + key + '.png')
    plt.clf()
    plt.violinplot(to_array_for_violin_with_key(data_mvn_100, key), showmeans=False, showmedians=True,  showextrema=False,)
    plt.tight_layout()
    plt.savefig('sumup/mvn_100_' + key + '.png')
    plt.clf()
    plt.violinplot(to_array_for_violin_with_key(data_mvn_1000, key), showmeans=False, showmedians=True,  showextrema=False,)
    plt.tight_layout()
    plt.savefig('sumup/mvn_1000_' + key + '.png')
    plt.clf()
    plt.violinplot(to_array_for_violin_with_key(data_mvn_2000, key), showmeans=False, showmedians=True,  showextrema=False,)
    plt.tight_layout()
    plt.savefig('sumup/mvn_2000_' + key + '.png')
    plt.clf()

def inner_plot_with_key(data, key):
    data_to_plot = []
    for test in data:
        data_to_plot.append(data[test][key])
    plt.plot(data_to_plot)
    plt.fill_between(range(0, len(data)), data_to_plot)

def build_plot_cv(data_mvn_10, data_mvn_100, data_mvn_1000, data_mvn_2000):
    inner_plot_with_key(data_mvn_10, 'cv')
    inner_plot_with_key(data_mvn_100, 'cv')
    inner_plot_with_key(data_mvn_1000, 'cv')
    inner_plot_with_key(data_mvn_2000, 'cv')
    plt.tight_layout()
    plt.savefig('sumup/cv.png')
    plt.clf()

def build_plot_qcd(data_mvn_10, data_mvn_100, data_mvn_1000, data_mvn_2000):
    inner_plot_with_key(data_mvn_10, 'qcd')
    inner_plot_with_key(data_mvn_100, 'qcd')
    inner_plot_with_key(data_mvn_1000, 'qcd')
    inner_plot_with_key(data_mvn_2000, 'qcd')
    plt.tight_layout()
    plt.savefig('sumup/qcd.png')
    plt.clf()

def inner_plot_min_duration(data):
    data_to_plot = []
    duration_to_plot = []
    for test in data:
        sorted_data = sorted(data[test]['energy'])
        data_to_plot.append(sorted_data[0] / 1E3)
        index_min_energy = data[test]['energy'].index(sorted_data[0])
        duration_min_energy = data[test]['duration'][index_min_energy] / 1E6
        duration_to_plot.append(duration_min_energy)
    print(data_to_plot, duration_to_plot)
    return data_to_plot, duration_to_plot

def build_plot_mini(data_mvn_10, data_mvn_100, data_mvn_1000, data_mvn_2000, suffix=''):
    data_to_plot, duration_to_plot = inner_plot_min_duration(data_mvn_10)
    plt.plot(data_to_plot, 'o', color='blue')
    plt.plot(duration_to_plot, 'x', color='blue')
    data_to_plot, duration_to_plot = inner_plot_min_duration(data_mvn_100)
    plt.plot(data_to_plot, 'o', color='orange')
    plt.plot(duration_to_plot, 'x', color='orange')
    data_to_plot, duration_to_plot = inner_plot_min_duration(data_mvn_1000)
    plt.plot(data_to_plot, 'o', color='green')
    plt.plot(duration_to_plot, 'x', color='green')
    data_to_plot, duration_to_plot = inner_plot_min_duration(data_mvn_2000)
    plt.plot(data_to_plot, 'o', color='red')
    plt.plot(duration_to_plot, 'x', color='red')

    plt.xticks(range(0, len(data_mvn_2000)))
    plt.tight_layout()
    plt.savefig('sumup/min_energy_duration' + suffix + '.png')
    plt.clf()

def inner_plot_mini(data):
    data_to_plot = []
    for test in data:
        sorted_data = sorted(data[test]['energy'])
        data_to_plot.append(sorted_data[0])
    plt.violinplot(data_to_plot, showmeans=False, showmedians=True,  showextrema=False)

def inner_plot_mini_color(data):
    data_to_plot = []
    for test in data:
        sorted_data = sorted(data[test]['energy'])
        data_to_plot.append(sorted_data[0])
    return plt.violinplot(data_to_plot, showmeans=False, showmedians=True,  showextrema=False)

def inner_plot_line_mini(data):
    data_to_plot = []
    for test in data:
        sorted_data = sorted(data[test]['energy'])
        data_to_plot.append(sorted_data[0])
    plt.plot(data_to_plot, 'o')

def get_duration_of_min_energy(data):
    min_duration_per_test = [0]
    for test in data:
        sorted_data = sorted(data[test]['energy'])
        min_energy = sorted_data[0]
        index_min_energy = data[test]['energy'].index(min_energy)
        duration_of_min_energy = data[test]['duration'][index_min_energy]
        min_duration_per_test.append(duration_of_min_energy)
    return min_duration_per_test

def build_violin_plot_min_duration_among_durations(data_mvn_10, data_mvn_100, data_mvn_1000, data_mvn_2000):
    min_durations = get_duration_of_min_energy(data_mvn_10)
    plt.plot(min_durations, 'o', color='blue')
    plt.violinplot(to_array_for_violin_with_key(data_mvn_10, 'duration'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.xticks(range(1, len(data_mvn_10)))
    plt.tight_layout()
    plt.savefig('sumup/duration_of_min_10.png')
    plt.clf()

    min_durations = get_duration_of_min_energy(data_mvn_100)
    plt.plot(min_durations, 'o', color='red')
    plt.violinplot(to_array_for_violin_with_key(data_mvn_100, 'duration'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.xticks(range(1, len(data_mvn_100)))
    plt.tight_layout()
    plt.savefig('sumup/duration_of_min_100.png')
    plt.clf()


def build_plot_mini_aggregate(data_mvn_10, data_mvn_100, data_mvn_1000, data_mvn_2000, suffix=''):
    inner_plot_mini(data_mvn_10)
    inner_plot_mini(data_mvn_100)
    inner_plot_mini(data_mvn_1000)
    inner_plot_mini(data_mvn_2000)
    plt.tight_layout()
    plt.savefig('sumup/aggreate_min' + suffix + '.png')
    plt.clf()

    inner_plot_line_mini(data_mvn_10)
    inner_plot_line_mini(data_mvn_100)
    inner_plot_line_mini(data_mvn_1000)
    inner_plot_line_mini(data_mvn_2000)
    plt.xticks(range(0, len(data_mvn_2000)))
    plt.tight_layout()
    plt.savefig('sumup/plot_min' + suffix + '.png')
    plt.clf()

    data_to_plot = [[]]
    for test in data_mvn_10:
        sorted_data = sorted(data_mvn_10[test]['energy'])
        data_to_plot[0].append(sorted_data[0])
    plt.violinplot(data_to_plot, showmeans=False, showmedians=True,  showextrema=False)
    
    data_to_plot = [[0], []]
    for test in data_mvn_100:
        sorted_data = sorted(data_mvn_100[test]['energy'])
        data_to_plot[1].append(sorted_data[0])
    plt.violinplot(data_to_plot, showmeans=False, showmedians=True,  showextrema=False)

    data_to_plot = [[0], [0], []]
    for test in data_mvn_1000:
        sorted_data = sorted(data_mvn_1000[test]['energy'])
        data_to_plot[2].append(sorted_data[0])
    plt.violinplot(data_to_plot, showmeans=False, showmedians=True,  showextrema=False)

    data_to_plot = [[0], [0], [0], []]
    for test in data_mvn_2000:
        sorted_data = sorted(data_mvn_2000[test]['energy'])
        data_to_plot[3].append(sorted_data[0])    
    plt.violinplot(data_to_plot, showmeans=False, showmedians=True,  showextrema=False)

    plt.tight_layout()
    plt.savefig('sumup/all_in_one_aggreate_min' + suffix + '.png')
    plt.clf()

import sys

if __name__ == '__main__':
    
    path_to_data_folder = 'data/output/sumup'

    data_mvn_10, total_10 = read_json_iteration('_'.join([path_to_data_folder, 'mvn', '10']))
    data_mvn_100, total_100 = read_json_iteration('_'.join([path_to_data_folder, 'mvn', '100']))
    data_mvn_1000, total_1000 = read_json_iteration('_'.join([path_to_data_folder, 'mvn', '1000']))
    data_mvn_2000, total_2000 = read_json_iteration('_'.join([path_to_data_folder, 'mvn', '2000']))

    medianes_mvn_10 = compute_medianes(data_mvn_10, 50, 'energy')
    medianes_mvn_100 = compute_medianes(data_mvn_100, 50, 'energy')
    medianes_mvn_1000 = compute_medianes(data_mvn_1000, 50, 'energy')
    medianes_mvn_2000 = compute_medianes(data_mvn_2000, 10, 'energy')
    
    build_plot_diff_medianes([data_mvn_10, data_mvn_100, data_mvn_1000, data_mvn_2000], 'mvn')
    #build_violin_plot_min_duration_among_durations(data_mvn_10, data_mvn_100, data_mvn_1000, data_mvn_2000)
  
    build_plot_cv(data_mvn_10, data_mvn_100, data_mvn_1000, data_mvn_2000)
    build_plot_qcd(data_mvn_10, data_mvn_100, data_mvn_1000, data_mvn_2000)
    build_plot_mini(data_mvn_10, data_mvn_100, data_mvn_1000, data_mvn_2000)

    build_violin_plot_separated(data_mvn_10, data_mvn_100, data_mvn_1000, data_mvn_2000, 'energy')
    build_violin_plot_separated(data_mvn_10, data_mvn_100, data_mvn_1000, data_mvn_2000, 'duration')
    build_violin_plot_separated(data_mvn_10, data_mvn_100, data_mvn_1000, data_mvn_2000, 'power')
    
    plt.violinplot(to_array_for_violin(medianes_mvn_10), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin(medianes_mvn_100), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin(medianes_mvn_1000), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin(medianes_mvn_2000), showmeans=False, showmedians=True,  showextrema=False,)
    plt.tight_layout()
    plt.savefig('sumup/medianes.png')
    plt.clf()

    plt.violinplot(to_array_for_violin_with_key(data_mvn_10, 'energy'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin_with_key(data_mvn_100, 'energy'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin_with_key(data_mvn_1000, 'energy'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin_with_key(data_mvn_2000, 'energy'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.tight_layout()
    plt.savefig('sumup/energy.png')
    plt.clf()

    plt.violinplot(to_array_for_violin_with_key(data_mvn_10, 'power'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin_with_key(data_mvn_100, 'power'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin_with_key(data_mvn_1000, 'power'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin_with_key(data_mvn_2000, 'power'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.tight_layout()
    plt.savefig('sumup/power.png')
    plt.clf()

    plt.violinplot(to_array_for_violin_with_key(data_mvn_10, 'duration'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin_with_key(data_mvn_100, 'duration'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin_with_key(data_mvn_1000, 'duration'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin_with_key(data_mvn_2000, 'duration'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.tight_layout()
    plt.savefig('sumup/duration.png')
    plt.clf()

    data_mvn_10_n, total_10_n = read_json_iteration('_'.join([path_to_data_folder, 'mvn', '10']), 10)
    data_mvn_100_n, total_100_n = read_json_iteration('_'.join([path_to_data_folder, 'mvn', '100']), 100)
    data_mvn_1000_n, total_1000_n = read_json_iteration('_'.join([path_to_data_folder, 'mvn', '1000']), 1000)
    data_mvn_2000_n, total_2000_n = read_json_iteration('_'.join([path_to_data_folder, 'mvn', '2000']), 2000)
    
    build_plot_mini(data_mvn_10_n, data_mvn_100_n, data_mvn_1000_n, data_mvn_2000_n, '_n')
    build_plot_mini_aggregate(data_mvn_10, data_mvn_100, data_mvn_1000, data_mvn_2000)
    build_plot_mini_aggregate(data_mvn_10_n, data_mvn_100_n, data_mvn_1000_n, data_mvn_2000_n, '_n')

    plt.boxplot(total_10)
    plt.boxplot(total_100)
    plt.boxplot(total_1000)
    plt.boxplot(total_2000)
    plt.tight_layout()
    plt.savefig('sumup/total.png')
    plt.clf()

    plt.boxplot(total_10_n)
    plt.boxplot(total_100_n)
    plt.boxplot(total_1000_n)
    plt.boxplot(total_2000_n)
    plt.tight_layout()
    plt.savefig('sumup/total_n.png')
    plt.clf()

    '''
    medianes_mvn_10_n = compute_medianes(data_mvn_10_n, 50, 'energy')
    medianes_mvn_100_n = compute_medianes(data_mvn_100_n, 50, 'energy')
    medianes_mvn_1000_n = compute_medianes(data_mvn_1000_n, 50, 'energy')
    medianes_mvn_2000_n = compute_medianes(data_mvn_1000_n, 10, 'energy')

    build_plot_diff_medianes([data_mvn_10_n, data_mvn_100_n, data_mvn_1000_n, data_mvn_2000_n], 'mvn_n')

    plt.violinplot(to_array_for_violin_with_key(data_mvn_10_n, 'energy'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin_with_key(data_mvn_100_n, 'energy'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin_with_key(data_mvn_1000_n, 'energy'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin_with_key(data_mvn_2000_n, 'energy'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.tight_layout()
    plt.savefig('sumup/energy_n.png')
    plt.clf()

    plt.violinplot(to_array_for_violin_with_key(data_mvn_10_n, 'duration'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin_with_key(data_mvn_100_n, 'duration'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin_with_key(data_mvn_1000_n, 'duration'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin_with_key(data_mvn_2000_n, 'duration'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.tight_layout()
    plt.savefig('sumup/duration_n.png')
    plt.clf()

    plt.violinplot(to_array_for_violin_with_key(data_mvn_10_n, 'power'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin_with_key(data_mvn_100_n, 'power'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin_with_key(data_mvn_1000_n, 'power'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin_with_key(data_mvn_2000_n, 'power'), showmeans=False, showmedians=True,  showextrema=False,)
    plt.tight_layout()
    plt.savefig('sumup/power_n.png')
    plt.clf()

    plt.violinplot(to_array_for_violin(medianes_mvn_10_n), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin(medianes_mvn_100_n), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin(medianes_mvn_1000_n), showmeans=False, showmedians=True,  showextrema=False,)
    plt.violinplot(to_array_for_violin(medianes_mvn_2000_n), showmeans=False, showmedians=True,  showextrema=False,)
    plt.tight_layout()
    plt.savefig('sumup/medianes_n.png')
    plt.clf()
    '''