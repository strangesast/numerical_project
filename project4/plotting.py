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
import scipy.stats
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
    wind_averaged_axis.plot(dates, awinds, 'o')
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
    wind_averaged_axis.set_title('Averaged Gust and Wind Speed')
    wind_averaged_axis.set_ylabel('Speed (mph)')
    
    ########################################
    # general axis settings

    #afig.autofmt_xdate()
    #fig.autofmt_xdate()
    monthsFormat = DateFormatter('%b   -')
    daysFormat = DateFormatter('%d')
    for ax in afig.axes + fig.axes + wfig.axes:
        temp_axis.set_xlabel('Day')
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFormat)
        ax.xaxis.set_minor_locator(days)
        ax.xaxis.set_minor_formatter(daysFormat)
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_rotation('vertical')

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
    afig.set_size_inches(*big)
    wfig.set_size_inches(*big)

    print('saving figure to "{}"'.format(wout_fpath))
    wfig.savefig(wout_fpath, bbox_inches='tight')
    print('saving figure to "{}"'.format(out_fpath))
    fig.savefig(out_fpath, bbox_inches='tight')
    print('saving figure to "{}"'.format(aout_fpath))
    afig.savefig(aout_fpath, bbox_inches='tight')
    print('done')

#part_one(data)

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
ax.set_ylabel('Energy (kWh)')
ax2.set_ylabel('Power (kW)')
ax3.set_ylabel('Wind Speed (mph)')

x, y = zip(*both)
y = [yi if yi > 0 else 0 for yi in y]
#ax.plot(x, y)

dt, powers = zip(*timedelta_power)

apowers = [each if each > 0 else 0 for each in powers]

print("max power: {}".format(max(apowers)))
print("avg power: {}".format(sum(apowers)/len(apowers)))
print("min power: {}".format(min(apowers)))

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

ax.plot(x[:-20], map(lambda x: x/3.6, energy[:-19]), linewidth=0.5) # energy
#ax2 = ax.twinx()
#ax2.plot(x[:-20], y[:-20], 'r', linewidth=0.5)
#ax2.set_ylim(0)
ax2.plot(x[:-20], map(lambda x: x/1000, y[:-20]), linewidth=0.5) # power
ax3.plot(x[:-20], winds[:-20], linewidth=0.5) # windspeed

#for a2 in ax2.get_yticklabels():
#    a2.set_color('r')

fig.savefig('/home/samuel/Downloads/energy_and_power_and_wind.png', bbox_inches='tight', dpi=500)

xnew = np.arange(0, max(deltas))
ynew = interpolate.splev(xnew, tck, der=0)
xnew_d = [mindate + datetime.timedelta(seconds=x) for x in xnew]


fig = plt.figure(figsize=(10, 4))
ax = fig.add_subplot(111)
ax.set_title('Power and Total Energy')
ax.plot(xnew_d, ynew)
ax.set_ylim(0)
ax.set_ylabel('Power (Watts)')
ax.set_xlabel('Date')
#xlim = sorted(dates)[-1]
#ax.set_xlim([0, xlim])
ax2 = ax.twinx()
#ax2.set_xlim([0, xlim])
ax2.plot(dates[:-13], map(lambda x: x/3600000, energy[:-12]), 'r')
ax2.set_ylabel('Energy (kWh)')
ax.fmt_xdata = DateFormatter('%Y-%m-%d')
fig.autofmt_xdate()
fig.savefig('/home/samuel/Downloads/power_energy_twinplot.png', bbox_inches='tight')

first = integrate.simps(ynew, xnew)
second = integrate.simps(y, deltas)

print('spline simps approximation: {}'.format(first))
print('data simps approximation:   {}'.format(second))

cost_per_kilowatthour = 0.121829
dates = dates[:-13]
energy = [x/3600 for x in energy[:-12]]
money = [cost_per_kilowatthour*x/1000-4500 for x in energy]

fig = plt.figure()
ax = fig.add_subplot(111)


ax.plot(dates, money)
ax.set_ylabel('Amount earned ($)')
ax.fmt_xdata = DateFormatter('%Y-%m-%d')

slope, intercept, r_value, p_value, std_err = scipy.stats.linregress([(t-datetime.datetime(1970,1,1)).total_seconds() for t in dates], money)
print("slope: {} $/day".format(slope*(3600*24)))
print("intercept: {}".format(intercept))
print("r^2: {}".format(r_value**2))
print("std_err: {}".format(std_err))

fig.autofmt_xdate()
fig.savefig('/home/samuel/Downloads/money_plot.png')

delta_wind = np.diff([x if x is not None else 0 for x in winds]) / np.diff([t for t in deltas])
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(dates[:-1], delta_wind*3600, 'r')
ax2 = ax.twinx()
ax2.plot(dates, winds)
ax2.set_ylabel('mph')

ax.set_xlabel('Date')
ax.set_ylabel('mph / hr')
ax.set_title('Time Differentiated Wind Speed and Wind Speed')

fig.autofmt_xdate()
fig.set_size_inches((30, 10))
fig.savefig('/home/samuel/Downloads/delta_wind_delta_time.png', bbox_inches='tight')
