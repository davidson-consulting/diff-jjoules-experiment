import sys
import os

def unzip(path_to_zip):
    print('unzipping', path_to_zip)
    os.system(' '.join(['unzip', '-qq', '-o', path_to_zip]))

if __name__ == '__main__':
    root_folder = sys.argv[1]
    print('unzipping all the zip in', root_folder)

    for dirName, subdirList, fileList in os.walk(root_folder):
        for file in fileList:
            if file.endswith('.zip'):
                unzip(dirName + '/' + file)