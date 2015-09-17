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


g = bisection(lambda x: 2 - x, -0.5, 2.1, 0.0001)

walk = [x for x in g]

if not walk[-1] == None:
    print(walk[-1])


def newtons(f, fprime, x0, thr=0.001, iters=100):

    root = None

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


g = newtons(lambda x: (x-2)**2 - 1, lambda x: 2*(x-2), 0.25)


walk = [x for x in g]
if not walk[-1] == None:
    print(walk[-1])


def secant(f, x0, x1, thr=0.001, iters=100, sm=0.0001):

    root = None

    for each in range(iters):

        if abs(f(x1) - f(x0)) < sm:
            # too small
            break

        x2 = x1 - f(x1)*(x1 - x0) / (f(x1) - f(x0))

        if abs(f(x2)) < thr:
            root = x2
            break

        x0 = x1
        x1 = x2

        yield x2

    yield root

g = secant(lambda x: (x-2)**2 - 1, 0, 2)

walk = [x for x in g]

print(walk[-1])
