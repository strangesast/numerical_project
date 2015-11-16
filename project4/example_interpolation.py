from __future__ import division
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DayLocator, DateFormatter, HourLocator
import numpy as np
from scipy import integrate, interpolate
from matplotlib.dates import YearLocator, MonthLocator, DayLocator, DateFormatter
from operator import itemgetter
import datetime
from methods import parse_data_file, interpolate_wind_power_table

data_fname = 'wind_data.csv'
cpath = os.path.dirname(os.path.realpath(__file__))
data_fpath = os.path.join(cpath, data_fname)
windtable_fname = 'power_wind_table.csv'

data, mindate = parse_data_file(data_fpath)

dates, temps, winds, gusts, deltas = zip(*data)

xnew = np.arange(0, 50, 0.1)
xnew, ynew = interpolate_wind_power_table(windtable_fname, xnew)

interpolated_dict = dict(zip(xnew, ynew)) # conversion dict
interpolated_dict[None] = None # add None for gaps in data

powers = [interpolated_dict[wind] for wind in winds] # convert winds to powers
cpowers, cdeltas = zip(*[(a, b) for a, b in zip(powers, deltas) if a is not None and b is not None])

# interpolation
tck = interpolate.splrep(cdeltas, cpowers, s=0, k=2) # generate interpolation function
nones = [] # deltas where power 'is None'
for xi, yi in zip(deltas, powers):
    if yi is None:
        nones.append(xi)

xnew = np.arange(0, max(deltas), 300)
ynew = interpolate.splev(xnew, tck, der=0)

# generate interpolated points from interpolation function
mpowers = interpolate.splev(nones, tck, der=0) # 'missing powers'

timedelta_power = zip(cdeltas, cpowers) + zip(nones, mpowers)
both = sorted(timedelta_power, key=itemgetter(0))
# recreate time objects from deltas (in seconds) and mindate
both = map(lambda x: (mindate + datetime.timedelta(seconds=x[0]), x[1]), both)

fig = plt.figure()
ax = fig.add_subplot(111)

def seconds_to_dt(ob):
    return mindate + datetime.timedelta(seconds=ob)

days = DayLocator()
hours = HourLocator()  # every month
months = MonthLocator()
hoursFormat = DateFormatter('%H')
dayFormat = DateFormatter('%d')

ax.xaxis.set_major_locator(days)
ax.xaxis.set_major_formatter(dayFormat)
ax.xaxis.set_minor_locator(hours)
ax.xaxis.set_minor_formatter(hoursFormat)

ax.plot(map(seconds_to_dt, nones), mpowers, 'ro', label='interpolated')
ax.plot(map(seconds_to_dt, cdeltas), cpowers, 'bo', label='original')
ax.plot(map(seconds_to_dt, xnew), ynew, 'g', label='interpolation function')
ax.set_xlim([mindate+datetime.timedelta(seconds=5000000), mindate+datetime.timedelta(seconds=5060000)])
ax.set_ylim([-100, 200])
ax.set_ylabel('Power')
ax.set_xlabel('Date / Hours')
#ax.set_xticklabels(map(seconds_to_dt, xnew), rotation=70)

fig.autofmt_xdate()


ax.legend(
  loc='upper center',
  bbox_to_anchor=(0.5, -0.1),
  fancybox = True,
  ncol = 3
)

ax.set_title('Example Interpolation')

plt.savefig('/home/samuel/Downloads/example-interpolation.png', bbox_inches='tight')
