from constants import *

from utils.args.graph_args import *

from utils.cmd.io_cmd import *
from utils.cmd.git_cmd import *
from utils.cmd.json_cmd import *

from utils.logs.log import *

from utils.graph.graph import *
from utils.graph.math import *

def get_key_data_from_data(data, key):
    key_data = []
    for d in data:
        key_data.append(d[key])
    return key_data

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()

    input_folder_path = args.input
    output_folder_path = args.output
    project = args.project

    complete_input_folder_path = '/'.join([input_folder_path, project])
    commits = read_file_by_lines('/'.join([complete_input_folder_path, COMMITS_FILE_PATH]))

    cursor_commits = 2
    while cursor_commits < len(commits):
        sha_v1 = reduce_sha(commits[cursor_commits])
        sha_v2 = reduce_sha(commits[cursor_commits-1])

        folder_name = '_'.join(([str(cursor_commits), sha_v1, sha_v2]))

        current_output_folder = '/'.join([output_folder_path, project, folder_name])

        data_v1_per_test = read_json_energy_data_in_folder_per_test('/'.join([current_output_folder, V1]))
        data_v2_per_test = read_json_energy_data_in_folder_per_test('/'.join([current_output_folder, V2]))

        mediane_per_test_v1 = {}
        mediane_per_test_v2 = {}

        mediane_delta_per_test = {}

        for test in data_v1_per_test:
            if not test in data_v2_per_test:
                print('Error', test, 'is not in both version!')
                continue
            data_v1 = get_key_data_from_data(data_v1_per_test[test], INSTR_NB_KEY)
            data_v2 = get_key_data_from_data(data_v2_per_test[test], INSTR_NB_KEY)
            mediane_delta_per_test[test] = mediane_delta(data_v1, data_v2)
            mediane_per_test_v1[test] = mediane(data_v1)
            mediane_per_test_v2[test] = mediane(data_v2)
        cursor_commits = cursor_commits + 1
    
    plot_delta_as_hist(
        from_dict_to_array(mediane_delta_per_test)[10:20],
        [test for test in mediane_per_test_v1][0:10],
        'instructions',
        output='',
        show=True
    )
