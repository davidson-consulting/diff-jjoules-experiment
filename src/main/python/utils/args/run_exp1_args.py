import argparse

class RunArgs():

    def build_parser(self):
        parser = argparse.ArgumentParser()

        parser.add_argument('-c', '--no-clone', type=bool, help='Specify that we need to clone or not.')
        parser.add_argument('-i', '--input', type=str, help='Specify the path to input files.')
        parser.add_argument('-o', '--output', type=str, help='Specify the path to output the files.')
        parser.add_argument('-p', '--project', type=str, help='Specify the name of the projet.')
        parser.add_argument('-b', '--begin', type=int, default=-1, help='Specify the index of the commit to start with.')
        parser.add_argument('-e', '--end', type=int, default=-1, help='Specify the index of the commit to end with.')
        
        return parser
