import sys

from utils.constants import *
from utils.args.input_args import *

from utils.cmd.git_cmd import *
from utils.cmd.io_cmd import *

import clone

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()
    url = args.url
    project = args.project
    output = args.output

    clone.remove_and_clone_both(url)

    create_if_does_not_exist(output + '/' + project)
    output_file_path = output + '/' + project + '/' + COMMITS_FILE_PATH
    delete_file(output_file_path)

    with open(output_file_path, 'w') as output_file:
        output_file.write(url + '\n')
    git_log_pretty_and_redirect(PATH_V1, output_file_path)
