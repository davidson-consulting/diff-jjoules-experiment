import math
import numpy as np

from scipy import stats as scipystats

from .utils import *
from .constants import *

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
    avg_abs_dev = sum([ abs(x - mean)  for x in data_test ]) / len(data_test)
    rel_avg_dev = avg_abs_dev / mean
    return med, variance, stddev, cv, qcd, avg_abs_dev, rel_avg_dev

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

def corrcoef(data):
    energy_array, instr_array, cycles_array = from_dict_to_array_rm_zero_for_keys(data, ENERGY_KEY, INSTR_KEY, CYCLES_KEY)
    corrcoef_instr = np.corrcoef(np.array(energy_array), np.array(instr_array))
    corrcoef_cycles = np.corrcoef(np.array(energy_array), np.array(cycles_array))
    '''
    spearmanr_instr = scipystats.spearmanr(np.array(energy_array), np.array(instr_array))
    spearmanr_cycles = scipystats.spearmanr(np.array(energy_array), np.array(cycles_array))
    spearmanr = scipystats.spearmanr(np.array(instr_array), np.array(cycles_array))
    corrcoef = np.corrcoef(np.array(instr_array), np.array(cycles_array))
    print('instr', corrcoef_instr, spearmanr_instr)
    print('cycles', corrcoef_cycles, spearmanr_cycles)
    print('instr vs cycles', spearmanr, corrcoef)
    '''
    return corrcoef_instr, corrcoef_cycles

def corrcoef_datas(data_1, data_2):
    return np.corrcoef(np.array(data_1), np.array(data_2))