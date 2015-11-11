import csv
from datetime import datetime, date
import numpy as np

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


def spline(x, y, incr=0.1):
    dx = [a-b for a, b in zip(x[1:], x[:-1])]
    dy = [a-b for a, b in zip(y[1:], y[:-1])]
    top = dx
    mid = [1] + [2*(i+j) for i, j in zip(dx[:-1], dx[1:])] + [1]
    bot = dx
    r = [0] + [3*(a[1]/a[0] - b[1]/b[0]) for a, b in zip(zip(dx[1:], dy[1:]), zip(dx[:-1], dy[:-1]))] + [0]
    atop = np.hstack((np.zeros((len(top)+1, 1)), np.vstack((np.diag(top), np.zeros(len(top))))))
    abot = np.hstack((np.vstack((np.zeros(len(bot)),np.diag(bot))),np.zeros((len(bot)+1, 1))))
    tot = abot + atop + np.diag(mid)
    b = np.linalg.solve(tot, r)
    a = [dyi/dxi - dxi*(2*bi1 + bi2)/3 for dxi, dyi, bi1, bi2 in zip(dx, dy, b[:-1], b[1:])]
    c = [(bi2 - bi1)/(3*dxi) for bi1, bi2, dxi in zip(b[:-1], b[1:], dx)]
    ys_all = []
    xs_all = []

    for i, coeff in enumerate(zip(a, b, c)):
        a, b, c = coeff
        xi1 = x[i]
        xi2 = x[i+1]
        yi1 = y[i]
    
        xs = np.arange(xi1, xi2+incr, incr)
        dx = xs - xi1
    
        ys = c*dx
        ys = (ys+b)*dx
        ys = (ys+a)*dx + yi1
        xs_all += list(xs)
        ys_all += list(ys)

    return xs_all, ys_all
