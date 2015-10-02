import time
import pprint
from sympy import *
xdim = 2
ydim = 2

def check(test):#, board_dimensions):
    # replace with generator
    test_dim = (4, 4)

    if test[0] == 0: return (True, 1) 
    if test[1] == 0: return (True, 0) 
    if test[0] == test_dim[0]: return (True, 0) 
    if test[1] == test_dim[1]: return (True, 0) 


    return (False, 0)
    

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
