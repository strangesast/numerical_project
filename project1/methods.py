from __future__ import division

# Part III: Bisection method

def bisection(f, a, b, thr=0.001, iters=100):
    """ Calculates root of function 'f' on interval [a, b] to precision 'thr' in
    at most 'iters' iterations
    """
    assert f(a)*f(b) <= 0, "f(a), f(b) must be opposite sign"

    root = None # if it doesnt converge, use this

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


def newtons(f, fprime, x0, thr=0.001, iters=100):

    root = None

    yield x0

    for each in range(iters):
        y = f(x0)

        if abs(y) < thr:
            root = x0
            break

        yprime = fprime(x0)

        x1 = x0 - y/yprime

        x0 = x1

        yield x1


    yield root


def secant(f, x0, x1, thr=0.001, iters=100, sm=0.0001):

    root = None

    yield x0

    yield x1

    for each in range(iters):

        x2 = x1 - f(x1 if x1 > sm else sm)*(x1 - x0) / (f(x1 if x1 > sm else sm) - f(x0 if x0 > sm else sm))

        if abs(f(x2)) < thr:
            root = x2
            break

        x0 = x1
        x1 = x2

        yield x2

    yield root
