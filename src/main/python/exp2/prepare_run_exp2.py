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
from utils.args.run_exp2_args import *
from utils.utils import *
from utils.statitics import *

import clone

from xml.dom import minidom

class CoveredLine:
    def __init__(self, line, count):
        self.line = line
        self.count = count
    
    def __repr__(self):
        return str(self.line) + '(' + str(self.count) + ')'

class CoveredMethod:
    def __init__(self, name, begin_line, count):
        self.name = name
        self.begin_line = begin_line
        self.covered_lines = []
        self.count = count

    def add_covered_line(self, covered_line):
        self.covered_lines.append(covered_line)
    
    def is_ending_after(self, target_line):
        for covered_line in self.covered_lines:
            if int(covered_line.line) >= target_line:
                return True
        return False
    
    def __repr__(self):
        return '\t' + self.name + ':' + str(self.begin_line) + ':' + str(self.count) + '\n\t{\n\t\t' + ', '.join([str(covered_line) for covered_line in self.covered_lines]) + '\n\t}'

class CoveredClass:
    def __init__(self, name):
        self.name = name
        self.covered_methods = []

    def add_covered_method(self, covered_method):
        self.covered_methods.append(covered_method)
    
    def __repr__(self):
        return self.name + '{\n' + '\n'.join([str(covered_method) for covered_method in self.covered_methods]) + '\n}'

    def get_method_name_at_line(self, target_line):
        for covered_method in self.covered_methods:
            if int(covered_method.begin_line) >= target_line and covered_method.is_ending_after(target_line):
                return covered_method.name
        return ''

def filter_method_name(method_name):
    discarded_method_names = ['equals', 'tostring', 'hashcode', 'pop', 'peek', 'poll', 'add', 'push', 'put', 'size', 'containskey', 'contains', 'clear']
    return not method_name[0].isupper() and \
        not method_name.startswith('is') and \
        not method_name.startswith('has') and \
        not method_name.startswith('get') and \
        not method_name.startswith('set') and \
        not method_name.lower() in discarded_method_names

def get_max_indices(sorted_full_qualified_method_names):
    max_cursor = int(0.10 * len(sorted_full_qualified_method_names))
    return [max_cursor - 2, max_cursor - 1, max_cursor, max_cursor + 1, max_cursor + 2]

def get_min_indices(sorted_full_qualified_method_names):
    min_cursor = int(0.90 * len(sorted_full_qualified_method_names))
    return [min_cursor - 2, min_cursor - 1, min_cursor, min_cursor + 1, min_cursor + 2]

def get_average_indices(sorted_full_qualified_method_names):
    middle_cursor = int(len(sorted_full_qualified_method_names) / 2)
    if len(sorted_full_qualified_method_names) < 5:
        print('not enough data', len())
        return [0]
    return [middle_cursor - 2, middle_cursor - 1, middle_cursor, middle_cursor + 1, middle_cursor + 2]

def find_covered_class_from_class_name(class_name, covered_classes):
    for covered_class in covered_classes:
        if covered_class.name == class_name:
            return covered_class
    return None

def from_full_qualified_name(full_qualified_name):
    splitted_full_qualified_name = full_qualified_name.split('#')
    return splitted_full_qualified_name[0], splitted_full_qualified_name[1]

def to_full_qualified_name(class_name, method_name):
    return class_name + '#' + method_name

def sorting_by_get_and_size(key, dict):
    return len(dict[key])

