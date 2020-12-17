import sys
import os

from utils.cmd_utils import *
from utils.readme_args import *
from utils.json_utils import *
from build_graph import build_data_per_class, build_data_per_test


def construct_url(input_file_path, commit_sha_v2):
    with open(commits_file_path, 'r') as commits_file:
        lines = commits_file.readlines()
        repo_url = lines[0]
    return repo_url.split('\n')[0] + '/commit/' + commit_sha_v2
    
def construct_row_markdown(array_values):
    return '| ' + ' | '.join(array_values) + ' |'

def run_for_per_class(data_v1, data_v2, path_to_readme):
    energies_v1, durations_v1, energies_v2, durations_v2, labels, done_test_class_names, counter = build_data_per_class(data_v1, data_v2)

    print_to_file(construct_row_markdown(['Index', 'EnergyV1', 'EnergyV2', 'DeltaEnergy', ]), path_to_readme)
    print_to_file(construct_row_markdown(['---', '---', '---', '---']), path_to_readme)
    for i in range(0, len(done_test_class_names)):
        row = construct_row_markdown([
            labels[i],
            str(energies_v1[i]), 
            str(energies_v2[i]), 
            str(energies_v2[i] - energies_v1[i]),
        ])
        print_to_file(row, path_to_readme)


    print_to_file('\n' + construct_row_markdown(['Index', 'DurationV1', 'DurationsV2', 'DeltaDuration']), path_to_readme)
    print_to_file(construct_row_markdown(['---', '---', '---', '---']), path_to_readme)
    for i in range(0, len(done_test_class_names)):
        row = construct_row_markdown([
            labels[i],
            str(durations_v1[i]), 
            str(durations_v2[i]),
            str(durations_v2[i] - durations_v1[i]),
        ])
        print_to_file(row, path_to_readme)

    print_to_file('\n![](./' + project_name + '.png)\n', path_to_readme)
    #print_to_file('![](./' + project_name + '_delta.png)\n', path_to_readme)
    #print_to_file('![](./' + project_name + '_delta_v.png)\n', path_to_readme)
    #print_to_file('![](./' + project_name + '_delta_1.png)\n', path_to_readme)
    print_to_file('![](./' + project_name + '_delta_1_v.png)\n', path_to_readme)

    print_to_file(construct_row_markdown(['Index', 'TestClassName', '#Tests']), path_to_readme)
    print_to_file(construct_row_markdown(['---', '---', '---']), path_to_readme)
    for i in range(0, len(done_test_class_names)):
        row = construct_row_markdown([labels[i], done_test_class_names[i], str(counter[i])])
        print_to_file(row, path_to_readme)

