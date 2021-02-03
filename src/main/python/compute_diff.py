from utils.json_utils import *

import os

import matplotlib.pyplot as plt
import numpy as np

def to_test_name(json_file_name):
    return json_file_name[0:len(json_file_name) - len('.json')]

def read_json_iteration(path, data, factor):
    for json_test_file in os.listdir(path):
        data_test_json = read_json(path + '/' + json_test_file)
        test_name = to_test_name(json_test_file)
        if not test_name in data:
            data[test_name] = []
        data[test_name].append(data_test_json['package|uJ'] / factor)

def read_json_version(path, data, factor):
    path_to_data = path + '/v1/'
    iteration_directories = sorted(os.listdir(path_to_data), key=lambda x: int(x))
    for iteration_directory in iteration_directories:
        path_iteration = path_to_data + '/' + iteration_directory
        read_json_iteration(path_iteration, data, factor)
    return data

def compute_mediane(sec_test):
    return sorted(sec_test)[int(len(sec_test) / 2)]

def compute_medianes(data):
    mediane_per_test = {}
    for test in data:
        mediane_per_test[test] = compute_mediane(data[test])
    return mediane_per_test

if __name__ == '__main__':

    path_to_gson_flaky = 'data/output/gson_flaky/794_d26c81_364de8_'

    data_flaky_100_1 = read_json_version(path_to_gson_flaky + 'flaky_1', {}, 100)
    data_flaky_100_2 = read_json_version(path_to_gson_flaky + 'flaky_2', {}, 100)
    not_data_flaky_100_1 = read_json_version(path_to_gson_flaky + 'not_flaky_1', {}, 100)
    not_data_flaky_100_2 = read_json_version(path_to_gson_flaky + 'not_flaky_2', {}, 100)

    medianes_flaky_100_1 = compute_medianes(data_flaky_100_1)
    medianes_flaky_100_2 = compute_medianes(data_flaky_100_2)
    medianes_not_flaky_100_1 = compute_medianes(not_data_flaky_100_1)
    medianes_not_flaky_100_2 = compute_medianes(not_data_flaky_100_2)

    diff_flaky_100 = []
    for test in medianes_flaky_100_1:
        diff = abs(abs(medianes_flaky_100_1[test]) - abs(medianes_flaky_100_2[test]))
        diff_flaky_100.append(diff)
    
    diff_not_flaky_100 = []
    for test in medianes_not_flaky_100_1:
        diff = abs(abs(medianes_not_flaky_100_1[test]) - abs(medianes_not_flaky_100_2[test]))
        diff_not_flaky_100.append(diff)

    plt.plot(diff_not_flaky_100)
    plt.plot(diff_flaky_100)

    data_flaky = read_json_version(path_to_gson_flaky + 'flaky_1000_1', {}, 1000)
    data_flaky = read_json_version(path_to_gson_flaky + 'flaky_1000_2', data_flaky, 1000)
    not_data_flaky = read_json_version(path_to_gson_flaky + 'not_flaky_1000_1', {}, 1000)
    not_data_flaky = read_json_version(path_to_gson_flaky + 'not_flaky_1000_2', not_data_flaky, 1000)

    first_half_flaky = {}
    second_half_flaky = {}
    for test in data_flaky:
        first_half_flaky[test] = data_flaky[test][len(data_flaky)//2:]
        second_half_flaky[test] = data_flaky[test][:len(data_flaky)//2]

    first_half_not_flaky = {}
    second_half_not_flaky = {}
    for test in not_data_flaky:
        first_half_not_flaky[test] = not_data_flaky[test][len(not_data_flaky)//2:]
        second_half_not_flaky[test] = not_data_flaky[test][:len(not_data_flaky)//2]

    medianes_first_flaky = compute_medianes(first_half_flaky)
    medianes_second_flaky = compute_medianes(second_half_flaky)
    medianes_first_not_flaky = compute_medianes(first_half_not_flaky)
    medianes_second_not_flaky = compute_medianes(second_half_not_flaky)

    diff_flaky = []
    for test in medianes_first_flaky:
        diff = abs(abs(medianes_first_flaky[test]) - abs(medianes_second_flaky[test]))
        diff_flaky.append(diff)
    
    diff_not_flaky = []
    for test in medianes_first_not_flaky:
        diff = abs(abs(medianes_first_not_flaky[test]) - abs(medianes_second_not_flaky[test]))
        diff_not_flaky.append(diff)

    plt.plot(diff_not_flaky)
    plt.plot(diff_flaky)
    plt.tight_layout()
    plt.savefig('diff_medianes_1000.png')
    plt.clf()