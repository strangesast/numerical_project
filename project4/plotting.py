from __future__ import division
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate, interpolate
from matplotlib.dates import YearLocator, MonthLocator, DayLocator, DateFormatter
import matplotlib.gridspec as gridspec
import datetime

from methods import parse_data_file, interpolate_wind_power_table

# data file location
cpath = os.path.dirname(os.path.realpath(__file__))
data_fname = 'wind_data.csv'
data_fpath = os.path.join(cpath, data_fname)
header = ['time', 'temperature', 'wind speed', 'gust', 'direction']
data = parse_data_file(data_fpath)


def part_one(data):
    ########################################
    # data
    dates = [each[header.index('time')] for each in data]
    temps = [each[header.index('temperature')] for each in data]
    winds = [each[header.index('wind speed')] if each[2] is not None else 0 for each in data]
    awinds = [(each[2] + each[3])/2 if each[3] is not None else each[2] for each in data]
    gusts = [(a[0], a[2], a[3]) for a in data if a[3] is not None]
    
    ########################################
    # figure / axis setup
    months = MonthLocator()  # every month
    days = DayLocator()
    gs = gridspec.GridSpec(2, 10)
    fig = plt.figure()
    afig = plt.figure()
    temp_axis = fig.add_subplot(gs[1, :])
    wind_axis = fig.add_subplot(gs[0, :])
    wind_averaged_axis = afig.add_subplot(111)
    
    ########################################
    # plots
    temp_axis.plot(dates, temps)
    wind_axis.plot(dates, winds)
    wind_averaged_axis.plot(dates, awinds)
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

    #afig.autofmt_xdate()
    #fig.autofmt_xdate()
    monthsFormat = DateFormatter('%b')
    daysFormat = DateFormatter('%d')
    for ax in afig.axes + fig.axes:
        temp_axis.set_xlabel('Day')
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFormat)
        ax.xaxis.set_minor_locator(days)
        #ax.xaxis.set_minor_formatter(daysFormat)
        #ax.fmt_xdata = DateFormatter('%b-%d')
        ax.autoscale_view()
    
    ########################################
    # plot output
    out_fpath = '/home/samuel/Downloads/plot_both.png'

    aout_fpath = '/home/samuel/Downloads/plot_averaged.png'
    
    big = (30, 10)
    small = (15, 5)
    fig.set_size_inches(*big)
    afig.set_size_inches(*small)

    print('saving figure to "{}"'.format(out_fpath))
    fig.savefig(out_fpath, bbox_inches='tight')
    print('saving figure to "{}"'.format(aout_fpath))
    afig.savefig(aout_fpath, bbox_inches='tight')
    print('done')

deltas = [each[4] for each in data]
dates = [each[header.index('time')] for each in data]
temps = [each[header.index('temperature')] for each in data]
winds = [each[header.index('wind speed')] for each in data]

xnew = np.arange(0, 50, 0.1)
xnew, ynew = interpolate_wind_power_table('power_wind_table.csv', xnew)

interpolated_dict = dict(zip(xnew, ynew))
interpolated_dict[None] = None

powers = []
for wind in winds:
    powers.append(interpolated_dict[wind])

fig = plt.figure(figsize=(16, 4))
ax = fig.add_subplot(111)
ax.plot(dates, powers)
ax.set_ylim(0)
ax.set_ylabel('Power (Watts)')
fig.savefig('/home/samuel/Downloads/spline.png', bbox_inches='tight')

clean = [(a, b) for a, b in zip(powers, deltas) if a is not None and b is not None]
powers, deltas = zip(*clean)
total_power = integrate.simps(powers, deltas)
print(total_power)

date_diff = max(dates)-min(dates)

tck = interpolate.splrep(powers, deltas, s=0, k=2)
xnew = np.arange(0, max(deltas))
ynew = interpolate.splev(xnew, tck, der=0)

total_power = integrate.simps(ynew, xnew)
