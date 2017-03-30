import numpy as np
import matplotlib.pyplot as plt
import pdb
from scipy.optimize import fsolve

epsilon = 1e-3

# This function describes state as a function of the 
# parameter vector p and the arclength s
def calc_f( p, s, plot=False ):
    s = np.arange(0, s, epsilon)
    u = p[0] + s*(p[1] + s*(p[2] + s*(p[3])))

    k = u 
    theta = np.cumsum(k)*epsilon 
    x = np.cumsum(np.cos(theta))*epsilon 
    y = np.cumsum(np.sin(theta))*epsilon 
    if(plot):
        plt.plot(x, y)
        plt.show()

    return np.array([x[-1],y[-1],theta[-1],k[-1]])

def boundary_function_g(q, x0, xd):
    (p, sf) = q
    h = calc_f(p, sf) + x0
    g = h-xd
    return g

def cost_function_J(q):
    (p, sf) = q
    s = np.arange(0, sf, epsilon)
    k = p[0] + s*(p[1] + s*(p[2] + s*p[3]))

    sum_squares = 0.5*np.sum(k*k)
    return sum_squares 

def calc_L(params, x0, xd):
    p = params[0:4]
    sf = params[4]
    l_mult = params[5] 
    q = (p, sf)
    return cost_function_J(q) - l_mult*boundary_function_g(q, x0, xd)

def grad_L(params, x0, xd):
    grad = np.zeros((1, len(params)))
    
    for p_idx in range(0, len(params)):
        center = calc_L(params, x0, xd)
        perturbed_params = params
        params[p_idx] += epsilon
        plus = calc_L(params, x0, xd)
        pdb.set_trace()
        grad[p_idx] = (plus-center)/epsilon
    return grad
        


p = [0, 33, -82, 41.5, 1.1, 0]

x0 = [0, 0, 3.1415/2.0, 10]
xd = [0.70102248, 0.52060821, -1.22559075, -7.68353244]; 


p_opt = fsolve(grad_L, p, (x0, xd))

calc_f(p_opt, 1.1, plot=True)










