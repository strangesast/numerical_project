from __future__ import division
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def spline(x, y):
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
    return zip(a, b, c)


xorig = np.arange(0, 10, 0.01)
yorig = np.sin(xorig)

for j, x in enumerate([np.arange(0, 11, 1.0), np.arange(0, 10.1, 0.1)]):
    y = np.sin(x)
    s = spline(x, y)

    fig = plt.figure()
    ax = plt.subplot(111)

    ys_all = []
    xs_all = []
    for i, coeff in enumerate(s):
        a, b, c = coeff
        xi1 = x[i]
        xi2 = x[i+1]
        yi1 = y[i]
    
        xs = np.arange(xi1, xi2+0.1, 0.1)
        dx = xs - xi1
    
        ys = c*dx
        ys = (ys+b)*dx
        ys = (ys+a)*dx + yi1
        xs_all += list(xs)
        ys_all += list(ys)
    
    lines, = ax.plot(xs_all, ys_all, label='spline')
    lines.set_linewidth(0.5)
    lines, = ax.plot(xorig, yorig, label='y = sin(10x)')
    lines.set_linewidth(0.5)

    ax.plot(x, y, 'r*', label='dataset')
    ax.set_title("Data Set {}".format(j+1))
    ax.legend(
      loc='upper center',
      bbox_to_anchor=(0.5, -0.1),
      fancybox = True,
      ncol = 3
    )
    fig.savefig('/home/samuel/Downloads/plot_{}.svg'.format(j+1), bbox_inches='tight', figsize=(10, 10))