def select_methods_to_mutate(path_module_v1, base_output_path):
    mvn_diff_jjoules_coverage(path_module_v1)
    copy(path_module_v1 + 'clover_coverage.json', base_output_path + '/clover_coverage.json')
    mvn_clover(path_module_v1)
    copy(path_module_v1 + 'target/site/clover/clover.xml', base_output_path + '/clover.xml')
    file = minidom.parse(path_module_v1 + 'target/site/clover/clover.xml')
    covered_classes = []
    packages = file.getElementsByTagName('coverage')[0].getElementsByTagName('project')[0].getElementsByTagName('package')
    for package in packages:
        java_class_files = package.getElementsByTagName('file')
        for java_class_file in java_class_files:
            class_name = java_class_file.attributes['name'].value
            if not '$' in class_name:
                # Skipping in case there is no covered elements
                metrics = java_class_file.getElementsByTagName('metrics')[0]
                nb_methods = metrics.attributes['methods'].value
                nb_covered_methods = metrics.attributes['coveredmethods'].value
                if nb_methods == '0' or nb_covered_methods == '0':
                    continue
                path = java_class_file.attributes['path'].value
                package = path[0:-len(class_name)].split('src/main/java/')[1].replace('/', '.')
                full_qualified_name = package + class_name[0:-len('.java')]
                current_covered_class = CoveredClass(full_qualified_name)
                lines = java_class_file.getElementsByTagName('line')
                current_covered_method = None
                for line in lines:
                    if line.attributes['type'].value == 'method':
                        if not current_covered_method == None:
                            current_covered_class.add_covered_method(current_covered_method)
                        signature = line.attributes['signature'].value
                        method_name = signature.split('(')[0]
                        num_line = line.attributes['num'].value
                        count = int(line.attributes['count'].value)
                        current_covered_method = CoveredMethod(method_name, num_line, count)
                    elif not line.attributes['type'].value == 'cond':
                        num_line = line.attributes['num'].value
                        count = int(line.attributes['count'].value)
                        current_covered_method.add_covered_line(CoveredLine(num_line, count))
                covered_classes.append(current_covered_class)
    coverage = read_json(path_module_v1 + 'clover_coverage.json')
    tests_that_hit_a_method_by_name = {}
    for test_class in coverage['testClassCoverage']:
        for test_method in coverage['testClassCoverage'][test_class]['testMethodsCoverage']:
            test_method_coverages = coverage['testClassCoverage'][test_class]['testMethodsCoverage'][test_method]['classCoverageList']
            for covered_class_name in test_method_coverages:
                if covered_class_name.endswith('Test') or '$' in covered_class_name:
                    continue
                coverages = test_method_coverages[covered_class_name]['coverages']
                for cov in coverages:
                    covered_class = find_covered_class_from_class_name(covered_class_name, covered_classes)
                    if covered_class == None:
                        continue
                    method_name = covered_class.get_method_name_at_line(cov['line'])
                    if method_name == '':
                        continue
                    full_qualified_method_name = to_full_qualified_name(covered_class_name, method_name)
                    full_qualified_test_method_name = to_full_qualified_name(test_class, test_method)
                    if not full_qualified_method_name in tests_that_hit_a_method_by_name:
                        tests_that_hit_a_method_by_name[full_qualified_method_name] = { full_qualified_test_method_name }
                    else:
                        tests_that_hit_a_method_by_name[full_qualified_method_name].add(full_qualified_test_method_name)
    sorted_full_qualified_method_names = sorted(tests_that_hit_a_method_by_name, key=lambda k: sorting_by_get_and_size(k, tests_that_hit_a_method_by_name), reverse=True)
    selected_methods_to_mutate = {}
    nb_test_per_selected_methods = {}
    indices = get_max_indices(sorted_full_qualified_method_names) + get_average_indices(sorted_full_qualified_method_names) + get_min_indices(sorted_full_qualified_method_names)
    for index in indices:
        class_name, method_name = from_full_qualified_name(sorted_full_qualified_method_names[index])
        if method_name == '':
            print(sorted_full_qualified_method_names[index])
        if not class_name in selected_methods_to_mutate:
            selected_methods_to_mutate[class_name] = []
            nb_test_per_selected_methods[class_name] = {}
        selected_methods_to_mutate[class_name].append(method_name)
        nb_test_per_selected_methods[class_name][method_name] = len(tests_that_hit_a_method_by_name[sorted_full_qualified_method_names[index]])
    
    write_json(base_output_path + '/selected_methods_to_mutate.json', selected_methods_to_mutate)
    write_json(base_output_path + '/nb_test_per_selected_methods.json', nb_test_per_selected_methods)

