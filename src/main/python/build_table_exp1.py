import sys

from utils.cmd.git_cmd import *
from utils.cmd.io_cmd import *
from utils.cmd.mvn_cmd import *
from utils.cmd.json_cmd import *
from utils.constants import *
from utils.args.build_table_exp1_args import *
from utils.utils import *
from utils.statitics import *
from utils.cmd.latex_cmd import *

CONSIDERED_TEST_METHODS_JSON_FILE_NAME = '/consideredTestMethods.json'
DELTA_OMEGA_FILE_NAME = '/deltaOmega.json'
DIFF_JJOULES_SEC_JSON_FILE_NAME = '/diff_jjoules.json'

DATA_V1_JSON_FILE_NAME = '/data_v1.json'
DATA_V2_JSON_FILE_NAME = '/data_v2.json'

PACKAGE_KEY = 'package-0|uJ'
ENERGY_KEY = 'energy'
INSTR_KEY = 'instructions'
DURATIONS_KEY = 'durations'
DURATIONS_NS_KEY = 'duration|ns'

def build_row_overall_result_commit(commit_path):
    considered_test_methods = read_json(commit_path + CONSIDERED_TEST_METHODS_JSON_FILE_NAME)
    nb_considered_test_methods = 0
    for considered_test_method in considered_test_methods:
        nb_considered_test_methods = nb_considered_test_methods + len(considered_test_method)
    deltaOmegas = read_json(commit_path + DELTA_OMEGA_FILE_NAME)
    diff_jjoules_sec = read_json(commit_path + DIFF_JJOULES_SEC_JSON_FILE_NAME)
    print(
        get_id_commit_function(commit_path), 
        nb_considered_test_methods, 
        deltaOmegas[ENERGY_KEY],
        deltaOmegas[INSTR_KEY],
        deltaOmegas[DURATIONS_KEY],
        diff_jjoules_sec[PACKAGE_KEY],
        diff_jjoules_sec[INSTR_KEY],
        diff_jjoules_sec[DURATIONS_NS_KEY],
    )

def build_row_stats_result_commit(commit_path):
    units = [ENERGY_KEY, INSTR_KEY, DURATIONS_KEY]
    nb_tests = 0
    nb_unstable_tests_per_unit = {}
    medianes_per_unit = {}
    variances_per_unit = {}
    for unit in units:
        medianes_per_unit[unit] = []
        variances_per_unit[unit] = []
        nb_unstable_tests_per_unit[unit] = 0
    for json_data_path_file in [DATA_V1_JSON_FILE_NAME, DATA_V2_JSON_FILE_NAME]:
        data = read_json(commit_path + json_data_path_file)
        for fullqualified_test_method_name in data:
            current = []
            nb_tests = nb_tests + 1
            for record in data[fullqualified_test_method_name]:
                current.append(record)
            #  med, variance, stddev, cv, qcd
            stats_per_unit = stats_for_given_units(current, units)
            for unit in units:
                if len(stats_per_unit[unit]) > 1:
                    medianes_per_unit[unit].append(stats_per_unit[unit][0])
                    variances_per_unit[unit].append(stats_per_unit[unit][1])
                else:
                    nb_unstable_tests_per_unit[unit] = nb_unstable_tests_per_unit[unit] + 1
    avg_variance_per_unit, avg_stddev_per_unit = compute_avg_variance_avg_stddev_for_given_units(variances_per_unit, units)
    to_be_printed = [str(get_id_commit_function(commit_path))]
    to_be_printed.append(str(nb_tests))
    #to_be_printed.append(format_int(nb_tests, nb_unstable_tests))
    for unit in units:
        avg_mediane = average(medianes_per_unit[unit])
        if nb_unstable_tests_per_unit[unit] == 0:
            to_be_printed.append('-')
        else:
            to_be_printed.append(format_int(nb_tests, nb_unstable_tests_per_unit[unit]))
        to_be_printed.append(compute_and_format_perc(avg_mediane, avg_stddev_per_unit[unit]))
    print(to_row_latex(to_be_printed))

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()

    root_folder = args.output + '/' + args.project

    considered_commits = []
    for dirName, subdirList, fileList in os.walk(root_folder):
        if dirName.endswith('diff-jjoules'):
            if check_if_end_properly(fileList):
                considered_commits.append(dirName)

    considered_commits = sorted(considered_commits, key=get_id_commit_function)
    print(
        'ID',
        '#Tests',
        'DeltaOmega(Energy)',
        'DeltaOmega(Instr)',
        'DeltaOmega(Durat)',
        'DiffJJoules(Energy)',
        'DiffJJoules(Instr)',
        'DiffJJoules(Durat)',
    )
    for considered_commit in considered_commits:
        build_row_overall_result_commit(considered_commit)
    print()

    print(
        to_header_latex([
            'ID',
            '\#Tests',
            '\#Discarded(SEC)',
            'ENERGY',
            '\#Discarded(Instr)',
            'INSTRUCTIONS',
            '\#Discarded(Time)',
            'DURATIONS',
        ])
    )
    for considered_commit in considered_commits:
        build_row_stats_result_commit(considered_commit)

    print(to_footer_latex())
