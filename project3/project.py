#! /usr/bin/python
from __future__ import division
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from sympy import Symbol, simplify
import os

basefilepath = '/home/samuel/Downloads/'

def newtons(x, y, alt_x):
    A = np.zeros((len(x), len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
            if i == 0:
                A[j, i] = y[j]
            elif len(x) - i > j:
                A[j, i] = (A[j+1, i-1] - A[j, i-1])/(x[i+j]-x[j])

    coeffs = A[0, :]
    ys = np.zeros(len(alt_x))
    for i, xi in enumerate(alt_x):
        result = 0
        #if i == 0:
        #    symbolic_result = 0
        #    symbol_x = Symbol('x')
        for ic, c in enumerate(coeffs):
            cs = c
            #if i==0: symbolic = c
            for j in range(ic):
                cs*=(xi - x[j])
                #if i==0: symbolic*=(symbol_x - x[j])
            result += cs
            #if i==0: symbolic_result += symbolic
        ys[i] = result
        #if i==0:
            #print(simplify(symbolic_result))
            #print(len(x))

    return alt_x, ys


def lagrange(x, y, alt_x):
    ys = np.zeros(len(alt_x))
    n = len(x)
    for i, xi in enumerate(alt_x):
        result = 0
        for ci in range(n):
            c = 1
            for j in range(n):
                if ci != j:
                    a = (xi - x[j])/(x[ci]-x[j])
                    c*= a
            c*=y[ci]
            result += c
        ys[i] = result
    ys[i] = result

    return alt_x, ys

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


def plot_format_save(xdatas, ydatas, labels, markers, title, folder=None):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(len(xdatas)):
        xdata = xdatas[i]
        ydata = ydatas[i]
        label = labels[i]
        marker = markers[i]
        if label is not None:
            lines, = ax.plot(xdata, ydata, label=label)
            ax.legend(
              loc='upper center',
              bbox_to_anchor=(0.5, -0.1),
              fancybox = True,
              ncol = 3
            )
        else:
            lines, = ax.plot(xdata, ydata)

        if marker is not None:
            lines.set_marker(marker)
            lines.set_fillstyle('none')
            lines.set_linestyle(' ')

    ax.set_title(title)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    filepath = basefilepath
    if folder is not None:
        filepath += folder + '/'
        if not os.path.exists(filepath):
            os.makedirs(filepath)
    filepath += title.replace(' ', '_').lower() + '.png'
    print("saving to: {}".format(filepath))
    fig.savefig(filepath, bbox_inches='tight')


def plot_spline_approximation(x, y, f, folder_name):
    sx, sy = spline(x, y, incr=0.01) 
    plot_format_save([x, sx], [y, sy], ['Original', 'Spline'], ['o', None], 'Spline Approximation', folder_name)

    diff = f(np.array(sx)) - np.array(sy)
    print(f(sx[0]))
    print(sy[0])
    plot_format_save([sx], [diff], [None], [None], 'Spline Error', folder_name)


def plot_approximations_of(x, y, f, folder_name):
    fine_grid = np.arange(min(*x), max(*x)+0.01, 0.01)
    nxx, nyy = newtons(x, y, fine_grid)
    lxx, lyy = lagrange(x, y, fine_grid)
    
    plot_format_save([x, fine_grid, fine_grid], [y, nyy, lyy], ['Original', 'Newton', 'Lagrange'], ['o', None, None], 'Newton and Lagrange Approximation', folder_name)
    
    plot_format_save([fine_grid], [nyy-lyy], [None], [None], 'Newton Lagrange Difference', folder_name)
    
    plot_format_save([fine_grid], [f(fine_grid)-nyy], [None], [None], 'Newton Error', folder_name)
    
    plot_format_save([fine_grid], [f(fine_grid)-lyy], [None], [None], 'Lagrange Error', folder_name)

#x = np.array([-3.5000, -3.2500, -3.0000, -2.7500, -2.5000, -2.2500, -2.0000, -1.7500,\
#     -1.5000, -1.2500, -1.0000, -0.7500, -0.5000, -0.25000, 0.0, .25000, .50000,\
#     .7500, 1.0000, 1.2500, 1.5000, 1.7500, 2.0000, 2.2500, 2.5000, 2.7500,\
#     3.0000, 3.25000, 3.5000])
x = np.arange(-3.5, 3.5+0.25, 0.25)

y = np.array([0.3508, 0.1082, -0.1411, -0.3817, -0.5985, -0.7781, -0.9093, -0.9840,\
     -0.9975, -0.9490, -0.8415, -0.6816, -0.4794, -0.2474, 0.0, 0.2474, 0.4794,\
     0.6816, 0.8415, 0.9490, 0.9975, 0.9840, 0.9093, 0.7781, 0.5985, 0.3817,\
     0.1411, -0.1082, -0.3508])

#plot_format_save([x], [y], [None], ['o'], 'Track Position', 'first')

new_x = np.arange(-3.5, 3.5+0.11, 0.11)
new_y = np.sin(new_x)

#plot_approximations_of(new_x, new_y, np.sin, 'higher')

f = lambda x: np.sin(x)
#plot_approximations_of(x, y, f, 'first')
#plot_spline_approximation(x, y, f, 'spline_2')

x = np.arange(-3.5, 3.5+0.5, 0.5)
y = np.array(map(lambda a: (1+25*a**2)**-1, x))

#plot_approximations_of(x, y, f, 'second')

f = lambda x: (1+25*x**2)**-1
#plot_spline_approximation(x, y, f, 'spline')

new_x = np.arange(-3.5, 3.5+0.20, 0.20)
new_y = f(new_x)
plot_approximations_of(new_x, new_y, f, 'higher_2')
