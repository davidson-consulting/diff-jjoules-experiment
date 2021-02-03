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

    print_to_file('## Aggregation per test class\n', path_to_readme)

    print_to_file('\n![](./' + project_name + '.png)\n', path_to_readme)
    print_to_file('![](./' + project_name + '_delta_1_v.png)\n', path_to_readme)

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

    print_to_file(construct_row_markdown(['Index', 'TestClassName', '#Tests']), path_to_readme)
    print_to_file(construct_row_markdown(['---', '---', '---']), path_to_readme)
    for i in range(0, len(done_test_class_names)):
        row = construct_row_markdown([labels[i], done_test_class_names[i], str(counter[i])])
        print_to_file(row, path_to_readme)

def print_array_long(array_v1, array_v2, stdev_v1, stdev_v2, path_to_readme):
    for index in range(0, len(array_v1)):
        #perc_dev_v1 = '{:.2f}'.format(float(float(array_v1[index]) / float(stdev_v1[index]) * 100.0))
        perc_dev_v1 = '{:.2f}'.format(float(float(stdev_v1[index]) / float(array_v1[index]) * 100.0))
        perc_dev_v2 = '{:.2f}'.format(float(float(stdev_v2[index]) / float(array_v2[index]) * 100.0))
        #perc_dev_v2 = '{:.2f}'.format(float(float(array_v2[index]) / float(stdev_v2[index]) * 100.0))
        row = construct_row_markdown([
                str(index),
                str(array_v1[index]),
                str(array_v2[index]),
                str(array_v2[index] - array_v1[index]),
                '{:.2f}'.format(stdev_v1[index]),
                perc_dev_v1,
                '{:.2f}'.format(stdev_v2[index]),
                perc_dev_v2
        ])
        print_to_file(row, path_to_readme)

def print_array(array_v1, array_v2, path_to_readme):
    for index in range(0, len(array_v1)):
        row = construct_row_markdown([
                str(index),
                str(array_v1[index]),
                str(array_v2[index]),
                str(array_v2[index] - array_v1[index]),
        ])
        print_to_file(row, path_to_readme)

def check_is_delta_graph(file):
    return file.startswith(project_name + '_delta_energy_') and file.endswith('_v.png')

def run_per_test(data_v1, data_v2, path_to_readme, path_to_commit_folder):
    test_per_test_classes, energies_v1, durations_v1, energies_v2, durations_v2, valid_iteration_v1, valid_iteration_v2, stdev_v1, stdev_v2 = build_data_per_test(data_v1, data_v2)
    current_energies_v1 = []
    current_durations_v1 = []
    current_energies_v2 = []
    current_durations_v2 = []
    current_iteration_v1 = []
    current_iteration_v2 = []
    current_stdev_v1 = []
    current_stdev_v2 = []
    labels = []
    for test_class_name in test_per_test_classes:
        for test in test_per_test_classes[test_class_name]:
            labels.append(test_class_name + '-' + test)
            current_energies_v1.append(energies_v1[test_class_name + '-' + test])
            current_durations_v1.append(durations_v1[test_class_name + '-' + test])
            current_energies_v2.append(energies_v2[test_class_name + '-' + test])
            current_durations_v2.append(durations_v2[test_class_name + '-' + test])
            current_iteration_v1.append(valid_iteration_v1[test_class_name + '-' + test])
            current_iteration_v2.append(valid_iteration_v2[test_class_name + '-' + test])
            current_stdev_v1.append(stdev_v1[test_class_name + '-' + test])
            current_stdev_v2.append(stdev_v2[test_class_name + '-' + test])
        
    print_to_file('\n## Delta Energy per test method\n', path_to_readme)
    files = sorted([file for file in os.listdir(path_to_commit_folder) if check_is_delta_graph(file)], key=lambda folder_name: int(folder_name.split('_')[-2]))
    for file in files:
        if check_is_delta_graph(file):
            print_to_file('![](./' + file + ')\n', path_to_readme)
    print_to_file('\n' + construct_row_markdown(['ID', 'EnergyV1', 'EnergyV2', 'DeltaEnergy', 'σV1', '%σV1','σV2', '%σV2']), path_to_readme)
    print_to_file(construct_row_markdown(['---', '---', '---', '---', '---', '---', '---', '---']), path_to_readme)
    print_array_long(
        current_energies_v1, 
        current_energies_v2, 
        current_stdev_v1,
        current_stdev_v2,
        path_to_readme
    )
    
    '''
    print_to_file('\n## Delta Duration per test method\n', path_to_readme)
    for file in files:
        if file.startswith(project_name + '_delta_duration_') and file.endswith('_v.png'):
            print_to_file('![](./' + file + ')\n', path_to_readme)
    print_to_file('\n' + construct_row_markdown(['ID', 'DurationV1', 'DurationsV2', 'DeltaDuration']), path_to_readme)
    print_to_file(construct_row_markdown(['---', '---', '---', '---']), path_to_readme)
    print_array(current_durations_v1, current_durations_v2, path_to_readme)
    '''
    
    print_to_file('\n## Misc.\n', path_to_readme)
    print_to_file(construct_row_markdown(['ID', 'Test Class', 'Test Method']), path_to_readme)
    print_to_file(construct_row_markdown(['---', '---', '---']), path_to_readme)
    for index in range(0, len(labels)):
        test_class = labels[index].split('-')[0]
        test_method = labels[index].split('-')[1]
        row = construct_row_markdown([
                str(index),
                test_class,
                test_method
        ])
        print_to_file(row, path_to_readme)
    '''
    print_to_file('\n\n\n', path_to_readme)
    print_to_file(construct_row_markdown(['Test', 'IterationV1', 'IterationV2', 'DeltaIteration']), path_to_readme)
    print_to_file(construct_row_markdown(['---', '---', '---', '---']), path_to_readme)
    print_array(current_iteration_v1, current_iteration_v2, path_to_readme)
    '''
    return labels

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
    print_to_file('\n', path_to_readme)

