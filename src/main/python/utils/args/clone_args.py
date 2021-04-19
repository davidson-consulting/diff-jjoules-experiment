import argparse

class RunArgs():

    def build_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--url', type=str, help='Specify the url of the git repository to clone.')
        return parser
