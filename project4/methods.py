import csv
from datetime import datetime, date, timedelta
from scipy import interpolate
from operator import itemgetter
import numpy as np
import csv
import datetime


def try_float_conv(ob):
    try:
        return float(ob)
    except ValueError:
        return None


tstring = "%m-%d-%Y %H:%M %Z"
def parse_data_file(filepath):
    data = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # datetime, temperature, wind speed, gust speed, direction
            dt, temp, ws, gs, d = row
            try:
                dt = datetime.datetime.strptime(dt.replace('MDT', 'UTC'), tstring)
            except ValueError: # end of data
                break
    
            temp, ws, gs, d = map(try_float_conv, [temp, ws, gs, d])
            # keep only datetime, wind speed, gust speed
            data.append((dt, temp, ws, gs))

    sorted_data = sorted(data, key=itemgetter(0))
    mindate = sorted_data[0][0]
    
    # dt, ws, gs, td
    def add_seconds_delta(row):
        return row + ((row[0] - mindate).total_seconds(), )

    return map(add_seconds_delta, sorted_data)


def interpolate_wind_power_table(filepath, xnew):
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        data = []
        # windspeed, power
        for row in reader:
            data.append(map(int, row))
    
    x, y = zip(*data)
    tc = interpolate.splrep(x, y, s=0, k=2)
    ynew = interpolate.splev(xnew, tck, der=0)

    return map(lambda x: round(x, 4), xnew), map(lambda x: round(x, 4), ynew)
