import os
import csv
from datetime import datetime, date

cpath = os.path.dirname(os.path.realpath(__file__))
data_fname = 'wind_data.csv'
data_fpath = os.path.join(cpath, data_fname)

with open(data_fpath, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    data = [row for row in reader]

tstring = "%m-%d-%Y %H:%M %Z"
clean_data = []
for row in data:
    raw_time, temp, mph, gust, drct = row
    try:
        dt = datetime.strptime(
                raw_time.replace('MDT', 'UTC'),
                tstring)
    except ValueError, e:
        # reached end of rows
        break


    clean_data.append([dt, temp, mph, gust, drct])

print(len(clean_data))
