from __future__ import division
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sympy import Symbol
import time

def symbolic_method():
    xdim = 2
    ydim = 2

    # getByPosition
    i = 0
    
    convert = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
    #convert = [0, 1, 2, 3, 4, 5]
    
    x_dimension = 4
    y_dimension = 9
    def gbp(x, y, d):#, board_dimensions):
        d += 1
        test_dim = (x_dimension, y_dimension)
    
        if x == test_dim[0]: return (0, d)
        if y == test_dim[1]: return (0, d)
        if y == 0: return (0, d)
        if x == 0: return (1, d)
    
        if d < 10:
            one = gbp(x+1, y, d)
            two = gbp(x-1, y, d)
            thr = gbp(x,   y+1, d)
            fou = gbp(x,   y-1, d)
    
            P = (one[0] + two[0] + thr[0] + fou[0])/4
            return (P, d)
    
        else:
            return (Symbol(str(convert[x]) + str(convert[y])), d)
    
    _all = []
    for i in range(x_dimension + 1):
        sub = []
        for j in range(y_dimension + 1):
            t = gbp(i, j, 0)
            sub.append(t[0])
        _all.append(sub)
    
    bhold=[]
    for each in _all:
        ahold = []
        for a in each:
            try:
                ahold.append(float(a.as_ordered_terms()[-1]))
            except:
                ahold.append(a)
        bhold.append(ahold)
    
    for x in bhold:
        print(x)
    
    
    
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    
    fig, ax = plt.subplots()
    
    image = np.random.uniform(size=(10, 10))
    print(bhold)
    ax.imshow(bhold, cmap=plt.cm.gray, interpolation='nearest')
    ax.set_title('dropped spines')
    
    # Move left and bottom spines outward by 10 points
    ax.spines['left'].set_position(('outward', 10))
    ax.spines['bottom'].set_position(('outward', 10))
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # Only show ticks on the left and bottom spines
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    
    fig.savefig("/home/samuel/Downloads/out.png", bbox_inches='tight')


def numerical_method(shape, threshold, max_iters=100, trapdoor=None):
    xdim = shape[0]
    ydim = shape[1]

    # [1, 0, 0, ... ]
    # [1, 0, 0, ... ]
    # [ ... ]
    init = np.zeros((xdim, ydim))
    init[:, 0] = np.ones(1)

    # manipulated for each part
    def return_prob(ypos, xpos):
        return 1/8*(
            init[xpos-1, ypos] +\
            init[xpos+1, ypos] +\
            init[xpos-1, ypos-1] +\
            init[xpos-1, ypos+1] +\
            init[xpos+1, ypos+1] +\
            init[xpos+1, ypos-1] +\
            init[xpos, ypos-1] +\
            init[xpos, ypos+1])

    # rearange so delta between iteration can be easily calculated
    last = [x for x in init.reshape((init.shape[0]*init.shape[1]))]
    for iteration in range(max_iters):
        print('{} / {}'.format(iteration, max_iters))
        for i in range(1, ydim-1):
            for j in range(1, xdim-1):
                if trapdoor is not None:
                    if trapdoor[0] == i and trapdoor[1] == j:
                        continue
                init[j, i] = return_prob(i, j)

        # what's the largest change from the previous iteration
        max_diff = sum([abs(b-a) for a, b in zip([y for y in init.reshape((init.shape[0]*init.shape[1]))], last)])
        yield init
        if max_diff > threshold:
            last = [x for x in init.reshape((init.shape[0]*init.shape[1]))]
        else: break


def graph_array(array, filename):
    fig, ax = plt.subplots()
    image = np.random.uniform(size=(10, 10))
    ax.imshow(array, cmap=plt.cm.gray, interpolation='nearest')
    ax.set_title('probability distribution: {}'.format('x'.join(map(str, array.shape))))
    # Move left and bottom spines outward by 10 points
    ax.spines['left'].set_position(('outward', 10))
    ax.spines['bottom'].set_position(('outward', 10))
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # Only show ticks on the left and bottom spines
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    fig.savefig(os.path.join("/home/samuel/Downloads/", filename), bbox_inches='tight')
    return

by_shape = {}
for shape in [(5, 5), (50, 50), (500, 500), (1000, 1000)]:
    print('testing shape: {}'.format(shape))
    test_times = []
    for test in range(1):
        print('test {}'.format(test))
        numerical_test = numerical_method(shape, 1e-8, 10000)
        a = time.time()
        walk = [x for x in numerical_test]
        b = time.time()
        print(len(walk))
        test_times.append((b - a, len(walk)))

    print('graphing {}'.format('x'.join(map(str, shape))))
    filename = "probability_distribution_" + "x".join(map(str, shape)) + ".png"
    graph_array(walk[-1], filename)

    by_shape[shape] = test_times


for key in by_shape:
    print("shape: {}".format("x".join(map(str, key))))
    trial_times = [a for a, b in by_shape[key]]
    average_time = sum(trial_times)/len(trial_times)
    print("average time: {}s".format(average_time))
