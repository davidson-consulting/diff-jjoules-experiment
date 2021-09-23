import argparse

class RunArgs():

    def build_parser(self):
        parser = argparse.ArgumentParser()
        
        parser.add_argument('-u', '--url', type=str, help='Specify the url of the git repository to clone.')
        parser.add_argument('-p', '--project', type=str, help='Specify the name of the projet.')
        parser.add_argument('-o', '--output', type=str, help='Specify the path to output the files.')
        
        return parser