def read_data_and_append(data, cycles_consumption):
    for test in data:
        for i in range(0, len(data[test])):
            cycles_consumption.append(data[test][i][CYCLES_KEY])
    return cycles_consumption

def get_cycles(data):
    cycles = []
    for d in data:
        cycles = d[CYCLES_KEY]
    return cycles

def compute_mutation_intensities(root_folder, output_path):
    cycles_delta = []
    commit_folders = listdir(root_folder)
    commit_folders.sort(key=lambda commit_folder: int(commit_folder.split('_')[0]) if commit_folder != 'rq2' else -1)
    nb_ended_properly = 0
    for commit_folder in commit_folders:
        if not commit_folder == 'rq2':
            print(commit_folder)
            diff_jjoules_directory = root_folder + '/' + commit_folder + '/diff-jjoules'
            end_properly = check_if_end_properly(diff_jjoules_directory)
            if end_properly:
                nb_ended_properly = nb_ended_properly + 1
                data_V1 = read_json(diff_jjoules_directory + '/' + DATA_V1_JSON_FILE_NAME)
                data_V2 = read_json(diff_jjoules_directory + '/' + DATA_V2_JSON_FILE_NAME)
                for test in data_V1:
                    if test in  data_V2:
                        med_cycles_V1 = mediane([d[CYCLES_KEY] for d in data_V1[test]])
                        med_cycles_V2 = mediane([d[CYCLES_KEY] for d in data_V2[test]])
                        cycles_delta.append(abs(med_cycles_V2 - med_cycles_V1))
        if nb_ended_properly >= 100:
            break
    nb_delta = len(cycles_delta)
    cycles_delta = sorted(cycles_delta)
    index_min = int(nb_delta * 0.10)
    index_med = int(nb_delta / 2)
    index_max = int(nb_delta * 0.90)
    mutation_intensities = {}
    mutation_intensities['max'] = cycles_delta[index_max] 
    mutation_intensities['med'] = cycles_delta[index_med]
    mutation_intensities['min'] = cycles_delta[index_min]
    write_json(output_path + '/mutation_intensities.json', mutation_intensities)

if __name__ == '__main__':
    # In this EXP, we want to :
    #   - Make different mutation at different places in the latest version of the program
    #   - See if Diff-JJoules is able to detect the energy regression artificially introduced.
    # What we need to do is to find methods that are tested
    # We want to select 15 methods:
    #   - 5 that are not largely executed
    #   - 5 that are in the average
    #   - 5 that are largely executed
    # WE WON'T DO THAT 
    # We want to select 15 methods:
    #   - 5 that are executed by a "lot" of tests
    #   - 5 that are executed by a "median number" of tests
    #   - 5 that are executed by a "few" of tests
    # To do this, we sort the (src) methods by the number of test that execute them
    # Then we take the 10 percentile, the median and the 90 percentile -> resulting with 3 methods
    # For each the 3 methods, we select 2 methods before and 2 methods
    # It results with 5 methods of each kind.
    # The quantitative is relative to the project itself
    # We take the number of test since this number impact diff-XJoules direclty

    # We also compute the mutation intensities to be used
    # To do this, we compute from RQ1's result in the same way that the method the energy consumption
    # We take cycles delta mediane
    # We will take only 3 intensities

    # resulting with 3 * 15 runs

    args = RunArgs().build_parser().parse_args()

    commits = read_file_by_lines(args.input + '/' + args.project + '/' + COMMITS_FILE_PATH)
    module = read_file(args.input + '/' + args.project + '/' + MODULE_FILE_PATH)
    base_output_path = args.output + '/' + args.project + '/'
    must_use_date_format = args.date_format

    if not args.no_clone:
        clone.remove_and_clone_both(commits[0])

    git_reset_hard_folder(PATH_V1, commits[1])
    path_module_v1 = PATH_V1 + '/' + module + '/'
    delete_module_info_java(path_module_v1)

    select_methods_to_mutate(path_module_v1, args.input + '/' + args.project)

    compute_mutation_intensities(base_output_path + '/exp1/', args.input + '/' + args.project)