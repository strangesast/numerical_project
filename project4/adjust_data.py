from operator import itemgetter
import csv
import datetime

fname = 'wind_data.csv'
tstring = "%m-%d-%Y %H:%M %Z"

def try_float_conv(ob):
    try:
        return float(ob)
    except ValueError:
        return None


data = []
with open(fname, 'r') as f:
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
        data.append((dt, ws, gs))

sorted_data = sorted(data, key=itemgetter(0))

mindate = sorted_data[0][0]

def add_seconds_delta(row):
    return row + ((row[0] - mindate).total_seconds(), )

# dt, ws, gs, td
sorted_data = map(add_seconds_delta, sorted_data)

just_dt, just_ws, just_gs, just_td = zip(*sorted_data)

print(datetime.timedelta(seconds=max(just_td)/len(just_td)))
