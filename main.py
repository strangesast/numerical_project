from __future__ import division
"""
from matplotlib import pyplot as plt

# Part I
fig = plt.figure()
ax = plt.subplot(111)
xlim = 6.0
ylim = 40
it = 0.1  # iterate by how much

x = map(lambda x: x*it, range(1, int(xlim/it + 1)))

D1 = lambda v: v**2
y1 = map(D1, x)
ax.plot(x, y1, label='parasitic drag')

D2 = lambda v: 20/v**2
y2 = map(D2, x)
ax.plot(x, y2, label='induced drag')

D = lambda v: D1(v) + D2(v)
y = map(D, x)
ax.plot(x, y, label='combined')
y3 = map(lambda x: 20.5, x)
ax.plot(x, y3, label='eng force')


ax.legend(
  loc='upper center',
  bbox_to_anchor=(0.5, -0.1),
  fancybox = True,
  ncol = 4
)

plt.title('Drag')
plt.xlabel('Velocity')
plt.ylabel('Nondimensional Force')
plt.axis([0, xlim, 0, ylim])

fig.savefig('part1.png', bbox_inches='tight')


# Part II

fig.savefig('part2.png', bbox_inches='tight')

# Part III: Bisection method

"""

def bisection(f, interval, good_enough, max_iters=100):
    a = interval[0]
    b = interval[1]

    i = 0
    while i < max_iters:
        fa = f(a) # positive
        fb = f(b) # negative

        c = (a + b)/2
        fc = f(c)

        if abs(fc) < good_enough:
            yield c
            break
        elif 0 < (fa/abs(fa))*fc:
            a = c
        else:
            b = c

        i += 1
        yield (a, b)


g = bisection(lambda x: 2-x, [1.2, 2.25], 0.0001)

while True:
    print(next(g))
