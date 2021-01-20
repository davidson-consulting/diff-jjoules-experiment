import argparse
from enum import Enum

class Mode(Enum):
    restart_mode = 'restart'
    continue_mode = 'continue'
    redo_mode = 'redo'

    def __str__(self):
        return self.value

class RunArgs():

    def build_parser(self):

        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--project-name', type=str, help='Specify the name of the project. Will be used for output purpose')
        parser.add_argument('-o', '--output', type=str, help='Specify the path to the ouput folder. Should exists.')
        parser.add_argument('-c', '--commits', type=str, help='Specify the path to the commits file.')
        parser.add_argument('-i', '--iteration', type=str, help='Specify the number of iteration be done', default='2')
        parser.add_argument('-n', '--nb-commits', type=str, help='Specify the number of commits that must completed', default='2')
        parser.add_argument('mode', default='restart', type=Mode, choices=list(Mode))

        return parser
