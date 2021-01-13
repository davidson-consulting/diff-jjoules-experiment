import sys
import os
from utils.cmd_utils import *

if __name__ == '__main__':

    for dirName, subdirList, fileList in os.walk(sys.argv[1]):
        for file in fileList:
            if file == 'data_v1.json' or file == 'data_v2.json':
                delete_file(dirName + '/' + file)