import argparse

class RunArgs():

    def build_parser(self):
        parser = argparse.ArgumentParser()

        parser.add_argument('-o', '--output', type=str, help='Specify the path to the output folder')
        parser.add_argument('-p', '--project', type=str, help='Specify the name of the projet.')
        
        return parser
