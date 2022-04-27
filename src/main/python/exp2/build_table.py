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
from utils.args.build_table_exp2_args import *
from utils.utils import *
from utils.statitics import *
from utils.cmd.latex_cmd import *
from utils.cmd.graph_cmd import *

# What we want :
# Show how many energy mutation diff-jjoules has been able to detect
# Show the proportion of commits that is considered has introducing an energy regression

def precentage_sec_reg_for_project(project_root_folder):
    commit_folders = listdir(project_root_folder)
    commit_folders.sort(key=lambda commit_folder: int(commit_folder.split('_')[0]) if commit_folder != 'rq2' else -1)
    nb_sec_reg, nb_total = 0, 0
    properly_ended = []
    for commit_folder in commit_folders:
        if commit_folder == 'rq2':
            continue
        if len(properly_ended) == 100:
            break
        diff_jjoules_directory = project_root_folder + '/' + commit_folder + '/diff-jjoules'
        end_properly = check_if_end_properly(diff_jjoules_directory)
        if end_properly:
            properly_ended.append(commit_folder)
            if isfile(diff_jjoules_directory + DELTA_OMEGA_FILE_NAME):
                delta_omega = read_json(diff_jjoules_directory + DELTA_OMEGA_FILE_NAME) 
                nb_sec_reg = nb_sec_reg + (1 if float(delta_omega[ENERGY_KEY]) > 0 else 0)
                nb_total = nb_total + 1
    return format_int_with_total(nb_total, nb_sec_reg)
    

if __name__ == '__main__':
    
    args = RunArgs().build_parser().parse_args()
    
    projects = PROJECTS
    projects = ['gson']
    
    line = []
    print(
        to_header_latex([
            'Project',
            'Max Mutation',
            'Min Mutation',
            '\% SEC REG',
        ])
    )
    for project in projects:
        line.append(project)
        data_path_folder = '/'.join([args.output, project, 'exp2'])
        input_path_folder = '/'.join([args.input, project])
        mutation_intensities = read_json(input_path_folder + '/' + 'mutation_intensities.json')
        selected_methods_to_mutate = read_json(input_path_folder + '/' + 'selected_methods_to_mutate.json')
        for mutation_intensity in ['max', 'min']:
            mutation_cell = []
            for selected_class in selected_methods_to_mutate:
                for selected_method in selected_methods_to_mutate[selected_class]:
                    folder_path_data = '_'.join([ str(int(mutation_intensities[mutation_intensity])), selected_class, selected_method])
                    delta_omega_json_path = '/'.join([data_path_folder, folder_path_data, 'diff-jjoules', 'deltaOmega.json'])
                    if isfile(delta_omega_json_path):
                        deltaOmega = read_json(delta_omega_json_path)
                        if float(deltaOmega[ENERGY_KEY]) > 0:
                            mutation_cell.append('\\cmark{}')
                        else:
                            mutation_cell.append('\\xmark{}')
                    else:
                        mutation_cell.append('---')
            line.append(' '.join(mutation_cell))                    
        line.append(precentage_sec_reg_for_project('/'.join([args.output, project, 'exp1'])))
        print(to_row_latex(line))
        
    print(to_footer_latex())
    
    