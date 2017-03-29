import numpy as np
import matplotlib.pyplot as plt
import pdb

epsilon = 1e-5

def forward_dynamics( p, s ):
    s = np.arange(0, s, epsilon)
    u = p[0] + s*(p[1] + s*(p[2] + s*(p[3])))
    k = u
    theta = np.cumsum(k)*epsilon
    x = np.cumsum(np.cos(theta))*epsilon
    y = np.cumsum(np.sin(theta))*epsilon

    plt.plot(x, y, 'red')
    plt.show()

    return np.array([x[-1],y[-1],theta[-1],k[-1]])

def boundary_conditions_h(p, s):
    return forward_dynamics(p, 0) + forward_dynamics(p, s)
     
    
def boundary_conditions_g(p, s, xb):
    return boundary_conditions_h(p, s) - xb
    

print forward_dynamics( np.array([0,33,-82,41.5]), 1.1)
