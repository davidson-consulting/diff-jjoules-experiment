import sys
import os
import csv

from utils.json_utils import *

def build_csv_file_for_version(path_to_commit_folder, version, csv_data):
    path_version = path_to_commit_folder  + '/v' + version
    print('build csv for', path_version)
    files_v1 = os.listdir(path_version)
    for folder_iteration in files_v1:
        if folder_iteration.endswith('.png') or folder_iteration == 'README.md':
            continue
        path_iteration = path_version + '/' + folder_iteration
        json_files = os.listdir(path_iteration)
        for json_file in json_files:
            path_json = path_iteration + '/' + json_file
            data_json = read_json(path_json)
            if data_json['package|uJ'] != 0:
                csv_data.append([json_file.split('.json')[0], str(version), data_json['package|uJ']])

if __name__ == '__main__':

    path_to_commit_folder = sys.argv[1]

    print('run to_CSV for', path_to_commit_folder)

    csv_data = []

    build_csv_file_for_version(path_to_commit_folder, '1', csv_data)
    build_csv_file_for_version(path_to_commit_folder, '2', csv_data)
    print(csv_data)

    with open('data.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        for row in csv_data:
            print(row)
            csvwriter.writerow(row)
