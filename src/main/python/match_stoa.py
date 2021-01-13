import os
import csv

if __name__ == '__main__':
    files = os.listdir('data/output/january_2021/gson/')
    with open('every.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            commit = row[0]
            for file in files:
                if file == 'README.md' or file.endswith('.png'):
                    continue
                if commit.startswith(file.split('_')[-1]) or commit.startswith(file.split('_')[1]):
                    print(commit, file)