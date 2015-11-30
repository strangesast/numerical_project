# MA377 Project 5
import math

"""
g = 9.81 m / s^2 # gravity

v(t) # velocity of projectile at time t

a = -4.75e-8
b = 2.0e-4
rho(y) = a y + b # air pressure

air_friction = rho(y) abs( v(t) )^2

x'' = -rho(y) (x')^2
y'' = -rho(y) (y')^2 - g


h(x) = 1000 exp( 10e-6 (x - 4800)^2 ) # hill height over x

x_o = 0 # initial position
x_target = 5100 # target position

v_o = 350 m/s # initial muzzle velocity

1/2 m v_1^2 = 1/2 m v_0^2 + delta_kinetic + delta_potential 

delta_potential = m g delta_h
delta_kinetic = -drag_force

"""

# air pressure
def rho(y):
    a = -4.75e-8
    b = 2.0e-4
    return a*y + b




cos = math.cos
sin = math.sin

g = 9.81  # m / s^2
v_0 = 350 # m / s

x_0, y_0 = (0, 0) # m 
a = math.pi / 4   # rad

v_c = v_0
x_c = x_0
y_c = y_0

v_y = v_c*cos(a)
v_x = v_c*sin(a)

while y_c >= 0:
    #print('x_c: {}'.format(x_c))
    print('y_c: {}'.format(y_c))

    x_c += v_x
    y_c += v_y

    rho_c = rho(y_c) # current air pressure

    d_v_x = -rho_c*abs(v_x)**2
    d_v_y = -rho_c*abs(v_y)**2 - g

    v_x += d_v_x
    v_y += d_v_y

# air friction equal to
# rho (height) abs(velocity (time)) ^ 2
