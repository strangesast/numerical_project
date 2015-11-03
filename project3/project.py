#! /usr/bin/python
from __future__ import division
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

#x = np.array([-3.5000, -3.2500, -3.0000, -2.7500, -2.5000, -2.2500, -2.0000, -1.7500,\
#     -1.5000, -1.2500, -1.0000, -0.7500, -0.5000, -0.25000, 0.0, .25000, .50000,\
#     .7500, 1.0000, 1.2500, 1.5000, 1.7500, 2.0000, 2.2500, 2.5000, 2.7500,\
#     3.0000, 3.25000, 3.5000])
x = np.arange(-3.5, 3.5+0.25, 0.25)

y = np.array([0.3508, 0.1082, -0.1411, -0.3817, -0.5985, -0.7781, -0.9093, -0.9840,\
     -0.9975, -0.9490, -0.8415, -0.6816, -0.4794, -0.2474, 0.0, 0.2474, 0.4794,\
     0.6816, 0.8415, 0.9490, 0.9975, 0.9840, 0.9093, 0.7781, 0.5985, 0.3817,\
     0.1411, -0.1082, -0.3508])

# a
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x, y, 'ro', mfc='none', label='original')

# b
def newtons(x, y):
    coefs = []
    A = np.zeros((len(x), len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
            if i == 0:
                A[j, i] = y[j]
            elif len(x) - i > j:
                A[j, i] = (A[j+1, i-1] - A[j, i-1])/(x[i+j]-x[j])

    coeffs = A[0, :]
    alt_x = np.arange(min(*x), max(*x)+0.01, 0.01)
    ys = np.zeros(len(alt_x))
    for i, xi in enumerate(alt_x):
        result = 0
        for ic, c in enumerate(coeffs):
            cs = c
            for j in range(ic):
                cs*=(xi - x[j])
            result += cs
        ys[i] = result

    return alt_x, ys

nx, ny = newtons(x, y)
ax.plot(nx, ny, label='newton')

# c


ax.set_title('Various Methods')
ax.set_xlabel('x')
ax.set_ylabel('y')

ax.legend(
  loc='upper center',
  bbox_to_anchor=(0.5, -0.1),
  fancybox = True,
  ncol = 3
)

filepath = '/home/samuel/Downloads/test.png'
fig.savefig(filepath, bbox_inches='tight')
