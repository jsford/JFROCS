import numpy as np
import matplotlib.pyplot as plt
import pdb

epsilon = 1e-3

# This function describes state as a function of the 
# parameter vector p and the arclength s
def calc_f( p, s ):
    s = np.arange(0, s, epsilon)
    u = p[0] + s*(p[1] + s*(p[2] + s*(p[3])))

    k = u 
    theta = np.cumsum(k)*epsilon 
    x = np.cumsum(np.cos(theta))*epsilon 
    y = np.cumsum(np.sin(theta))*epsilon 
    plt.plot(x, y)

    return np.array([x[-1],y[-1],theta[-1],k[-1]])

# This function describes the change in state as a function of the 
# parameter vector p and the arclength s
def calc_f_dot( p, s ):
    s = np.arange(0, s, epsilon)
    u = p[0] + s*(p[1] + s*(p[2] + s*(p[3])))

    k = s*(p[1] + 2*s*(p[2] + 3*s*(p[3])))
    theta = u 
    x = np.cos(theta) 
    y = np.sin(theta) 

    return np.array([x[-1],y[-1],theta[-1],k[-1]])

# The boundary condition is that the final posture should be the same as xb, the
# as xb, the boundary posture
def boundary_conditions_g(q, xb):
    return calc_f(q[0], q[1]) - xb


def cost_function_J(q, xd):
    sum = 0
    for s in np.arange(epsilon, q[1], 1000*epsilon):
        xf = calc_f(q[0], s)
        sum += xf[0] + xf[1] + xf[2]*1000*epsilon + xf[3]*1000*1000*epsilon*epsilon
    return sum/2.0 

p = [0, 33, -82, 41.5]
xb = [0.70102248, 0.52060821, -1.22559075, -7.68353244]; 


p1 = np.arange(32, 34, .1)
g = []
J = []

for new_p in p1:
    p[1] = new_p 
    g.append(boundary_conditions_g([p, 1.1], xb))
    J.append(cost_function_J([p, 1.1], xb))

plt.show()
plt.plot(p1,g)
plt.show()










