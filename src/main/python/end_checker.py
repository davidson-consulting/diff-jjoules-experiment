import random
import os
import sys

from utils.cmd.json_cmd import *
from utils.cmd.io_cmd import *
from utils.statitics import *
from utils.utils import *
    
def increase_first(nb_first, input_array, offset=0):
    array = [x for x in input_array]
    array.sort()
    for i in range(0, len(input_array)):
        if array[0] == input_array[i]:
            nb_first[i+offset] = nb_first[i+offset] + 1
    return nb_first

def increase_first_for_both(nb_first, cvs, qcds, stddevs):
    nb_first = increase_first(nb_first, cvs)
    nb_first = increase_first(nb_first, qcds, offset=5)
    return increase_first(nb_first, stddevs, offset=10)

def read_data_and_count(json_data_path_file, nb_first, unit):
    data = read_json(json_data_path_file)
    nb_discard = 0
    for fullqualified_test_method_name in data:
        current = []
        nb_discard = 0
        for record in data[fullqualified_test_method_name]:
            if record[unit] != 0:
                current.append(record[unit])
            else:
                nb_discard = nb_discard + 1
        #random.shuffle(current)
        med_5, var_5, stddev_5, cv_5, qcd_5 = stats(current[:5])
        #random.shuffle(current)
        med_10, var_10, stddev_10, cv_10, qcd_10 = stats(current[:10])
        #random.shuffle(current)
        med_25, var_25, stddev_25, cv_25, qcd_25 = stats(current[:25])
        #random.shuffle(current)
        med_50, var_50, stddev_50, cv_50, qcd_50 = stats(current[:50])
        #random.shuffle(current)
        med_100, var_100, stddev_100, cv_100, qcd_100 = stats(current)

        nb_first = increase_first_for_both(
            nb_first,
            [cv_5, cv_10, cv_25, cv_50, cv_100],
            [qcd_5, qcd_10, qcd_25, qcd_50, qcd_100],
            [stddev_5, stddev_10, stddev_25, stddev_50, stddev_100]
        )
    return nb_first

def read_and_count(unit):
    nb_first = [0] * (5 * 3)
    for considered_commit in considered_commits:
        for json_data_path_file in ['/data_v1.json', '/data_v2.json']:
            path = considered_commit + json_data_path_file
            if isfile(path):
                nb_first = read_data_and_count(path, nb_first, unit)
    print('unit', 'indicator', '[5, 10, 25, 50, 100]')
    print(unit, 'cv', nb_first[0:5])
    print(unit, 'qcd', nb_first[5:10])
    print(unit, 'stddev', nb_first[10:15])

if __name__ == '__main__':

    # this script was used to design the experiment on the preliminary result
    # this script won't work any more, unless you use the data in the following commits :
    # e647dc3219573de6e922b282d414cbcc9f284645

    path = sys.argv[1]

    considered_commits = []
    for dirName, subdirList, fileList in os.walk(path):
        if dirName.endswith('diff-jjoules'):
            if check_if_end_properly(fileList):
                considered_commits.append(dirName)
    
    total_number_test = 0

    for considered_commit in considered_commits:
        for json_data_path_file in ['/data_v1.json', '/data_v2.json']:
            path = considered_commit + json_data_path_file
            if isfile(path):
                data = read_json(considered_commit + json_data_path_file)
                total_number_test = total_number_test + len(data)

    print('number of considered commits :', len(considered_commits))
    print('number of test methods :', total_number_test)
    
    #read_and_count('energy')
    #read_and_count('instructions')

    path = considered_commits[0] + '/data_v1.json'
    data = read_json(path)
    test = list(data.keys())[2]
    energies = []
    for record in data[test]:
        energies.append(record['energy'])
    print(energies)
    energies = sorted(energies)
    for energy in energies:
        print(energy)
    print('#', 'med', 'variance', 'stddev', 'cv', 'qcd')
    print(str(5), stats(energies[:5]))
    print(str(10), stats(energies[:10]))
    print(str(25), stats(energies[:25]))
    print(str(100), stats(energies))
    print(str(100) + ' - 5', stats(sorted(energies)[5:-5]))
    print(str(100) + ' - 10', stats(sorted(energies)[10:-10]))
