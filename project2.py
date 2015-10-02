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
def gbp(x, y, d):#, board_dimensions):
    d += 1
    test_dim = (8, 8)

    if x == test_dim[0]: return (0, d)
    if y == test_dim[1]: return (0, d)
    if y == 0: return (0, d)
    if x == 0: return (1, d)

    if d < 100:
        one = gbp(x+1, y, d)
        two = gbp(x-1, y, d)
        thr = gbp(x,   y+1, d)
        fou = gbp(x,   y-1, d)

        P = (one[0] + two[0] + thr[0] + fou[0])/4
        return (P, d)

    else:
        return (Symbol(str(convert[x]) + str(convert[y])), d)

all = []
for i in range(9):
    sub = []
    for j in range(9):
        t = gbp(i, j, 0)
        sub.append(t[0])
    all.append(sub)

for each in all:
    print(each)
