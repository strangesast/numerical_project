from __future__ import division

# Part III: Bisection method

def bisection(f, a, b, thr=0.01, iters=100):
    """ Calculates root of function 'f' on interval [a, b] to precision 'thr' in
    at most 'iters' iterations
    """
    assert f(a)*f(b) <= 0, "f(a), f(b) must be opposite sign"

    root = None

    for each in range(iters):
        c = (a + b)/2

        # if close enough, great
        if abs(f(c)) < thr:
            root = c
            break

        # is fa positive or is fb
        if 0 < f(a)*f(c):
            a = c
        else:
            b = c

        yield c

    yield root


g = bisection(lambda x: 2 - x, -0.5, 2.1, 0.0001)

walk = [x for x in g]

if walk[-1] == None:
    print("didn't find it")

else:
    print(walk[-1])