def run_per_test(data_v1, data_v2, path_to_readme):
    test_per_test_classes, energies_v1, durations_v1, energies_v2, durations_v2, valid_iteration_v1, valid_iteration_v2 = build_data_per_test(data_v1, data_v2)
    for test_class_name in test_per_test_classes:
        current_energies_v1 = []
        current_durations_v1 = []
        current_energies_v2 = []
        current_durations_v2 = []
        current_iteration_v1 = []
        current_iteration_v2 = []
        labels = []
        for test in test_per_test_classes[test_class_name]:
            labels.append(str(test_per_test_classes[test_class_name].index(test)))
            current_energies_v1.append(energies_v1[test_class_name + '-' + test])
            current_durations_v1.append(durations_v1[test_class_name + '-' + test])
            current_energies_v2.append(energies_v2[test_class_name + '-' + test])
            current_durations_v2.append(durations_v2[test_class_name + '-' + test])
            current_iteration_v1.append(valid_iteration_v1[test_class_name + '-' + test])
            current_iteration_v2.append(valid_iteration_v2[test_class_name + '-' + test])
        
        print_to_file('## ' + test_class_name + '\n', path_to_readme)

        print_to_file(construct_row_markdown(['Test', 'IterationV1', 'IterationV2', 'DeltaIteration']), path_to_readme)
        print_to_file(construct_row_markdown(['---', '---', '---', '---']), path_to_readme)
        for test in test_per_test_classes[test_class_name]:
            index = test_per_test_classes[test_class_name].index(test)
            row = construct_row_markdown([
                test_class_name + '-' + test,
                str(current_iteration_v1[index]),
                str(current_iteration_v2[index]),
                str(current_iteration_v2[index] - current_iteration_v1[index]),
            ])
            print_to_file(row, path_to_readme)

        print_to_file('\n' + construct_row_markdown(['Test', 'EnergyV1', 'EnergyV2', 'DeltaEnergy']), path_to_readme)
        print_to_file(construct_row_markdown(['---', '---', '---', '---']), path_to_readme)
        for test in test_per_test_classes[test_class_name]:
            index = test_per_test_classes[test_class_name].index(test)
            row = construct_row_markdown([
                test_class_name + '-' + test,
                str(current_energies_v1[index]),
                str(current_energies_v2[index]),
                str(current_energies_v2[index] - current_energies_v1[index]),
            ])
            print_to_file(row, path_to_readme)

        print_to_file('\n' + construct_row_markdown(['Test', 'DurationV1', 'DurationsV2', 'DeltaDuration']), path_to_readme)
        print_to_file(construct_row_markdown(['---', '---', '---', '---']), path_to_readme)
        for test in test_per_test_classes[test_class_name]:
            index = test_per_test_classes[test_class_name].index(test)
            row = construct_row_markdown([
                test_class_name + '-' + test,
                str(current_durations_v1[index]),
                str(current_durations_v2[index]),
                str(current_durations_v2[index] - current_durations_v1[index]),
            ])
            print_to_file(row, path_to_readme)
        
        print_to_file('\n![](./' + test_class_name + '-graph.png)\n', path_to_readme)

def run_for_time(path_to_commit_folder, path_to_readme):
    time_file_path = path_to_commit_folder + '/time'
    with open(time_file_path, 'r') as time_file:
        time = time_file.readlines()[0].split('\n')[0]
    time_file_path = path_to_commit_folder + '/time_injection'
    with open(time_file_path, 'r') as time_file:
        time_injection = time_file.readlines()[0].split('\n')[0]
    time_file_path = path_to_commit_folder + '/time_selection'
    with open(time_file_path, 'r') as time_file:
        time_selection = time_file.readlines()[0].split('\n')[0]

    print_to_file('\n\n', path_to_readme)
    print_to_file(construct_row_markdown(['Time Label', 'Time (s)']), path_to_readme)
    print_to_file(construct_row_markdown(['---', '---']), path_to_readme)
    print_to_file(construct_row_markdown(['Selection', time_selection]), path_to_readme)
    print_to_file(construct_row_markdown(['Injection', time_injection]), path_to_readme)
    print_to_file(construct_row_markdown(['Total', time]), path_to_readme)

def run_commit(input_file_path, commit_folder):
    path_to_commit_folder = path_to_data_project + commit_folder
    path_to_readme = path_to_commit_folder + '/README.md'
    delete_file(path_to_readme)

    commit_sha_v2 = commit_folder.split('_')[-1]

    print_to_file('# ' + project_name + ' ' + commit_sha_v2 + '\n\n', path_to_readme)
    print_to_file(construct_url(input_file_path, commit_sha_v2) + '\n\n', path_to_readme)

    data_v1 = read_json(path_to_commit_folder  + '/avg_v1.json')
    data_v2 = read_json(path_to_commit_folder  + '/avg_v2.json')
    
    run_for_per_class(data_v1, data_v2, path_to_readme)
    run_for_time(path_to_commit_folder, path_to_readme)
    run_per_test(data_v1, data_v2, path_to_readme)
        
if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()
    project_name = args.project_name
    output_path = args.output
    commits_file_path = args.commits + '/' + project_name + '/input'
    data_path = args.data_path

    path_to_data_project = data_path + '/' + project_name + '/'

    for commit_folder in os.listdir(path_to_data_project):
        run_commit(commits_file_path, commit_folder)