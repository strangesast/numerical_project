# MA377 Project 5
from __future__ import division
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

g = 9.81

def hill_function(x):
    return 1000*np.exp(-(4800-x)**2/1000000)


def airdensity_function(y):
    val = -4.75/10**8*y + 2.0/10**4
    return val if val > 0 else 0


def fire(initial_coordinates, angle, velocity, step_size):
  angle_rad = 1/2*np.pi - angle*np.pi/180;
  current_x_pos, current_y_pos = initial_coordinates

  current_x_vel = np.sin(angle_rad)*velocity;
  current_y_vel = np.cos(angle_rad)*velocity;

  ret = [];
  last_x = current_x_pos;
  last_y = current_y_pos;

  while current_y_pos >= hill_function(current_x_pos):
    current_x_pos += current_x_vel*step_size;
    current_y_pos += current_y_vel*step_size;

    d_v_x = -airdensity_function(current_y_pos)*abs(current_x_vel)**2*step_size;
    d_v_y = -(airdensity_function(current_y_pos)*abs(current_y_vel)**2 + g)*step_size;

    current_x_vel += d_v_x;
    current_y_vel += d_v_y;

    ret = [current_x_pos, current_y_pos, current_x_vel, current_y_vel];

    last_x = current_x_pos;
    last_y = current_y_pos;

    yield ret;

start = (0, hill_function(0))
targetx = 5100
target = (targetx, hill_function(targetx))

targets = np.arange(100, 9000, 100)
angles = np.arange(0, 90, 0.1)

def hit_range(t, hit):
    return np.sqrt((t[0] - hit[0])**2 + (t[1] - hit[1])**2)


def return_hit(angle, velocity):
    """ return coordinates of projectile collision with hill
    """
    # initialize shot with 'start' coordinates, muzzle 'angle', muzzle 'velocity', and step size
    gen = fire(start, angle, velocity, 0.1)
    # calcualte position of projectile until break conditions are met
    # (y_position < hill_height) and return the last position (where 
    # it hit the dirt).  take only the first two values (x, y position)
    return [step for step in gen][-1][:2]

def test(targetx, angle):
    """ accept target x position and calculate is position on the hill
    """
    # initialize target at 'targetx' and corresponding location on hill
    target = (targetx, hill_function(targetx))

    # use 'return_hit' function to determine hit coordinates with given angle and velocity
    hit = return_hit(angle, 350)
    return hit_range(target, hit)

test = np.vectorize(test)


def plot_ranges():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ranges = np.zeros(angles.shape)
    for i, angle in enumerate(angles):
        hit = return_hit(angle, 350)
        ranges[i] = hit_range(target, hit)
    
    ax.plot(angles, ranges)
    ax.set_ylabel('Range (m)')
    ax.set_xlabel(r'Angle $\alpha$ ($^\circ$)')
    ax.set_title(r'Range within 5100m over 0$^\circ$ < $\alpha$ < 90$^\circ$')
    
    root1, root2 = list(np.sort(ranges)[:2])
    rangeslist = list(ranges)
    
    root1y = angles[rangeslist.index(root1)]
    root2y = angles[rangeslist.index(root2)]
    
    for xi, yi in [(root1y, root1), (root2y, root2)]:
        ax.annotate(r'root: ({}$^\circ$, {})'.format(round(xi, 2), round(0)), xy=(xi, yi), xytext=(xi, yi+3000),
            arrowprops=dict(facecolor='black', shrink=0.05)
            )
    
    
    fig.savefig('/home/samuel/Downloads/roots.png')
    #plt.show()

def plot_surface():
    targets = np.arange(100, 6000, 100)
    angles = np.arange(0, 90, 1)
    targets, angles = np.meshgrid(targets, angles)
    z = test(targets, angles)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    #X = np.arange(-5, 5, 0.25)
    #Y = np.arange(-5, 5, 0.25)
    #X, Y = np.meshgrid(X, Y)
    #R = np.sqrt(X**2 + Y**2)
    #Z = np.sin(R)
    surf = ax.plot_surface(targets, angles, z, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    #ax.set_zlim(-1.01, 1.01)
    
    #ax.zaxis.set_major_locator(LinearLocator(10))
    #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    
    ax.set_xlabel('Target Location (m)')
    ax.set_ylabel(r'Angle ($^\circ$)')
    ax.set_zlabel('Range (m)')
    ax.set_title('Projectile Range Surface Plot')
    fig.colorbar(surf, shrink=0.5, aspect=5)
    
    fig.savefig('/home/samuel/Downloads/test.png')
    plt.show()

plot_surface()
