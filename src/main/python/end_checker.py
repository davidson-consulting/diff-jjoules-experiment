import random
import os
import sys
from utils.cmd.json_cmd import *
from utils.cmd.io_cmd import *
from utils.statitics import *

def check_if_end_properly(fileList):
    for file in fileList:
        if file == 'end.txt':
            return False
    return True
    
def increase_first(nb_first, input_array, offset=0):
    array = [x for x in input_array]
    array.sort()
    for i in range(0, len(input_array)):
        if array[0] == input_array[i]:
            nb_first[i+offset] = nb_first[i+offset] + 1
    return nb_first

def increase_first_for_both(nb_first, cvs, qcds):
    nb_first = increase_first(nb_first, cvs)
    return increase_first(nb_first, qcds, offset=5)

def read_data_and_count(json_data_path_file, nb_first, unit):
    data = read_json(json_data_path_file)
    for fullqualified_test_method_name in data:
        current = []
        for record in data[fullqualified_test_method_name]:
            if record[unit] != 0:
                current.append(record[unit])
        random.shuffle(current)
        med_5, stddev_5, cv_5, qcd_5 = stats(current[:5])
        random.shuffle(current)
        med_10, stddev_10, cv_10, qcd_10 = stats(current[:10])
        random.shuffle(current)
        med_25, stddev_25, cv_25, qcd_25 = stats(current[:25])
        random.shuffle(current)
        med_50, stddev_50, cv_50, qcd_50 = stats(current[:50])
        random.shuffle(current)
        med_100, stddev_100, cv_100, qcd_100 = stats(current)

        nb_first = increase_first_for_both(
            nb_first,
            [cv_5, cv_10, cv_25, cv_50, cv_100],
            [qcd_5, qcd_10, qcd_25, qcd_50, qcd_100]
        )
    return nb_first

def read_and_count(unit):
    nb_first = [0] * (5 * 2)
    for considered_commit in considered_commits:
        for json_data_path_file in ['/data_v1.json', '/data_v2.json']:
            path = considered_commit + json_data_path_file
            if isfile(path):
                nb_first = read_data_and_count(path, nb_first, unit)
    print('unit', 'indicator', '[5, 10, 25, 50, 100]')
    print(unit, 'cv', nb_first[0:5])
    print(unit, 'qcd', nb_first[5:10])

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
    
    read_and_count('energy')
    read_and_count('instructions')

