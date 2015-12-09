from __future__ import division
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

g = 9.81
hill_function = lambda x: 1000*np.exp(-(4800-x)**2/1000000)
rho = lambda y: max(-4.75/10**8*y + 2.0/10**4, 0)

def fire(initial_coordinates, angle, velocity, step_size):
  """
  accept initial conditions and step size
  return position, velocity at each step
  """
  angle_rad = angle*np.pi/180
  current_x_pos, current_y_pos = initial_coordinates
  current_x_vel, current_y_vel = np.cos(angle_rad)*velocity, np.sin(angle_rad)*velocity

  while current_y_pos >= hill_function(current_x_pos):
    current_x_pos += current_x_vel*step_size
    current_y_pos += current_y_vel*step_size

    p = rho(current_y_pos)
    d_v_x = -p*abs(current_x_vel)**2*step_size
    d_v_y = -(p*abs(current_y_vel)**2 + g)*step_size
    current_x_vel += d_v_x
    current_y_vel += d_v_y
    yield [current_x_pos, current_y_pos]

gen = fire((0, hill_function(0)), 45, 350, 0.1)
result = [step for step in gen]

fig = plt.figure()
ax = fig.add_subplot(111)
x, y = zip(*result)
ax.plot(x, y, label='flight path')

xh = np.arange(0, max(x), 0.1)
yh = hill_function(xh)

ax.plot(xh, yh, label='hill profile')
ax.legend(
  loc='upper center',
  bbox_to_anchor=(0.5, -0.1),
  fancybox = True,
  ncol = 3
)

ax.set_ylabel('y')
ax.set_xlabel('x')
ax.set_title(r'Example flight path for ${\theta}$=45$^\circ$')

ax.annotate('collision ({}, {})'.format(round(x[-1], 1), round(y[-1], 1)), xy=(x[-1], y[-1]), xytext=(x[-1]-5000, y[-1]+600),
    arrowprops=dict(facecolor='black', shrink=0.05),
    )
fig.savefig('test.png', bbox_inches='tight')
plt.show()
