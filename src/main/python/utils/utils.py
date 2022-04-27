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
    return int(commit_path.split('/')[5].split('_')[0])

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

def get_java_path_file(line):
    for word in line.split(' '):
        if word.endswith('.java'):
            return word
    for word in line.split('\t'):
        if word.endswith('.java'):
            return word
    return ''

def check_if_line_is_java_file_modification(line):
    return (line.startswith('+++') or line.startswith('---')) and len(get_java_path_file(line)) > 0

def find_most_impacted_module(path_v1, path_v2):
    os.system(' '.join(['diff', '-ru', path_v1, path_v2, '>', '/tmp/diff']))
    diff_content = read_file('/tmp/diff')
    diff_content_lines = diff_content.split('\n')
    nb_per_module = {}
    for line in diff_content_lines:
        if check_if_line_is_java_file_modification(line):
            java_file = get_java_path_file(line)
            if 'test' in java_file:
                continue
            if path_v1 in java_file:
                module = java_file.split('src/main/java/')[0].split(path_v1)[1]
            else:
                module = java_file.split('src/main/java/')[0].split(path_v2)[1]
            print(module)
            if not module in nb_per_module:
                nb_per_module[module] = 1
            else:
                nb_per_module[module] = nb_per_module[module] + 1
    if len(nb_per_module) == 0:
        return nb_per_module
    print(nb_per_module)
    return sorted(nb_per_module.items(), key=lambda x: x[1], reverse=True)[0][0]
        