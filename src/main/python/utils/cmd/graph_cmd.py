import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import random as rnd

def jitter_plot(projects, data, keys):
    sns.set_theme(style="whitegrid")
    dict_for_dataframe = {}
    dict_for_dataframe['project'] = []
    dict_for_dataframe['counter'] = []
    dict_for_dataframe['value'] = []
    for key in keys:
        data_key = data[keys.index(key)]
        for project in data_key:
            for d in data_key[project]:
                dict_for_dataframe['project'].append(project)
                dict_for_dataframe['counter'].append(key)
                dict_for_dataframe['value'].append(d)
    dataframe = pd.DataFrame.from_dict(dict_for_dataframe)
    ax = sns.violinplot(x="project", y="value", hue="counter", data=dataframe, palette="muted")
    plt.savefig('/'.join(['pictures', 'dav_article', 'violin_rel_avg_dev_project.png']))
    plt.clf()

    ax = sns.violinplot(y="value", x="counter", data=dataframe, palette="muted")
    plt.savefig('/'.join(['pictures', 'dav_article', 'violin_rel_avg_dev.png']))
    plt.clf()

    '''
    dict_for_dataframe = {}
    dict_for_dataframe['project'] = []
    dict_for_dataframe['counter'] = []
    dict_for_dataframe['value'] = []
    dict_for_dataframe['sensor'] = []
    for key in keys:
        data_key = data[keys.index(key)]
        for project in data_key:
            for d in data_key[project]:
                real_project = project.split('_')[0]
                sensor = project.split('_')[1]
                dict_for_dataframe['sensor'].append(sensor)
                dict_for_dataframe['project'].append(real_project)
                dict_for_dataframe['counter'].append(key)
                dict_for_dataframe['value'].append(d)
    dataframe = pd.DataFrame.from_dict(dict_for_dataframe)
    ax = sns.violinplot(y="value", x="sensor", hue='counter', data=dataframe, palette="muted")
    plt.savefig('/'.join(['pictures', 'dav_article', 'violin_rel_avg_dev.png']))
    plt.clf()
    '''


def from_dict_to_array(data, key):
    return [d[key] for d in data]

def from_dict_to_array_rm_zero(data, key):
    array = []
    for d in data:
        if d[key] > 0:
            array.append(d[key])
    return array

def plot_graph(data, keys):
    for key in keys:
        array = from_dict_to_array(data, key)
        plt.plot(array, label=key)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    projects = ['gson', 'jsoup']
    instr_data_per_project, cycles_data_per_project = {}, {}
    for project in projects:
        instr_data_per_project[project] = [] 
        cycles_data_per_project[project] = []
    for i in range(1000):
        for project in projects:
            instr_data_per_project[project].append(rnd.random())
            cycles_data_per_project[project].append(rnd.random())
    jitter_plot(projects, [instr_data_per_project, cycles_data_per_project], ['instr', 'cycles'])