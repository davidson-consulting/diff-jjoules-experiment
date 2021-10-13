
def check_if_end_properly(fileList):
    for file in fileList:
        if file == 'end.txt':
            return False
    return True

def get_id_commit_function(commit_path):
    return int(commit_path.split('/')[4].split('_')[0])