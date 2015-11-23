import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from methods import parse_data_file, interpolate_wind_power_table

cpath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(cpath, 'wind_data.csv')
windtable_fname = 'power_wind_table.csv'


data, mindate = parse_data_file(filepath)
print(data[0])

xnew = np.arange(0, 50, 0.1)
xnew, ynew = interpolate_wind_power_table(windtable_fname, xnew)

def furling(_min, _max, data):
    total_time = 0

    for i, row in enumerate(data[:-1]):
        ws = row[2] if row[2] is not None else 0
        gs = row[3]
        ws = ws if gs is None else (ws+gs)/2
        td = row[-1] # timedelta
        ntd = data[i+1][-1] # next timedelta

        condition = _min <= ws <= _max

        if not condition:
            total_time += ntd - td

    return total_time

total = max([x[-1] for x in data])

per = furling(10, 100, data)

print(per / total)
