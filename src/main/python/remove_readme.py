import sys
import os
from utils.cmd_utils import *

if __name__ == '__main__':

    for dirName, subdirList, fileList in os.walk(sys.argv[1]):
        for file in fileList:
            if file == 'README.md':
                delete_file(dirName + '/' + file)