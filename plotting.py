from __future__ import division
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Part I
fig = plt.figure()
ax = plt.subplot(111)
xlim = 6.0
ylim = 40
it = 0.1  # iterate by how much

plt.title('Combined Drag Force')
plt.xlabel('Velocity')
plt.ylabel('Nondimensional Force')
plt.axis([0, xlim, 0, ylim])

x = map(lambda x: x*it, range(1, int(xlim/it + 1)))

D1 = lambda v: v**2
y1 = map(D1, x)

D2 = lambda v: 20/v**2
y2 = map(D2, x)

D = lambda v: D1(v) + D2(v)
y = map(D, x)
ax.plot(x, y, label='combined drag')

fig.savefig('/home/samuel/Downloads/numerical/part1a.png', bbox_inches='tight')

y3 = map(lambda v: 20.5, x)
ax.plot(x, y3, label='engine force')

plt.title('Combined and Constituent Drag Forces')
ax.plot(x, y1, label='parasitic drag')
ax.plot(x, y2, label='induced drag')

ax.legend(
  loc='upper center',
  bbox_to_anchor=(0.5, -0.1),
  fancybox = True,
  ncol = 3
)

fig.savefig('/home/samuel/Downloads/numerical/part1b.png', bbox_inches='tight')


"""
# Part III: Bisection method
from methods import bisection

# v**2 + 20/v**2 = 20.5
f = lambda v: v**2 + 20*v**(-2) - 20.5

# root 1
g1 = bisection(f, 0.1, 3.0, 1*10**(-6))
# root 2
g2 = bisection(f, 3.0, 5.5, 1*10**(-6))

walk1 = [each for each in g1]
walk2 = [each for each in g2]

walk1f = [f(each) + 20.5 for each in walk1]
walk2f = [f(each) + 20.5 for each in walk2]

ax.cla()
ax.plot(x, y, label='combined drag')
ax.plot(x, y3, label='engine force')

ax.plot(walk1, walk1f, 'ro')
#for i in range(len(walk1)):
#    ax.annotate("{}".format(i), (walk1[i], walk1f[i]), shrink=0.05)

ax.plot(walk2, walk2f, 'bo')
#for i in range(len(walk2)):
#    ax.annotate("{}".format(i), (walk2[i], walk2f[i]), shrink=0.05)

plt.title('Bisection Method Root Calculation')
plt.xlabel('Velocity')
plt.ylabel('Nondimensional Force')
plt.axis([0, xlim, 0, ylim])

# 3a.
fig.savefig('/home/samuel/Downloads/numerical/part3a.png', bbox_inches='tight')

# 3b.
with open('/home/samuel/Downloads/numerical/part3b.csv', 'w') as f:
    a = zip(walk1, walk1f, walk2, walk2f)
    f.write(
    "\n".join(
        [", ".join(
            [str(each) for each in each]
            ) for each in a]
        )
    )

# Part IV
from methods import newtons

f = lambda v: v**2 + 20*v**(-2) - 20.5
fprime = lambda v: 2*v - 40*v**(-3)

g1 = newtons(f, fprime, 1.5, 1*10**(-6), iters=100)
g2 = newtons(f, fprime, 3.5, 1*10**(-6), iters=100)

walk1 = [each for each in g1]
walk1f = [f(each) + 20.5 for each in walk1]

walk2 = [each for each in g2]
walk2f = [f(each) + 20.5 for each in walk2]

ax.cla()
ax.plot(x, y, label='combined drag')
ax.plot(x, y3, label='engine force')

ax.plot(walk1, walk1f, 'ro')
ax.plot(walk2, walk2f, 'bo')

plt.title("Newton's Method Root Calculation")
plt.xlabel('Velocity')
plt.ylabel('Nondimensional Force')
plt.axis([0, xlim, 0, ylim])

# 4a.
fig.savefig('/home/samuel/Downloads/numerical/part4a.png', bbox_inches='tight')

# 4b.
with open('/home/samuel/Downloads/numerical/part4b.csv', 'w') as f:
    one = zip(walk1, walk1f)
    two = zip(walk2, walk2f)
    trim = max(len(one), len(two))

    one = one + [('', '') for x in range(abs(len(one) - len(two)))]
    one = one[0:trim]
    two = two + [('', '') for x in range(abs(len(one) - len(two)))]
    two = two[0:trim]

    both = [[x[0], x[1], y[0], y[1]] for x, y in zip(one, two)]

    f.write(
    "\n".join(
        [", ".join(
            [str(each) for each in each]
            ) for each in both]
        )
    )

# 4c.

ax.set_yscale('log')
plt.axis([0, xlim, 0, max(max(walk2f), max(walk1f))])
plt.title("Newton's Method Root Calculation - Log Scale")
plt.ylabel('Natural Log of Nondimensional Force')
fig.savefig('/home/samuel/Downloads/numerical/part4c.png', bbox_inches='tight')


"""
# Part V
from methods import secant
f = lambda v: v**2 + 20*v**(-2) - 20.5

g1 = secant(f, 0.5, 0.6, thr=1*10**(-6), sm=0.01)
g2 = secant(f, 3.5, 3.6, thr=1*10**(-6), sm=0.01)

walk1 = [each for each in g1]
walk2 = [each for each in g2]
walk1f = [f(each) + 20.5 for each in walk1]
walk2f = [f(each) + 20.5 for each in walk2]

ax.cla()
ax.plot(x, y, label='combined drag')
ax.plot(x, y3, label='engine force')

ax.plot(walk1, walk1f, 'ro')
ax.plot(walk2, walk2f, 'bo')

#ax.set_yscale('log')
#plt.axis([0, xlim, 0, max(max(walk2f), max(walk1f))])
plt.axis([0, xlim, 0, ylim])
plt.title("Secant Method Root Calculation")
plt.xlabel('Velocity')
plt.ylabel('Nondimensional Force')
fig.savefig('/home/samuel/Downloads/numerical/part5a.png', bbox_inches='tight')

# 5b
with open('/home/samuel/Downloads/numerical/part5b.csv', 'w') as f:
    one = zip(walk1, walk1f)
    two = zip(walk2, walk2f)
    trim = max(len(one), len(two))

    one = one + [('', '') for x in range(abs(len(one) - len(two)))]
    one = one[0:trim]
    two = two + [('', '') for x in range(abs(len(one) - len(two)))]
    two = two[0:trim]

    both = [[x[0], x[1], y[0], y[1]] for x, y in zip(one, two)]

    f.write(
    "\n".join(
        [", ".join(
            [str(each) for each in each]
            ) for each in both]
        )
    )

# 5c
ax.set_yscale('log')
plt.axis([0, xlim, 0, max(max(walk2f), max(walk1f))])
plt.title("Secant Method Root Calculation - Log Scale")
plt.ylabel('Natural Log of Nondimensional Force')
fig.savefig('/home/samuel/Downloads/numerical/part5c.png', bbox_inches='tight')
