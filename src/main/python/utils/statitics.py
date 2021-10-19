import math

def average(data):
    return sum(data) / len(data)

def mediane(data):
    data = sorted(data)
    if len(data) % 2 == 0:
        middle_cursor = int(len(data) / 2)
        return (data[middle_cursor - 1] + data[middle_cursor]) / 2
    else:
        return data[int(len(data)/2)]

def quartiles(data):
    data = sorted(data)
    if len(data) < 4:
        return data[0], data[-1]
    if len(data) % 2 == 0:
        cursor_middle = int(len(data) / 2)
        return mediane(data[:cursor_middle]), mediane(data[cursor_middle:])
    else:
        cursor_end_q1 = int((len(data) / 2) - 1)
        cursor_begin_q3 = int((len(data) / 2) + 1)
        return mediane(data[:cursor_end_q1]), mediane(data[cursor_begin_q3:])

def format_perc(value):
    return '{:.2f}'.format(value * float(100)) + '\\%'

def compute_and_format_perc(med, value):
    return format_perc(float(float(value) / float(med)))

def format(med, value):
    return '{:.2f}'.format(value) + ' (' + compute_and_format_perc(med, value) + ')'

def format_int(med, value):
    return str(int(value)) + ' (' + compute_and_format_perc(med, value) + ')'

def stats(data_test):
    med = mediane(data_test)
    q1, q3 = quartiles(data_test)
    mean = average(data_test)
    deviations = [ (x - mean) ** 2 for x in data_test ]
    variance = average(deviations)
    stddev = math.sqrt(variance)
    qcd = (q3 - q1) / (q3 + q1)
    cv = stddev / mean
    return med, variance, stddev, cv, qcd

def from_dict_to_array(data, key):
    return [d[key] for d in data]

def from_dict_to_array_rm_zero(data, key):
    array = []
    for d in data:
        if d[key] > 0:
            array.append(d[key])
    return array

def stats_for_given_units(data, units):
    stats_per_unit = {}
    for unit in units:
        data_unit = from_dict_to_array_rm_zero(data, unit)
        if len(data_unit) > 1 and all(not value == 0 for value in data_unit):
            med, variance, stddev, cv, qcd = stats(data_unit)
            stats_per_unit[unit] = [med, variance, stddev, cv, qcd]
        else:
            stats_per_unit[unit] = []
    return stats_per_unit

def compute_avg_variance_avg_stddev(variances):
    avg_variance = average(variances)
    return avg_variance, math.sqrt(avg_variance)

def compute_avg_variance_avg_stddev_for_given_units(variances_per_unit, units):
    avg_variance_per_unit = {}
    avg_stddev_per_unit = {}
    for unit in units:
        avg_variance_per_unit[unit], avg_stddev_per_unit[unit] = compute_avg_variance_avg_stddev(variances_per_unit[unit])
    return avg_variance_per_unit, avg_stddev_per_unit

def remove_outliers(data, unit, nb_to_remove, perc=0.05):
    med = mediane(data_unit)
    for i in range(nb_to_remove):
        dist_beg = abs(med - data_unit[0])
        dist_end = abs(med - data_unit[-1])
        if dist_beg > dist_end:
            data_unit = data_unit[1:]
        else:
            data_unit = data_unit[:-1]
    return data_unit

def remove_outliers_for_units(data, units):
    data_wo_outliers = {}
    if len(data) < 10:
        return data
    nb_to_remove = int(len(data) * perc)
    for unit in units:
        data_wo_outliers[unit], nb_to_remove = remove_outliers(data, unit, nb_to_remove, perc=0.05)
    return data_wo_outliers