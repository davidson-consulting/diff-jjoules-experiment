import json

def write_json(path_to_json, data):
    with open(path_to_json, 'w') as outfile:
        outfile.write(json.dumps(data, indent=4))

def read_json(path_to_json):
    with open(path_to_json) as json_file:
        data = json.load(json_file)
    return data

CPU_MJ_KEY = 'package|uJ'
DURATION_NS_KEY = 'duration|ns'
DRAM_MJ_KEY = 'dram|uJ'

def get_energy_data(data):
    return {
        'energy': data[CPU_MJ_KEY],
        'duration': data[DURATION_NS_KEY],
        'dram': data[DRAM_MJ_KEY],
    } if data[CPU_MJ_KEY] > 0 else {}

def avg_on_each_field(entries, entry):
    new_entries = {}
    for e in entries:
        new_entries[e] = (entries[e] + entry[e]) / 2
    return new_entries
