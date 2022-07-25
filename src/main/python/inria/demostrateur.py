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

def read_for_project(output_data, project):
    
    label_per_mark_strategy = {
        'STRICT': 'strict', 
        'AGGREGATE': 'agg',
        'CODE_COVERAGE': 'cocov',
        'DIFF_COVERAGE': 'dicov'
    }
    
    prefix_data_path = 'data/february-2022/'
    input_path = 'input/'
    output_path = 'output/'
    data_folder = 'exp1/'
    decisions_folder = 'exp2/'
    diff_jjoules_results_folder = 'diff-jjoules/'
    
    data_project = {}
    data_project['project'] = project
    input_file_content = read_file_by_lines(prefix_data_path + input_path + project + '/input')
    data_project['url'] = input_file_content[0] 
    data_project['total_commit'] = len(input_file_content) - 1
    
    project_root_folder = prefix_data_path + output_path + project + '/'
    commits_folder = listdir(project_root_folder + data_folder)
    commits_folder.sort(key=lambda commit_folder: int(commit_folder.split('_')[0]))

    data_project['data'] = []
    previous_delta = 0
    for commit_folder in commits_folder:
        diff_jjoules_directory = project_root_folder + data_folder + commit_folder + '/diff-jjoules'
        base_decision_folder_path = project_root_folder + decisions_folder + commit_folder
        end_properly = check_if_end_properly(diff_jjoules_directory) and check_if_end_properly(base_decision_folder_path)
        if end_properly:
            commit_data = {}
            commit_data['id'] = int(commit_folder.split('_')[0])
            commit_data['sha_v1'] = commit_folder.split('_')[1]
            commit_data['sha_v2'] = commit_folder.split('_')[2]
            deltas = read_json(diff_jjoules_directory + '/deltas.json')
            delta = 0
            nb_tests = 0
            for d in deltas:
                delta = delta + deltas[d]['energy']
                nb_tests = nb_tests + 1
            commit_data['nb_tests'] = nb_tests
            previous_delta = previous_delta + delta
            commit_data['delta'] = previous_delta
            
            base_decision_folder_path_all = base_decision_folder_path + '/ALL_' 
            decisions = {}
            for mark_strategy in MARK_STRATEGIES:
                decisions[label_per_mark_strategy[mark_strategy]] = read_file(base_decision_folder_path_all + mark_strategy + '/decision')
            commit_data['decisions'] = decisions
            data_project['data'].append(commit_data)
            if len(data_project['data']) == 50:
                break
        
    data_project['nb_commit'] = len(data_project['data'])
    
    output_data.append(data_project)
    return output_data

if __name__ == '__main__':
    
    output_pathname = 'diff_jjoules_demo_data.json'
    
    '''
        "project": "gson",
        "url": "http://github.com/google/gson.git
        "nb_commit": 100
        "total_commit": 1000
        "data": [
            {
                "id": 1,
                "sha_v1": "xxxxx",
                "sha_v2": "xxxxx",
                "nb_tests": 23,
                "delta": 10000,
                "decisions": {
                    "strict": "break",
                    "aggregate": "break",
                    "cocov": "pass",
                    "dicov": pass
                }
            },
            ...
        ]
    '''
    
    PROJECTS = [
        'gson', 
        'jsoup', 
        'commons-io',
        'commons-lang',
        'xwiki'
    ]
    
    output_data = []
    for project in PROJECTS:
        output_data = read_for_project(output_data, project)
    
    write_json('diff-jjoules-demo.json', output_data)