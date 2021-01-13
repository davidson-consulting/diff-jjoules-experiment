import sys
import os
import math

from utils.data_args import *
from utils.json_utils import *

def get_class_name(json_file):
    return json_file.split('.json')[0]

def compute_energy_for_tests(path_to_folder_iteration):
    compute_energy_for_tests = {}
    for json_file in os.listdir(path_to_folder_iteration):
        print(path_to_folder_iteration + '/' + json_file)
        key = get_class_name(json_file)
        data = get_energy_data(read_json(path_to_folder_iteration + '/' + json_file))
        if len(data) > 0:
            compute_energy_for_tests[key] = data
        #else:
        #    print(path_to_folder_iteration + '/' + json_file, 'not added')
    return compute_energy_for_tests

def compute_avg_energy_for_iterations(path_to_data_version):
    iteration_folders = os.listdir(path_to_data_version)
    if len(iteration_folders) == 0:
        print('No iteration folders found in ', path_to_data_version)
        return {}
    energies_per_test = {}
    duration_per_test = {}
    dram_per_test = {}
    nb_validated_iteration_per_test = {}
    for iteration_folder in iteration_folders[1:]:
        current_avg_energy_per_test = compute_energy_for_tests(path_to_data_version + '/' + iteration_folder)
        for test in current_avg_energy_per_test:
            if len(current_avg_energy_per_test[test]) > 0:
                if test in nb_validated_iteration_per_test:
                    nb_validated_iteration_per_test[test] = nb_validated_iteration_per_test[test] + 1
                else:
                    nb_validated_iteration_per_test[test] = 1
                if not test in energies_per_test:
                    energies_per_test[test] = [current_avg_energy_per_test[test]['energy']]
                    duration_per_test[test] = [current_avg_energy_per_test[test]['duration']]
                    dram_per_test[test] = [current_avg_energy_per_test[test]['dram']]
                else:
                    energies_per_test[test].append(current_avg_energy_per_test[test]['energy'])
                    duration_per_test[test].append(current_avg_energy_per_test[test]['duration'])
                    dram_per_test[test].append(current_avg_energy_per_test[test]['dram'])
    data_per_test = {}
    
    for test in energies_per_test:
        mean_energy = sum(energies_per_test[test]) / len(energies_per_test[test])
        mean_duration = sum(duration_per_test[test]) / len(duration_per_test[test])
        mean_dram = sum(dram_per_test[test]) / len(duration_per_test[test])
        deviations = [ (x - mean_energy) ** 2 for x in energies_per_test[test] ]
        variance = sum(deviations) / len(deviations)
        stdev = math.sqrt(variance)
        median_energy = sorted(energies_per_test[test])[int(len(energies_per_test[test])  / 2)]
        #print(test)
        #for energy_test in energies_per_test[test]:
            #print(energy_test)
        #print(mean_energy, stdev)
        data_per_test[test] = {}
        data_per_test[test]['energy'] = median_energy
        data_per_test[test]['duration'] = mean_duration
        data_per_test[test]['dram'] = mean_dram
        data_per_test[test]['iteration'] = nb_validated_iteration_per_test[test]
        data_per_test[test]['stdev'] = stdev
        #sys.exit(-1)

    return data_per_test

def compute_avg_energy_for_commit(path_to_data_commit):
    path_v1 = path_to_data_commit + '/v1/'
    path_v2 = path_to_data_commit + '/v2/'
    data_v1 = compute_avg_energy_for_iterations(path_v1)
    data_v2 = compute_avg_energy_for_iterations(path_v2)
    return data_v1, data_v2

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()
    project_name = args.project_name
    path_to_data = args.data_path

    path_to_commit_folders = path_to_data + '/' + project_name + '/'
    files = os.listdir(path_to_commit_folders)
    for file in files:
        path_to_file = path_to_commit_folders + file
        print(file, files.index(file), '/', len(files))
        if os.path.isfile(path_to_file + '/data_v1.json') and os.path.isfile(path_to_file + '/data_v2.json'):
            continue
        if os.path.isdir(path_to_file):
            data_v1, data_v2 = compute_avg_energy_for_commit(path_to_file)
            write_json(path_to_file + '/data_v1.json', data_v1)
            write_json(path_to_file + '/data_v2.json', data_v2)
