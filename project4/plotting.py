from __future__ import division
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate, interpolate
from matplotlib.dates import YearLocator, MonthLocator, DayLocator, DateFormatter
import matplotlib.gridspec as gridspec
from operator import itemgetter
import datetime

from methods import parse_data_file, interpolate_wind_power_table

# data file location
cpath = os.path.dirname(os.path.realpath(__file__))
data_fname = 'wind_data.csv'
data_fpath = os.path.join(cpath, data_fname)
header = ['time', 'temperature', 'wind speed', 'gust', 'delta']
data, mindate = parse_data_file(data_fpath)


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
    wfig = plt.figure()
    jwind_axis = wfig.add_subplot(111)
    temp_axis = fig.add_subplot(gs[1, :])
    wind_axis = fig.add_subplot(gs[0, :])
    wind_averaged_axis = afig.add_subplot(111)
    
    ########################################
    # plots temp_axis.plot(dates, temps)
    jwind_axis.plot(dates, winds)
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
    jwind_axis.set_title('Interpolated Wind Speed Data')
    jwind_axis.set_ylabel('Wind Speed (mph)')
    wind_axis.set_ylabel('Wind Speed (mph)')
    wind_axis.set_title('Wind Speed')
    wind_axis.set_ylabel('Wind Speed (mph)')
    
    ########################################
    # general axis settings

    #afig.autofmt_xdate()
    #fig.autofmt_xdate()
    monthsFormat = DateFormatter('%b   -')
    daysFormat = DateFormatter('%d')
    for ax in afig.axes + fig.axes + wfig.axes:
        temp_axis.set_xlabel('Day')
        plt.xticks(rotation=90)
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFormat)
        ax.xaxis.set_minor_locator(days)
        ax.xaxis.set_minor_formatter(daysFormat)
        #ax.fmt_xdata = DateFormatter('%b-%d')
        ax.autoscale_view()
    

    ########################################
    # plot output
    wout_fpath = '/home/samuel/Downloads/plot_wind.png'
    out_fpath = '/home/samuel/Downloads/plot_both.png'

    aout_fpath = '/home/samuel/Downloads/plot_averaged.png'
    
    big = (30, 10)
    small = (15, 5)
    fig.set_size_inches(*big)
    afig.set_size_inches(*small)
    wfig.set_size_inches(*big)

    print('saving figure to "{}"'.format(wout_fpath))
    wfig.savefig(wout_fpath, bbox_inches='tight')
    print('saving figure to "{}"'.format(out_fpath))
    fig.savefig(out_fpath, bbox_inches='tight')
    print('saving figure to "{}"'.format(aout_fpath))
    afig.savefig(aout_fpath, bbox_inches='tight')
    print('done')

part_one(data)

print('part two')
deltas = [each[header.index('delta')] for each in data]
dates = [each[header.index('time')] for each in data]
temps = [each[header.index('temperature')] for each in data]
winds = [each[header.index('wind speed')] for each in data]

xnew = np.arange(0, 50, 0.1)
xnew, ynew = interpolate_wind_power_table('power_wind_table.csv', xnew)

# convert wind to power in watts (based on interpolated power table)
interpolated_dict = dict(zip(xnew, ynew)) # conversion dict
interpolated_dict[None] = None # add None for gaps in data
powers = [interpolated_dict[wind] for wind in winds] # convert winds to powers

# x, y data for interpolation (without None's)
cpowers, cdeltas = zip(*[(a, b) for a, b in zip(powers, deltas) if a is not None and b is not None])

# interpolation
tck = interpolate.splrep(cdeltas, cpowers, s=0, k=2) # generate interpolation function
nones = [] # deltas where power 'is None'
for xi, yi in zip(deltas, powers):
    if yi is None:
        nones.append(xi)

# generate interpolated points from interpolation function
mpowers = interpolate.splev(nones, tck, der=0) # 'missing powers'
# NOTE: interpolation function generates low (often negative) values that do not
# represent intermediate power values

# recombine interpolated and original data
timedelta_power = zip(cdeltas, cpowers) + zip(nones, mpowers)
both = sorted(timedelta_power, key=itemgetter(0))
# recreate time objects from deltas (in seconds) and mindate
both = map(lambda x: (mindate + datetime.timedelta(seconds=x[0]), x[1]), both)


fig = plt.figure(figsize=(16, 6))
gs = gridspec.GridSpec(3, 10)
ax = fig.add_subplot(gs[0,:])
ax2 = fig.add_subplot(gs[1,:])
ax3 = fig.add_subplot(gs[2,:])
ax.set_ylabel('Energy (sum)')
ax2.set_ylabel('Power')
ax3.set_ylabel('Wind Speed')

x, y = zip(*both)
y = [yi if yi > 0 else 0 for yi in y]
#ax.plot(x, y)

dt, powers = zip(*timedelta_power)

energy = []
last_tot = 0
for i, t in enumerate(dt):
    if i == 0: continue
    xs = dt[:i]
    ys = powers[:i]

    total_power = integrate.simps(ys, xs)
    if total_power < last_tot:
        total_power = last_tot
    last_tot = total_power
    energy.append(total_power)

ax.plot(x[:-20], energy[:-19], linewidth=0.5)
#ax2 = ax.twinx()
#ax2.plot(x[:-20], y[:-20], 'r', linewidth=0.5)
#ax2.set_ylim(0)
ax2.plot(x[:-20], y[:-20], linewidth=0.5)
ax3.plot(x[:-20], winds[:-20], linewidth=0.5)

#for a2 in ax2.get_yticklabels():
#    a2.set_color('r')

#fig.savefig('/home/samuel/Downloads/energy_and_power_and_wind.png', bbox_inches='tight', dpi=500)

xnew = np.arange(0, max(deltas))
ynew = interpolate.splev(xnew, tck, der=0)
xnew_d = [mindate + datetime.timedelta(seconds=x) for x in xnew]


fig = plt.figure(figsize=(10, 4))
ax = fig.add_subplot(111)
ax.plot(xnew_d, ynew)
ax.set_ylim(0)
ax.set_ylabel('Power')
ax.set_xlabel('Time (seconds)')
#xlim = sorted(dates)[-1]
#ax.set_xlim([0, xlim])
ax2 = ax.twinx()
#ax2.set_xlim([0, xlim])
ax2.set_ylabel('Energy')
ax2.plot(dates[:-13], energy[:-12], 'r')
fig.savefig('/home/samuel/Downloads/test.png', bbox_inches='tight')

first = integrate.simps(ynew, xnew)
second = integrate.simps(y, deltas)