def add_md_link_to_text(text, link):
    return '[' + text + '](' + link + ')'

def get_test_record_by_name(test_records, test_name):
    for test_record in test_records:
        if test_record['name'] == test_name:
            return test_record['category'], test_record['delta'], test_record['categoryPercentage']

def build_lines_tables(keyword, lines_classication, path_to_readme):
    for class_name in lines_classication[keyword]:
        for lines in lines_classication[keyword][class_name]:
            print_to_file(construct_row_markdown([keyword, class_name, str(lines)]), path_to_readme)

def run_for_analyze(path_to_commit_folder, path_to_readme, url_repository_files, module, labels):
    test_classication = read_json(path_to_commit_folder + '/test_classification.json')
    test_records = read_json(path_to_commit_folder + '/test_records.json')
    neutral_tests = test_classication['neutral']
    positive_tests = test_classication['positive']
    negative_tests = test_classication['negative']


    print_to_file('\n\n', path_to_readme)
    print_to_file('## Classifications', path_to_readme)
    print_to_file('\n### Tests', path_to_readme)

    print_to_file(construct_row_markdown(['ID', 'Class', 'Delta', 'Share']), path_to_readme)
    print_to_file(construct_row_markdown(['---', '---', '---', '---']), path_to_readme)
    class_test, class_delta, class_share = get_test_record_by_name(test_records, 'global')
    print_to_file(construct_row_markdown(['G', class_test, str(class_delta), '-']), path_to_readme)
    class_test, class_delta, class_share = get_test_record_by_name(test_records, 'negative')
    print_to_file(construct_row_markdown(['N', class_test, str(class_delta), '{:.2f}'.format(class_share)]), path_to_readme)
    class_test, class_delta, class_share = get_test_record_by_name(test_records, 'positive')
    print_to_file(construct_row_markdown(['P', class_test, str(class_delta), '{:.2f}'.format(class_share)]), path_to_readme)
    for index in range(0, len(labels)):
        test_name = labels[index]
        if not test_name in neutral_tests:
            class_test, class_delta, class_share = get_test_record_by_name(test_records, test_name)
            print_to_file(construct_row_markdown([str(index), class_test, str(class_delta), '{:.2f}'.format(class_share)]), path_to_readme)

    lines_classication = read_json(path_to_commit_folder + '/lines_classification.json')
    
    print_to_file('\n### Lines', path_to_readme)
    print_to_file(construct_row_markdown(['Class', 'Java Class', 'Line']), path_to_readme)
    print_to_file(construct_row_markdown(['---', '---', '---']), path_to_readme)
    build_lines_tables('negative', lines_classication, path_to_readme)
    build_lines_tables('positive', lines_classication, path_to_readme)
    build_lines_tables('unknown', lines_classication, path_to_readme)


