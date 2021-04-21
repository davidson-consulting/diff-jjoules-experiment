
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from .math import *

def from_dict_to_array(data):
    array = []
    for key in data:
        array.append(data[key])
    return array

def plot_v1_vs_v2(data_v1, data_v2, output_path='', show=False):
    plt.plot(data_v1, 'o')
    plt.plot(data_v2, 'o')
    if show:
        plt.show()
    else:
        plt.savefig(output_path + '.png', bbox_inches='tight')
    plt.clf()

def plot_delta_as_hist(data, labels, unit, output='graph.png', show=False):
    data_p, data_n = [], []
    for d in data:
        if d > 0:
            data_p.append(d)
            data_n.append(0)
        else:
            data_n.append(d)
            data_p.append(0)
    classifier_p = unit + '_p'
    classifier_n = unit + '_n'
    df = pd.DataFrame({'Test': labels,
                    classifier_p: data_p,
                    classifier_n: data_n,
                }, index=labels)
    bar_plot = sns.barplot(x="Test", y=classifier_p, data=df, order=labels, color='red')
    bar_plot = sns.barplot(x='Test', y=classifier_n, data=df, order=labels, color='blue')
    bar_plot.set(ylabel=unit, xlabel="Test")
    plt.tight_layout()
    if show:
        plt.show()
    else:
        plt.savefig(output + '.png')
    plt.clf()