global path_to_log

def set_path_log(new_path):
    global path_to_log
    path_to_log = new_path

def print_to_file_to_path(content, path_file):
    with open(path_file, 'a') as file:
        file.write(str(content) + '\n')

def log(content):
    global path_to_log
    print(content, path_to_log)
    print_to_file_to_path(content, path_to_log)