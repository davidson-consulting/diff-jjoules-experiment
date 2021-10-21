import matplotlib.pyplot as plt

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