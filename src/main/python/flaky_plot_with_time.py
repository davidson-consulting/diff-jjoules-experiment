from utils.json_utils import *

import os

import matplotlib.pyplot as plt
import numpy as np

def to_array_for_violin(data):
    array = []
    for key in data:
        array.append(np.array(data[key]))
    return array

def to_array_for_violin_dimension(data, dimension):
    array = []
    for key in data:
        array.append(np.array(data[key][dimension])*1E-9)
    return array

def to_test_name(json_file_name):
    return json_file_name[0:len(json_file_name) - len('.json')]

def read_json_iteration(path, data):
    for json_test_file in os.listdir(path):
        data_test_json = read_json(path + '/' + json_test_file)
        test_name = to_test_name(json_test_file)
        if not test_name in data:
            data[test_name] = {}
            data[test_name]['energy'] = []
            data[test_name]['time'] = []
        data[test_name]['energy'].append(data_test_json['package|uJ'])
        data[test_name]['time'].append(data_test_json['duration|ns'])

def read_json_version(path, version, data):
    path_to_data = path + '/' + version + '/'
    iteration_directories = sorted(os.listdir(path_to_data), key=lambda x: int(x))
    for iteration_directory in iteration_directories:
        path_iteration = path_to_data + '/' + iteration_directory
        read_json_iteration(path_iteration, data)
    return data

def build_violin_plot(data):
    plt.violinplot(to_array_for_violin(data),
                    showmeans=False,
                    showmedians=True)

def build_ratio(data):
    ratio_time_energy_per_test = {}
    for test in data:
        data_test = data[test]
        ratio_time_energy_per_test[test] = []
        for i in range(len(data_test['energy'])):
            ratio = data_test['energy'][i] / data_test['time'][i]
            ratio_time_energy_per_test[test].append(ratio)
    return ratio_time_energy_per_test

if __name__ == '__main__':

    path_to_gson_flaky = 'data/output/gson_flaky/794_d26c81_364de8_'

    data_not_flaky = read_json_version(path_to_gson_flaky + 'not_flaky_1', 'v1', {})
    data_not_flaky = read_json_version(path_to_gson_flaky + 'not_flaky_2', 'v1', data_not_flaky)

    data_flaky = read_json_version(path_to_gson_flaky + 'flaky_1', 'v1', {})
    data_flaky = read_json_version(path_to_gson_flaky + 'flaky_2', 'v1', data_flaky)

    data_flaky_1000 = read_json_version(path_to_gson_flaky + 'flaky_1000_1', 'v1', {})
    data_flaky_1000 = read_json_version(path_to_gson_flaky + 'flaky_1000_2', 'v1', data_flaky_1000)
    data_not_flaky_1000 = read_json_version(path_to_gson_flaky + 'not_flaky_1000_1', 'v1', {})
    data_not_flaky_1000 = read_json_version(path_to_gson_flaky + 'not_flaky_1000_2', 'v1', data_not_flaky_1000)

    ratio_time_energy_per_test_not_flaky = build_ratio(data_not_flaky)
    ratio_time_energy_per_test_flaky = build_ratio(data_flaky)
    ratio_time_energy_per_test_flaky_1000 = build_ratio(data_flaky_1000)
    ratio_time_energy_per_test_not_flaky_1000 = build_ratio(data_not_flaky_1000)
    
    build_violin_plot(ratio_time_energy_per_test_not_flaky)
    build_violin_plot(ratio_time_energy_per_test_flaky)
    build_violin_plot(ratio_time_energy_per_test_not_flaky_1000)
    build_violin_plot(ratio_time_energy_per_test_flaky_1000)

    plt.tight_layout()
    plt.savefig('ratio.png')
    plt.clf()

    plt.violinplot(to_array_for_violin_dimension(data_flaky, 'time'),
                    showmeans=False,
                    showmedians=True)
    plt.violinplot(to_array_for_violin_dimension(data_not_flaky, 'time'),
                    showmeans=False,
                    showmedians=True)
    plt.violinplot(to_array_for_violin_dimension(data_flaky_1000, 'time'),
                    showmeans=False,
                    showmedians=True)
    plt.violinplot(to_array_for_violin_dimension(data_not_flaky_1000, 'time'),
                    showmeans=False,
                    showmedians=True)

    plt.tight_layout()
    plt.savefig('times.png')
    plt.clf()