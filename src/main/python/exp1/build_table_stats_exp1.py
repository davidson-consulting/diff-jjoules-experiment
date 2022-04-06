import sys
import os

from os import listdir

SCRIPT_DIR = os.path.abspath('./src/main/python/utils/')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils.cmd.git_cmd import *
from utils.cmd.io_cmd import *
from utils.cmd.mvn_cmd import *
from utils.cmd.json_cmd import *
from utils.constants import *
from utils.args.build_table_exp1_args import *
from utils.utils import *
from utils.statitics import *
from utils.cmd.latex_cmd import *
from utils.cmd.graph_cmd import *

global nb_record_removed

def compute_med_and_var(diff_jjoules_directory, data, units, medianes_per_unit, diff_sec_instr, diff_sec_cycles, diff_sec_sec):
    global nb_record_removed
    count_test, count_sec_gt_instr, count_sec_gt_cycles = 0, 0, 0 
    for test in data:
        energy_data, instr_data, cycles_data = from_dict_to_array_rm_zero_for_keys_array(data[test], units)
        for d in data[test]:
            if d[units[0]] == 0 or d[units[1]] == 0 or d[units[2]] == 0:
                nb_record_removed = nb_record_removed + 1
        if len(energy_data) == 0 or len(instr_data) == 0 or len(cycles_data) == 0:
            #if not diff_jjoules_directory.split('/')[4] in directory:
                #print(diff_jjoules_directory.split('/')[4])
                #directory.append(diff_jjoules_directory.split('/')[4])
            continue
        energy_med, energy_variance, energy_stddev, energy_cv, energy_qcd, energy_avg_abs_dev, energy_rel_avg_dev = stats(energy_data)
        instr_med, instr_variance, instr_stddev, instr_cv, instr_qcd, instr_avg_abs_dev, instr_rel_avg_dev = stats(instr_data)
        cycles_med, cycles_variance, cycles_stddev, cycles_cv, cycles_qcd, cycles_avg_abs_dev, cycles_rel_avg_dev = stats(cycles_data)
        medianes_per_unit[ENERGY_KEY].append(energy_med)
        medianes_per_unit[INSTR_KEY].append(instr_med)
        medianes_per_unit[CYCLES_KEY].append(cycles_med)
        count_sec_gt_instr = count_sec_gt_instr  + (1 if energy_cv > instr_cv else 0)
        count_sec_gt_cycles = count_sec_gt_cycles  + (1 if energy_cv > cycles_cv else 0)
        #diff_sec_cycles.append(cycles_cv / energy_cv)
        #diff_sec_instr.append(instr_cv / energy_cv)
        #diff_sec_cycles.append(energy_cv / cycles_cv)
        #diff_sec_instr.append(energy_cv / instr_cv)
        #diff_sec_cycles.append(cycles_cv)
        #diff_sec_instr.append(instr_cv)
        #diff_sec_sec.append(energy_cv)
        #diff_sec_cycles.append(cycles_qcd)
        #diff_sec_instr.append(instr_qcd)
        #diff_sec_sec.append(energy_qcd)
        diff_sec_cycles.append(cycles_rel_avg_dev)
        diff_sec_instr.append(instr_rel_avg_dev)
        diff_sec_sec.append(energy_rel_avg_dev)
        count_test = count_test + 1
    return count_test, count_sec_gt_instr, count_sec_gt_cycles, medianes_per_unit, diff_sec_instr, diff_sec_cycles, diff_sec_sec

def compute_stats_for_commit(diff_jjoules_directory, units, medianes_per_unit, diff_sec_instr, diff_sec_cycles, diff_sec_sec):
    id_commit = get_id_commit_function(diff_jjoules_directory)
    data_V1 = read_json(diff_jjoules_directory + '/' + DATA_V1_JSON_FILE_NAME)
    data_V2 = read_json(diff_jjoules_directory + '/' + DATA_V2_JSON_FILE_NAME)
    nb_test_v1, count_sec_gt_instr_v1, count_sec_gt_cycles_v1, medianes_per_unit, diff_sec_instr, diff_sec_cycles, diff_sec_sec = compute_med_and_var(diff_jjoules_directory + '/' + DATA_V1_JSON_FILE_NAME, data_V1, units, medianes_per_unit, diff_sec_instr, diff_sec_cycles, diff_sec_sec)
    nb_test_v2, count_sec_gt_instr_v2, count_sec_gt_cycles_v2, medianes_per_unit, diff_sec_instr, diff_sec_cycles, diff_sec_sec = compute_med_and_var(diff_jjoules_directory + '/' + DATA_V2_JSON_FILE_NAME, data_V2, units, medianes_per_unit, diff_sec_instr, diff_sec_cycles, diff_sec_sec)
    return nb_test_v1 + nb_test_v2, count_sec_gt_instr_v1 + count_sec_gt_instr_v2, count_sec_gt_cycles_v1 + count_sec_gt_cycles_v2, medianes_per_unit, diff_sec_instr, diff_sec_cycles, diff_sec_sec

