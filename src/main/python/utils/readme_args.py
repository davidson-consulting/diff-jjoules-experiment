import argparse

class RunArgs():

    def build_parser(self):

        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--project-name', type=str, help='Specify the name of the project. Will be used for output purpose')
        parser.add_argument('-d', '--data-path', type=str, help='Specify the path to the data folder.')
        parser.add_argument('-c', '--commits', type=str, help='Specify the path to the commits file.')
        parser.add_argument('-o', '--output', type=str, help='Specify the path to the ouput folder. Should exists.')

        return parser
