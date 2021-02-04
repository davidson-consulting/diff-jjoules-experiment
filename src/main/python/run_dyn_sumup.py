import sys
from utils.cmd_utils import *
import csv
import datetime
import time
import os

def get_tests_to_execute(output_path):
    path = output_path + '/' + VALUE_TEST_LISTS
    tests_to_execute = []
    with open(path, 'r') as csvfile:
        file = csv.reader(csvfile, delimiter=';')
        for line in file:
            test_class = line[0]
            for test_method in line[1:]:
                tests_to_execute.append(test_class + '_' + test_method)
    return tests_to_execute

def copy_test_list(output_path):
    for dirName, subdirList, fileList in os.walk(PATH_V1):
        for file in fileList:
            if file == VALUE_TEST_LISTS:
                print('copy', dirName + '/' + VALUE_TEST_LISTS, output_path + '/' + VALUE_TEST_LISTS)
                copy(dirName + '/' + VALUE_TEST_LISTS, output_path + '/' + VALUE_TEST_LISTS)
                return

if __name__ == '__main__':

    PATH_V1 = '/tmp/v1/'
    PATH_V2 = '/tmp/v2/'
    repo_url = 'https://github.com/danglotb/gson.git'
    commit_sha_v1 = 'd26c8189182fa96691cc8e0d0f312469ee0627bb'
    commit_sha_v2 = '364de8061173b4b91f4477a55059f68e765fc3d1'
    
    delete_directory(PATH_V1)
    delete_directory(PATH_V2)
    clone(repo_url, PATH_V1)
    clone(repo_url, PATH_V2)
    
    PATH_V1 = '/tmp/v1/gson'
    PATH_V2 = '/tmp/v2/gson'

    reset_hard(commit_sha_v1, PATH_V1)
    delete_module_info_java(PATH_V1)
    reset_hard(commit_sha_v2, PATH_V2)
    delete_module_info_java(PATH_V2)

    output_path_root = 'data/sumup_dyn/'
    mkdir(output_path_root)

    run_mvn_diff_select(PATH_V1, PATH_V2, output_path_root + '/mvn_test_selections.log')
    copy_test_list(output_path_root)
    tests_to_execute = get_tests_to_execute(output_path_root)

    times_to_reach = [1000, 2000, 4000]
    for time in times_to_reach:
        output_path = output_path_root + str(time)
        mkdir(output_path)
        run_optimized_compile_test(PATH_V1)
        run_mvn_clean_test_build_cp(PATH_V2)
        run_mvn_build_classpath_and_instrument_class_dynamic_no_test(PATH_V1, PATH_V2, output_path + '/mvn_cp_instr.log', time)
        run_optimized_compile(PATH_V1)
        run_optimized_compile(PATH_V2)
        mkdir(output_path + '/v1/')
        mkdir(output_path + '/v2/')
        for i in range(100):
            print(i)
            v1_result_folder = output_path + '/v1/' + str(i)
            delete_directory(v1_result_folder)
            run_mvn_test_class(PATH_V1, tests_to_execute, v1_result_folder + '/mvn_test.log', True)
            copy_jjoules_result(PATH_V1, v1_result_folder)

            v2_result_folder = output_path + '/v2/' + str(i)
            delete_directory(v2_result_folder)
            run_mvn_test_class(PATH_V2, tests_to_execute, v2_result_folder + '/mvn_test.log', True)
            copy_jjoules_result(PATH_V2, v2_result_folder)