def build_row_for_project(project, project_root_folder):
    global nb_record_removed
    nb_record_removed = 0
    commits = []
    medianes_per_unit = {}
    units = [ENERGY_KEY, INSTR_KEY, CYCLES_KEY]
    diff_sec_instr, diff_sec_cycles, diff_sec_sec = [], [], []
    for unit in units:
        medianes_per_unit[unit] = []
    nb_test, nb_applicable_commit, count_sec_gt_instr, count_sec_gt_cycles = 0, 0, 0, 0
    properly_ended = []
    commit_folders = listdir(project_root_folder)
    commit_folders.sort(key=lambda commit_folder: int(commit_folder.split('_')[0]) if commit_folder != 'rq2' else -1)
    for commit_folder in commit_folders:
        if commit_folder == 'rq2':
            continue
        if len(properly_ended) == 100:
            corrcoef_instr = corrcoef_datas(medianes_per_unit[ENERGY_KEY], medianes_per_unit[INSTR_KEY])
            corrcoef_cycles = corrcoef_datas(medianes_per_unit[ENERGY_KEY], medianes_per_unit[CYCLES_KEY])
            to_be_printed = [
                project,
                str(len(commits)) + ('(' + compute_and_format_perc(len(commits), nb_applicable_commit) + ')'),
                str(nb_test),
                format_int(nb_test, count_sec_gt_instr),
                format_int(nb_test, count_sec_gt_cycles),
                #str(nb_record_removed),
                '{:.2f}'.format(corrcoef_instr[0][1]),
                '{:.2f}'.format(corrcoef_cycles[0][1])
            ]
            nb_record_removed = 0
            print(to_row_latex(to_be_printed))
            return properly_ended, diff_sec_instr, diff_sec_cycles, diff_sec_sec
        #print(project, commit_folder, len(properly_ended), '/', 100)
        commits.append(commit_folder)
        diff_jjoules_directory = root_folder + '/' + commit_folder + '/diff-jjoules'
        end_properly = check_if_end_properly(diff_jjoules_directory)
        if end_properly:
            properly_ended.append(commit_folder)
            current_nb_test, current_count_sec_gt_instr, current_count_sec_gt_cycles, medianes_per_unit, diff_sec_instr, diff_sec_cycles, diff_sec_sec = compute_stats_for_commit(diff_jjoules_directory, units, medianes_per_unit, diff_sec_instr, diff_sec_cycles, diff_sec_sec)
            nb_test = nb_test + current_nb_test
            count_sec_gt_cycles = count_sec_gt_cycles + current_count_sec_gt_cycles
            count_sec_gt_instr = count_sec_gt_instr + current_count_sec_gt_instr
            nb_applicable_commit = nb_applicable_commit + 1
        #else:
        #   print(commit_folder)
    corrcoef_instr = corrcoef_datas(medianes_per_unit[ENERGY_KEY], medianes_per_unit[INSTR_KEY])
    corrcoef_cycles = corrcoef_datas(medianes_per_unit[ENERGY_KEY], medianes_per_unit[CYCLES_KEY])
    print(len(properly_ended), project)
    to_be_printed = [
        project,
        str(len(commits)) + ('(' + compute_and_format_perc(len(commits), nb_applicable_commit) + ')'),
        str(nb_test),
        format_int(nb_test, count_sec_gt_instr),
        format_int(nb_test, count_sec_gt_cycles),
        #str(nb_record_removed),
        '{:.2f}'.format(corrcoef_instr[0][1]),
        '{:.2f}'.format(corrcoef_cycles[0][1])
    ]
    nb_record_removed = 0
    print(to_row_latex(to_be_printed))
    return properly_ended, diff_sec_instr, diff_sec_cycles, diff_sec_sec

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()

    print(
        to_header_latex([
            'Project',
            '\#Commits',
            '\#TestExec',
            '\#$CV(SEC) > CV(instr)$',
            '\#$CV(SEC) > CV(cycles)$',
            '$\\rho_{instr}$',
            '$\\rho_{cycles}$',
        ])
    )
    properly_ended = []
    diff_sec_instr_per_project, diff_sec_cycles_per_project, diff_sec_sec_per_project= {}, {}, {}
    for project in PROJECTS:
        root_folder = args.output + project
        properly_ended_project, diff_sec_instr, diff_sec_cycles, diff_sec_sec = build_row_for_project(project, root_folder)
        properly_ended.append(properly_ended_project)
        diff_sec_instr_per_project[project] = diff_sec_instr
        diff_sec_cycles_per_project[project] = diff_sec_cycles
        diff_sec_sec_per_project[project] = diff_sec_sec
    print(to_footer_latex())

    jitter_plot(PROJECTS, [diff_sec_instr_per_project, diff_sec_cycles_per_project, diff_sec_sec_per_project], ['instr', 'cycles', 'sec'])

    '''
    for e in properly_ended:
        print(e)
    '''
