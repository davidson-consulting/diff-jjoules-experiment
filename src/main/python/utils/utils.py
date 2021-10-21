import os

def check_if_end_properly(fileList, dirName):
    for file in fileList:
        if file == 'end.txt':
            return False
    return True

def get_id_commit_function(commit_path):
    return int(commit_path.split('/')[4].split('_')[0])

def get_considered_commits_and_sort(root_folder):
    considered_commits = []
    for dirName, subdirList, fileList in os.walk(root_folder):
        if dirName.endswith('diff-jjoules'):
            if check_if_end_properly(fileList, dirName):
                considered_commits.append(dirName)
    return sorted(considered_commits, key=get_id_commit_function)