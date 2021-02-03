from utils.json_utils import *

import os

import matplotlib.pyplot as plt
import numpy as np

def to_test_name(json_file_name):
    return json_file_name[0:len(json_file_name) - len('.json')]

def read_json_iteration(path, data):
    for json_test_file in os.listdir(path):
        data_test_json = read_json(path + '/' + json_test_file)
        test_name = to_test_name(json_test_file)
        if not test_name in data:
            data[test_name] = []
        data[test_name].append(data_test_json['package|uJ'] / 100)            

def read_json_version(path, version):
    data = {}
    path_to_data = path + '/' + version + '/'
    iteration_directories = sorted(os.listdir(path_to_data), key=lambda x: int(x))
    for iteration_directory in iteration_directories:
        path_iteration = path_to_data + '/' + iteration_directory
        read_json_iteration(path_iteration, data)
    return data

def compute_delta(data_v1, data_v2):
    delta = {}
    for test_name in data_v1:
        if not test_name in data_v2:
            print('!!!', test_name, 'not in v2')
        delta[test_name] = []
        for i in range(0, len(data_v1[test_name])):
            current_delta = data_v2[test_name][i] - data_v1[test_name][i]
            delta[test_name].append(current_delta)
    return delta

def run(path):
    data_v1 = read_json_version(path, 'v1')
    data_v2 = read_json_version(path, 'v2')
    delta = compute_delta(data_v1, data_v2)
    return data_v1, data_v2, delta

def build_violinboxplot(data_1, name):
    all_data_1 = []
    i = 0
    for key in data_1:
        if i > 10:
            break
        all_data_1.append(np.array(data_1[key]))
        i = i + 1
    plt.violinplot(all_data_1,
                    showmeans=False,
                    showmedians=True)
    plt.tight_layout()
    plt.savefig(name + '.png')
    plt.clf()

def build_violinboxplot_2(data_1, data_2, name):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
    all_data_1 = []
    for key in data_1:
        all_data_1.append(np.array(data_1[key]))
    axes[0].violinplot(all_data_1,
                    showmeans=False,
                    showmedians=True)
    all_data_2 = []
    for key in data_2:
        all_data_2.append(np.array(data_2[key]))
    axes[1].violinplot(all_data_2,
                    showmeans=False,
                    showmedians=True)
    plt.tight_layout()
    plt.savefig(name + '.png')
    plt.clf()

def compute_mediane(sec_test):
    return sorted(sec_test)[int(len(sec_test) / 2)]

def compute_medianes(data):
    mediane_per_test = {}
    for test in data:
        mediane_per_test[test] = compute_mediane(data[test])
    return mediane_per_test

if __name__ == '__main__':
    
    data_v1_1, data_v2_1, delta_1 = run('data/output/february_2021/gson/794_d26c81_364de8')
    data_v1_2, data_v2_2, delta_2 = run('data/output/february_2021/gson/794_d26c81_364de8_2')

    mediane_per_test_v1_1 = compute_medianes(data_v1_1)
    mediane_per_test_v1_2 = compute_medianes(data_v1_2)
    mediane_per_test_v2_1 = compute_medianes(data_v2_1)
    mediane_per_test_v2_2 = compute_medianes(data_v2_2)

    delta_mediane_per_test_1 = {}
    delta_mediane_per_test_2 = {}
    to_plot_1 = []
    to_plot_2 = []
    for test in mediane_per_test_v1_1:
        delta_mediane_per_test_1[test] = mediane_per_test_v2_1[test] - mediane_per_test_v1_1[test]
        to_plot_1.append(delta_mediane_per_test_1[test])
        delta_mediane_per_test_2[test] = mediane_per_test_v2_2[test] - mediane_per_test_v1_2[test]
        to_plot_2.append(delta_mediane_per_test_2[test])
    
    plt.plot(to_plot_1)
    plt.plot(to_plot_2)
    plt.tight_layout()
    plt.savefig('deltas.png')
    plt.clf()

    diff_v1 = []
    diff_v1_m = {}
    diff_v2 = []
    diff_v2_m = {}
    tests = []
    for test in mediane_per_test_v1_1:
        diff_v1.append(mediane_per_test_v1_1[test] - mediane_per_test_v1_2[test])
        diff_v1_m[test] = mediane_per_test_v1_1[test] - mediane_per_test_v1_2[test]
        diff_v2.append(mediane_per_test_v2_1[test] - mediane_per_test_v2_2[test])
        diff_v2_m[test] = mediane_per_test_v2_1[test] - mediane_per_test_v2_2[test]

    sorted_diff_v1 = sorted(diff_v1_m, key=lambda x: int(abs(diff_v1_m[x])))
    for test in sorted_diff_v1:
        print(test, diff_v1_m[test])

    plt.plot(diff_v1)
    plt.tight_layout()
    plt.savefig('diff_v1.png')
    plt.clf()

    plt.plot(diff_v2)
    plt.tight_layout()
    plt.savefig('diff_v2.png')
    plt.clf()