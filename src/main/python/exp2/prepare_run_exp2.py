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

class MethodCoverage:

    def __init__(self, name, hit):
        self.name = name  
        self.hit = int(hit)
    
    def __repr__(self):
        return self.name + '(' + str(self.hit) + ')'

class ClassCoverage:

    def __init__(self, name, nb_methods, nb_covered_methods):
        self.name = name
        self.nb_methods = int(nb_methods)
        self.nb_covered_methods = int(nb_covered_methods)
        self.method_coverages = []

    def add_method_coverage(self, method_coverage):
        self.method_coverages.append(method_coverage)

    def __repr__(self):
        return self.name + ' ' + str(self.nb_covered_methods) + '/' + str(self.nb_methods)#+ '\n' + '\n'.join([str(x) for x in self.method_coverages])

if __name__ == '__main__':

    # In this EXP, we want to :
    #   - Make different mutation at different places in the latest version of the program
    #   - See if Diff-JJoules is able to detect the energy regression artificially introduced.
    # What we need to do is to find methods that are tested, but not to widely used

    # TODO it is better to relies on result of RQ1 to do this...

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

    mvn_clover(path_module_v1)

    class_coverages = []
    file = minidom.parse(path_module_v1 + 'target/site/clover/clover.xml')
    packages = file.getElementsByTagName('coverage')[0].getElementsByTagName('project')[0].getElementsByTagName('package')
    for package in packages:
        java_class_files = package.getElementsByTagName('file')
        for java_class_file in java_class_files:
            class_name = java_class_file.attributes['name'].value
            if not '$' in class_name:
                metrics = java_class_file.getElementsByTagName('metrics')[0]
                nb_methods = metrics.attributes['methods'].value
                nb_covered_methods = metrics.attributes['coveredmethods'].value
                if nb_methods == '0' or nb_covered_methods == '0':
                    continue
                path = java_class_file.attributes['path'].value
                package = path[0:-len(class_name)].split('src/main/java/')[1].replace('/', '.')
                full_qualified_name = package + class_name[0:-len('.java')]
                current_class_coverage = ClassCoverage(full_qualified_name, nb_methods, nb_covered_methods)
                # TODO construct full qualified name for path
                lines = java_class_file.getElementsByTagName('line')
                for line in lines:
                    if line.attributes['type'].value == 'method':
                        signature = line.attributes['signature'].value
                        method_name = signature.split('(')[0]
                        count = line.attributes['count'].value
                        current_class_coverage.add_method_coverage(MethodCoverage(method_name, count))
                class_coverages.append(current_class_coverage)
    
    # From the class coverage, we want the ones that are mostly used and mostly covered
    class_coverages = sorted(class_coverages, key=lambda coverage: -(coverage.nb_covered_methods / coverage.nb_methods * 100))
    output = {}
    for class_coverage in class_coverages[0:10]:
        method_coverages = class_coverage.method_coverages
        method_coverages = sorted(method_coverages, key=lambda coverage: - coverage.hit)
        selected_method_to_be_mutated = [method_coverage for method_coverage in method_coverages[0:10] if method_coverage.hit > 1000]
        if len(selected_method_to_be_mutated) > 0:
            output[class_coverage.name] = [method_coverage.name for method_coverage in selected_method_to_be_mutated]

    write_json(base_output_path + 'rq2/methodsNames.json', output)