def run_for_localization(path_to_commit_folder, path_to_readme, url_repository_files, module):
    selected_test = read_json(path_to_commit_folder + '/selectedTests.json')
    

    print_to_file('\n\n', path_to_readme)
    print_to_file('## Localization of Green Regression', path_to_readme)

    print_to_file('### Selected Tests', path_to_readme)
    print_to_file(construct_row_markdown(['Test class', 'test method']), path_to_readme)
    print_to_file(construct_row_markdown(['---', '---']), path_to_readme)
    for testClass in selected_test:
        splittedClassName = testClass.split('.')
        current_url = url_repository_files + '/' + module + '/src/main/java/' + '/'.join(splittedClassName[:-1]) + '/' + splittedClassName[-1] + '.java'
        for test in selected_test[testClass]:
            line_cell = add_md_link_to_text(str(test), current_url)
            print_to_file(construct_row_markdown([testClass, test]), path_to_readme)

    suspectLines = read_json(path_to_commit_folder + '/suspectLines.json')
    print_to_file('\n### Suspected lines', path_to_readme)
    print_to_file(construct_row_markdown(['Class', 'line']), path_to_readme)
    print_to_file(construct_row_markdown(['---', '---']), path_to_readme)
    for className in suspectLines:
        splittedClassName = className.split('.')
        current_url = url_repository_files + '/' + module + '/src/main/java/' + '/'.join(splittedClassName[:-1]) + '/' + splittedClassName[-1] + '.java'
        for line in suspectLines[className]:
            current_url = current_url + '#L' + str(line)
            line_cell = add_md_link_to_text(str(line), current_url)
            print_to_file(construct_row_markdown([className, line_cell]), path_to_readme)

def construct_url_files(input_file_path, commit_sha_v2):
    with open(commits_file_path, 'r') as commits_file:
        lines = commits_file.readlines()
        repo_url = lines[0]
    return repo_url.split('\n')[0] + '/tree/' + commit_sha_v2

def run_commit(input_file_path, commit_folder, module):
    path_to_commit_folder = path_to_data_project + commit_folder
    path_to_readme = path_to_commit_folder + '/README.md'
    delete_file(path_to_readme)

    commit_sha_v2 = commit_folder.split('_')[-1]

    print_to_file('# ' + project_name + ' ' + commit_sha_v2 + '\n\n', path_to_readme)
    print_to_file(construct_url(input_file_path, commit_sha_v2) + '\n\n', path_to_readme)

    data_v1 = read_json(path_to_commit_folder  + '/data_v1.json')
    data_v2 = read_json(path_to_commit_folder  + '/data_v2.json')
    
    labels = run_per_test(data_v1, data_v2, path_to_readme, path_to_commit_folder)

    url_repository_files = construct_url_files(input_file_path, commit_sha_v2)
    
    run_for_analyze(path_to_commit_folder, path_to_readme, url_repository_files, module, labels)
    run_for_localization(path_to_commit_folder, path_to_readme, url_repository_files, module)

    run_for_time(path_to_commit_folder, path_to_readme)
    #run_for_per_class(data_v1, data_v2, path_to_readme)
        
if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()
    project_name = args.project_name
    output_path = args.output
    commits_file_path = args.commits + '/' + project_name + '/input'
    data_path = args.data_path
    main_module_name = read_module_name(args.commits + '/' + project_name)

    path_to_data_project = data_path + '/' + project_name + '/'

    nb_commit_measured = 0

    commit_folders = sorted([subfolder for subfolder in os.listdir(path_to_data_project) if not subfolder.endswith('.png') and not subfolder == 'README.md'], key=lambda folder_name: int(folder_name.split('_')[0]))

    for commit_folder in commit_folders:
        if commit_folder.startswith('118_') and not commit_folder.endswith('.png') and not commit_folder == 'README.md':
            print(commit_folder)
            run_commit(commits_file_path, commit_folder, main_module_name)
            nb_commit_measured = nb_commit_measured + 1
    
    path_to_readme = path_to_data_project + 'README.md'
    delete_file(path_to_readme)

    print_to_file('# ' + project_name, path_to_readme)
    with open(commits_file_path, 'r') as commits_file:
        lines = commits_file.readlines()
        nb_commit_total = len(lines) - 1
        repo_url = lines[0]
        print_to_file('\n' + repo_url, path_to_readme)
    
    print_to_file('![](./delta_energy_evolution.png)\n', path_to_readme)
    print_to_file('![](./delta_duration_evolution.png)\n', path_to_readme)

    print_to_file(construct_row_markdown(['Nb total commit', 'Nb commit measured', 'Nb commit errord', 'perc']), path_to_readme)
    print_to_file(construct_row_markdown(['---','---', '---', '---']), path_to_readme)
    print_to_file(construct_row_markdown([
        str(int(nb_commit_total)),
        str(nb_commit_measured),
        str(nb_commit_total - nb_commit_measured),
        '{:.2f}'.format(float(float(nb_commit_measured) / float((nb_commit_total))) * 100
    )]), path_to_readme)