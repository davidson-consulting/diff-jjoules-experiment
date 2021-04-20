import argparse

class RunArgs():

    def build_parser(self):
        parser = argparse.ArgumentParser()
        
        parser.add_argument('-p', '--project', type=str, help='Specify the project name')
        parser.add_argument('-i', '--input', type=str, help='Specify the path to the input folder')
        parser.add_argument('-o', '--output', type=str, help='Specify the path to the output folder')
        parser.add_argument('-n', '--iteration', type=int, help='Specify the number of time we need to execute the tests')
        parser.add_argument('--skip-clone', type=bool, help='Skip or not the cloning', default=False)
        parser.add_argument('-b', '--begin', type=int, help='Specify the starting index', default=2)
        parser.add_argument('-e', '--end', type=int, help='Specify the ending index', default=-1)
        
        return parser

