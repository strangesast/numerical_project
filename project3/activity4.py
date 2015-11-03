from __future__ import division
import numpy as np

x = np.array([1, 2, 3, 4])

f = lambda x: 1/x**2

y = map(f, x)

def calc_divided_diff(f, x):
    for xi in x[1:-1]:
        print(xi)
    return True

calc_divided_diff(f, x)
