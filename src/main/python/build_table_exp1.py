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

def to_list_fullqualified_test_method_names(considered_test_methods):
    considered_test_methods_list = []
    for test_class_name in considered_test_methods:
        for test_method_name in considered_test_methods[test_class_name]:
            considered_test_methods_list.append(test_class_name + "#" + test_method_name)
    return considered_test_methods_list

def build_row_stats_result_commit(commit_path):
    
    units = [ENERGY_KEY, INSTR_KEY, DURATIONS_KEY]
    nb_tests = 0
    nb_unstable_tests_per_unit = {}
    medianes_per_unit = {}
    variances_per_unit = {}
    nb_considered_test_methods = 0
    medianes_per_unit_c = {}
    variances_per_unit_c = {}
    for unit in units:
        medianes_per_unit_c[unit] = []
        variances_per_unit_c[unit] = []
        medianes_per_unit[unit] = []
        variances_per_unit[unit] = []
        nb_unstable_tests_per_unit[unit] = 0
    for json_data_path_file in [DATA_V1_JSON_FILE_NAME, DATA_V2_JSON_FILE_NAME]:
        if not isfile(commit_path + json_data_path_file):
            return
        considered_test_methods = to_list_fullqualified_test_method_names(read_json(commit_path + CONSIDERED_TEST_METHODS_JSON_FILE_NAME))
        data = read_json(commit_path + json_data_path_file)
        for fullqualified_test_method_name in data:
            current = []
            nb_tests = nb_tests + 1
            for record in data[fullqualified_test_method_name]:
                current.append(record)
            stats_per_unit = stats_for_given_units(current, units)
            for unit in units:
                if len(stats_per_unit[unit]) > 1:
                    medianes_per_unit[unit].append(stats_per_unit[unit][0])
                    variances_per_unit[unit].append(stats_per_unit[unit][1])
                    if fullqualified_test_method_name in considered_test_methods:
                        medianes_per_unit_c[unit].append(stats_per_unit[unit][0])
                        variances_per_unit_c[unit].append(stats_per_unit[unit][1])
                else:
                    nb_unstable_tests_per_unit[unit] = nb_unstable_tests_per_unit[unit] + 1
    avg_variance_per_unit, avg_stddev_per_unit = compute_avg_variance_avg_stddev_for_given_units(variances_per_unit, units)
    avg_variance_per_unit_c, avg_stddev_per_unit_c = compute_avg_variance_avg_stddev_for_given_units(variances_per_unit_c, units)
    to_be_printed = [str(get_id_commit_function(commit_path))]
    to_be_printed.append(str(nb_tests))
    for unit in units:
        avg_mediane = average(medianes_per_unit[unit])
        to_be_printed.append(compute_and_format_perc(avg_mediane, avg_stddev_per_unit[unit]))
    to_be_printed.append(str(len(considered_test_methods)))
    for unit in units:
        avg_mediane = average(medianes_per_unit_c[unit])
        to_be_printed.append(compute_and_format_perc(avg_mediane, avg_stddev_per_unit_c[unit]))
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
        to_header_latex([
            'ID',
            '\#Tests',
            'AVG$_\sigma(SEC)$',
            'AVG$_\sigma(Instr)$',
            'AVG$_\sigma(Time)$',
            '\#Tests',
            'AVG$_\sigma(SEC)$',
            'AVG$_\sigma(Instr)$',
            'AVG$_\sigma(Time)$',
        ])
    )
    for considered_commit in considered_commits:
        build_row_stats_result_commit(considered_commit)
    print(to_footer_latex())
