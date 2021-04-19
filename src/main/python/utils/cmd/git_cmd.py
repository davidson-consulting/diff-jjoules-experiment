import os

def run_cmd(command):
    print(command)
    os.system(command)

def git_clone(url):
    run_cmd(' '.join([
        'git',
        'clone',
        url
    ]))

def git_clone_folder(url, folder):
    run_cmd(
        ' '.join([
                'git',
                'clone',
                url, 
                folder
        ])
    )

def git_reset_hard_folder(folder, sha):
    cwd = os.getcwd()
    os.chdir(folder)
    run_cmd(' '.join([
        'git',
        'reset',
        '--hard',
        sha
    ]))
    os.chdir(cwd)

def git_log_pretty_and_redirect(path_project, output_file_path):
    run_cmd(
        ' '.join([
            'git',
            '-C',
            path_project,
            'log',
            '--pretty=format:"%H"',
            '>>',
            output_file_path
        ])
    )
