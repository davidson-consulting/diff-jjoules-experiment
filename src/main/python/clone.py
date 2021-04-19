import sys

from constants import *
from utils.args.clone_args import *

from utils.cmd.git_cmd import *
from utils.cmd.io_cmd import *

def remove_and_clone_both(url):
    remove_both()
    clone_both(url)

def remove_both():
    delete_directory(PATH_V1)
    delete_directory(PATH_V2)

def clone_both(url):
    git_clone_folder(url, PATH_V1)
    git_clone_folder(url, PATH_V2)

if __name__ == '__main__':

    args = RunArgs().build_parser().parse_args()

    remove_and_clone_both(args.url)