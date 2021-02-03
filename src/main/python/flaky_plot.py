from utils.json_utils import *

import os

import matplotlib.pyplot as plt
import numpy as np

def to_array_for_violin(data):
    array = []
    for key in data:
        array.append(np.array(data[key]))
    return array

def to_test_name(json_file_name):
    return json_file_name[0:len(json_file_name) - len('.json')]

def read_json_iteration(path, data):
    for json_test_file in os.listdir(path):
        data_test_json = read_json(path + '/' + json_test_file)
        test_name = to_test_name(json_test_file)
        if not test_name in data:
            data[test_name] = []
        data[test_name].append(data_test_json['package|uJ'])          

def read_json_version(path, version, data):
    path_to_data = path + '/' + version + '/'
    iteration_directories = sorted(os.listdir(path_to_data), key=lambda x: int(x))
    for iteration_directory in iteration_directories:
        path_iteration = path_to_data + '/' + iteration_directory
        read_json_iteration(path_iteration, data)
    return data

def build_violin_plot(path, version):
    plt.violinplot(to_array_for_violin(read_json_version(path, version, {})),
                    showmeans=False,
                    showmedians=True)

def compute_mediane(sec_test):
    return sorted(sec_test)[int(len(sec_test) / 2)]

def compute_medianes(data, nb_element_per_mediane):
    i = 0
    medianes_per_test = {}
    while i < 10:
        for test in data:
            outbound = max((i+1) * nb_element_per_mediane, len(data[test]))
            current_test_mediane = compute_mediane(data[test][i*nb_element_per_mediane:outbound])
            if not test in medianes_per_test:
                medianes_per_test[test] = []
            medianes_per_test[test].append(current_test_mediane)
        i = i + 1
    return medianes_per_test

def compute_diff_medianes(data_1, data_2):
    mediane_per_test_1 = {}
    mediane_per_test_2 = {}
    for test in data_1:
        mediane_per_test_1[test] = compute_mediane(data_1[test])
        mediane_per_test_2[test] = compute_mediane(data_2[test])
    diff_mediane_per_test = {}
    for test in mediane_per_test_1:
        diff_mediane_per_test[test] = abs(abs(mediane_per_test_1[test]) - abs(mediane_per_test_2[test]))
    return diff_mediane_per_test

def build_violin_for_medianes(data):
    plt.violinplot(to_array_for_violin(compute_medianes(data, 10)),
                    showmeans=False,
                    showmedians=True)

def first_half(d):
    return dict(list(d.items())[len(d)//2:])

def second_half(d):
    return dict(list(d.items())[:len(d)//2])

if __name__ == '__main__':

    path_to_gson_flaky = 'data/output/gson_flaky/794_d26c81_364de8_'

    build_violin_plot(path_to_gson_flaky + 'not_flaky_1', 'v1')
    build_violin_plot(path_to_gson_flaky + 'not_flaky_2', 'v1')
    build_violin_plot(path_to_gson_flaky + 'flaky_1', 'v1')
    build_violin_plot(path_to_gson_flaky + 'flaky_2', 'v1')
    build_violin_plot(path_to_gson_flaky + 'not_flaky_1000_1', 'v1')
    build_violin_plot(path_to_gson_flaky + 'not_flaky_1000_2', 'v1')
    build_violin_plot(path_to_gson_flaky + 'flaky_1000_1', 'v1')
    build_violin_plot(path_to_gson_flaky + 'flaky_1000_2', 'v1')
    plt.tight_layout()
    plt.savefig('all.png')
    plt.clf()

    data_not_flaky = read_json_version(path_to_gson_flaky + 'not_flaky_1', 'v1', {})
    data_not_flaky = read_json_version(path_to_gson_flaky + 'not_flaky_2', 'v1', data_not_flaky)
    data_flaky = read_json_version(path_to_gson_flaky + 'flaky_1', 'v1', {})
    data_flaky = read_json_version(path_to_gson_flaky + 'flaky_2', 'v1', data_flaky)

    data_not_flaky_1000 = read_json_version(path_to_gson_flaky + 'not_flaky_1000_1', 'v1', {})
    data_not_flaky_1000 = read_json_version(path_to_gson_flaky + 'not_flaky_1000_2', 'v1', data_not_flaky_1000)
    data_flaky_1000 = read_json_version(path_to_gson_flaky + 'flaky_1000_1', 'v1', {})
    data_flaky_1000 = read_json_version(path_to_gson_flaky + 'flaky_1000_2', 'v1', data_flaky_1000)
    
    plt.violinplot(to_array_for_violin(data_not_flaky))
    plt.violinplot(to_array_for_violin(data_flaky))
    plt.violinplot(to_array_for_violin(data_not_flaky_1000))
    plt.violinplot(to_array_for_violin(data_flaky_1000))
    plt.tight_layout()
    plt.savefig('sec.png')
    plt.clf()

    build_violin_for_medianes(data_not_flaky)
    build_violin_for_medianes(data_flaky)

    plt.tight_layout()
    plt.savefig('violin_medianes.png')
    plt.clf()

    diff_medianes_not_flaky = compute_diff_medianes(
        read_json_version(path_to_gson_flaky + 'not_flaky_1', 'v1', {}),
        read_json_version(path_to_gson_flaky + 'not_flaky_2', 'v1', {})
    )
    plt.plot(to_array_for_violin(diff_medianes_not_flaky))    
    diff_medianes_flaky = compute_diff_medianes(
        read_json_version(path_to_gson_flaky + 'flaky_1', 'v1', {}),
        read_json_version(path_to_gson_flaky + 'flaky_2', 'v1', {})
    )
    plt.plot(to_array_for_violin(diff_medianes_flaky))    

    plt.tight_layout()
    plt.savefig('diff_medianes.png')
    plt.clf()

   
