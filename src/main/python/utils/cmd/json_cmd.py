import json
import os

CPU_MJ_KEY = 'package|uJ'
DURATION_NS_KEY = 'duration|ns'
DRAM_MJ_KEY = 'dram|uJ'
INSTR_NB_KEY = 'instruction'

def from_json_name_to_test_name(json_path):
    return json_path.split('.json')[0]

def write_json(path_to_json, data):
    with open(path_to_json, 'w') as outfile:
        outfile.write(json.dumps(data, indent=4))

def read_json(path_to_json):
    with open(path_to_json) as json_file:
        data = json.load(json_file)
    return data

def get_energy_data(data):
    return {
        'energy': data[CPU_MJ_KEY],
        'duration': data[DURATION_NS_KEY],
        'dram': data[DRAM_MJ_KEY],
        INSTR_NB_KEY: data[INSTR_NB_KEY]
    } if data[CPU_MJ_KEY] > 0 else { INSTR_NB_KEY: data[INSTR_NB_KEY] }

def read_json_energy_data_in_folder_per_test(folder_path):
    data_per_test = {}
    for dirName, subdirList, fileList in os.walk(folder_path):
        for file in fileList:
            if file.endswith('.json'):
                test_name = from_json_name_to_test_name(file)
                current_path_to_json = '/'.join([dirName, file])
                energy_data = get_energy_data(read_json(current_path_to_json))
                if not test_name in data_per_test:
                    data_per_test[test_name] = []
                data_per_test[test_name].append(energy_data)
    return data_per_test
                