import os
import csv

from shutil import copyfile, SameFileError, copytree, rmtree, move

def run_cmd(command):
    print(command)
    return os.system(command)

def isfile(fname):
    return os.path.isfile(fname)

def read_file(file):
    with open(file, 'r') as file_to_read:
        content = file_to_read.read()
    return content

def read_file_by_lines(file):
    with open(file, 'r') as file_to_read:
        content = [line.replace('\n', '') for line in file_to_read.readlines()]
    return content

def copy(src, dst):
    print(src, 'to', dst)
    try:
        copyfile(src, dst)
    except (FileNotFoundError, SameFileError):
       print('Error...', src, dst)

def copy_directory(src, dst):
    try:
        copytree(src, dst)
    except (FileNotFoundError, SameFileError):
       print('Error...', src, dst)

def create_if_does_not_exist(directory):
        if not os.path.isdir(directory):
            os.makedirs(directory)
        return directory

def delete_directory(directory):
    if os.path.isdir(directory):
        rmtree(directory)

def delete_dir_and_mkdir(direction):
    delete_directory(direction)
    mkdir(direction)

def delete_file(file_path):
    try:
        os.remove(file_path)
    except (FileNotFoundError):
        print(file_path, 'does not exist. Pass...')
        
def delete_module_info_java(path):
    for dirName, subdirList, fileList in os.walk(path):
        for file in fileList:
            if file == 'module-info.java':
                delete_file(dirName + '/' + file)

def copy_target_file(path, output_path, target):
    for dirName, subdirList, fileList in os.walk(path):
        for file in fileList:
            if file == target:
                print('copy', dirName + '/' + target, output_path + '/' + target)
                copy(dirName + '/' + target, output_path + '/' + target)
                return

def get_tests_to_execute(path):
    tests_to_execute = {}
    with open(path, 'r') as csvfile:
        file = csv.reader(csvfile, delimiter=';')
        for line in file:
            tests_to_execute[line[0]] = line[1:]
    return tests_to_execute

def mkdir(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        print('pass creation of direction', path)

def zip_folder(path_to_folder):
    run_cmd(' '.join([
            'zip',
            '-r',
            path_to_folder + '.zip',
            path_to_folder
        ]
    ))

def move_directory(src_dir, dst):
    full_dst = os.path.join(os.getcwd(), dst)
    print('move', src_dir, 'to', full_dst)
    move(src_dir, full_dst)

def copy_jjoules_result(src_dir, dst):
    for dirName, subdirList, fileList in os.walk(src_dir):
        for subdir in subdirList:
            if subdir == 'jjoules-reports':
                print('copy dir', dirName + '/' + subdir,  dst)
                copy_directory(dirName + '/' + subdir, dst)