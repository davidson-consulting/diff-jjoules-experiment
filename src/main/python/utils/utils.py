import os

from os import listdir
from .cmd.io_cmd import *
from .constants import *

def check_if_end_properly(fileList, dirName):
    for file in fileList:
        if file == 'end.txt':
            return False
    return True

def check_if_end_properly(diff_jjoules_directory_path):
    has_considered_test_file = isfile(diff_jjoules_directory_path + '/' + CONSIDERED_TEST_METHODS_JSON_FILE_NAME)
    if not has_considered_test_file:
        return False
    if os.path.isdir(diff_jjoules_directory_path):
        diff_jjoules_files = listdir(diff_jjoules_directory_path)
        for diff_jjoules_file in diff_jjoules_files:
            if diff_jjoules_file == 'end.txt':
                with open(diff_jjoules_directory_path + '/' + diff_jjoules_file, 'r') as end_file:
                    content = end_file.read()
                    return has_considered_test_file and (content == 'The energy consumption are too unstable, no method could be considered.\n')
    return True

def get_id_commit_function(commit_path):
    return int(commit_path.split('/')[4].split('_')[0])

def get_considered_commits_and_sort(root_folder):
    considered_commits = []
    for dirName, subdirList, fileList in os.walk(root_folder):
        if dirName.endswith('diff-jjoules'):
            if check_if_end_properly(dirName):
                considered_commits.append(dirName)
    return sorted(considered_commits, key=get_id_commit_function)

def from_dict_to_array(data, key):
    return [d[key] for d in data]

def from_dict_to_array_rm_zero(data, key):
    array = []
    for d in data:
        if d[key] > 0:
            array.append(d[key])
    return array

def from_dict_to_array_rm_zero_for_keys(data, key1, key2, key3):
    array1, array2, array3 = [], [], []
    for d in data:
        if d[key1] > 0 and d[key2] > 0 and d[key3] > 0:
            array1.append(d[key1])
            array2.append(d[key2])
            array3.append(d[key3])
    return array1, array2, array3

def from_dict_to_array_rm_zero_for_keys_array(data, keys):
    return from_dict_to_array_rm_zero_for_keys(data, keys[0], keys[1], keys[2])

def has_any_zero(data):
    for d in data:
        if d[ENERGY_KEY] == 0.0:
            return True
    return False