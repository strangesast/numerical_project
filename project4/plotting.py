from __future__ import division
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import YearLocator, MonthLocator, DayLocator, DateFormatter
import matplotlib.gridspec as gridspec

from methods import parse_data_file 

########################################
# data file location
cpath = os.path.dirname(os.path.realpath(__file__))
data_fname = 'wind_data.csv'
data_fpath = os.path.join(cpath, data_fname)

########################################
# data
header = ['time', 'temperature', 'wind speed', 'gust', 'direction']
data = parse_data_file(data_fpath)
dates = [each[0] for each in data]
temps = [each[1] for each in data]
winds = [each[2] if each[2] is not None else 0 for each in data]
gusts = [(a[0], a[2], a[3]) for a in data if a[3] is not None]

########################################
# figure / axis setup
months = MonthLocator()  # every month
days = DayLocator()
yearsFmt = DateFormatter('%b')
gs = gridspec.GridSpec(2, 1)
fig = plt.figure()
temp_axis = fig.add_subplot(gs[1, 0])
wind_axis = fig.add_subplot(gs[0, 0])

########################################
# plots
temp_axis.plot(dates, temps)
wind_axis.plot(dates, winds)
# plot gust repr
max_gust = reduce(lambda a, b: a if a > b else b, [a[2] for a in gusts])
min_gust = reduce(lambda a, b: a if a < b else b, [a[2] for a in gusts])
max_r = 1 # max radius for gust circle

for each in gusts:
    x, y, gust = each
    p = (gust - min_gust)/(max_gust - min_gust)
    circ = plt.Circle((x, y), max_r*p, color='r', fill=False)
    wind_axis.add_artist(circ)
    #wind_axis.annotate(gust, xy=(x, y))

########################################
# specific axis settings
temp_axis.set_title('Temperature')
temp_axis.set_ylabel('Temperature ($^\circ$F)')
wind_axis.set_title('Wind Speed')
wind_axis.set_ylabel('Wind Speed (mph)')

########################################
# general axis settings
for ax in fig.axes:
    temp_axis.set_xlabel('Day')
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(days)
    ax.autoscale_view()

########################################
# plot output
out_fpath = '/home/samuel/Downloads/plot_test.png'
print('saving figure to "{}"'.format(out_fpath))

big = (30, 10)
small = (15, 5)
fig.set_size_inches(*big)
fig.savefig(out_fpath, bbox_inches='tight')

print('done')
