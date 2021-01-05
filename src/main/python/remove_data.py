import sys
import os
from utils.cmd_utils import *

if __name__ == '__main__':

    for dirName, subdirList, fileList in os.walk(sys.argv[1]):
        for subdir in subdirList:
            if subdir == 'v1' or subdir == 'v2':
                delete_directory(dirName + '/' + subdir)