import csv
from datetime import datetime, date

def check_float(string):
    try:
        return float(string)
    except ValueError:
        return None

tstring = "%m-%d-%Y %H:%M %Z"

def parse_data_file(filepath):
    clean_data = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = [row for row in reader]

    for row in data:
        raw_time, temp, mph, gust, drct = row
        try:
            dt = datetime.strptime(
                    raw_time.replace('MDT', 'UTC'),
                    tstring)
        except ValueError, e:
            # reached end of rows
            break

        clean_data.append([dt] + map(check_float, [temp, mph, gust, drct]))

    return clean_data
