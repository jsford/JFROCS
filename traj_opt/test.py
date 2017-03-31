#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import pdb
from scipy.optimize import fsolve

epsilon = 1e-3
POLY_DEG = 4

# This function describes state as a function of the 
# parameter vector p and the arclength s
def calc_f(q, plot=False ):
    s = np.arange(0, q[0], epsilon)
    u = q[1] + s*(q[2] + s*(q[3] + s*(q[4])))

    k = u 
    theta = np.cumsum(k)*epsilon 
    x = np.cumsum(np.cos(theta))*epsilon 
    y = np.cumsum(np.sin(theta))*epsilon 
    if(plot):
        plt.plot(x, y)

    return np.array([x[-1],y[-1],theta[-1],k[-1]])

def boundary_function_g(q, x0, xd):
    h = calc_f(q) + x0
    g = h-xd
    return g

# Change this to output a matrix 
# with (x,y,k,t)' on the side and (sf, p1, p2, p3, p4) on the top
def g_dq(q, x0, xd):
    grad = np.zeros((len(q), 4))
    for p_idx in range(0, len(q)):
        perturbed = q.copy()
        q[p_idx] += epsilon
        grad[p_idx,:] = np.transpose(boundary_function_g(q, x0, xd)
                         - boundary_function_g(perturbed, x0, xd))
    np.divide(grad, epsilon)
    return np.transpose(grad)

def cost_function_J(q):
    s = np.arange(0, q[0], epsilon)
    k = q[1] + s*(q[2] + s*(q[3] + s*q[4]))

    sum_squares = 0.5*np.sum(k*k)
    return sum_squares 

def J_dq(q):
    grad = np.zeros((1, len(q)))
    for p_idx in range(0, len(q)):
        perturbed = q.copy()
        perturbed[p_idx] += epsilon
        grad[:,p_idx] = (cost_function_J(q) - cost_function_J(perturbed))/epsilon
    return grad


def calc_L(params, x0, xd):
    l_mult = params[5] 
    return cost_function_J(q) + l_mult*boundary_function_g(q, x0, xd)


def grad_L(params, x0, xd):
    grad = np.zeros((1, len(params)))
    
    for p_idx in range(0, len(params)):
        center = calc_L(params, x0, xd)
        perturbed_params = params
        params[p_idx] += epsilon
        plus = calc_L(params, x0, xd)
        grad[p_idx] = (plus-center)/epsilon
    return grad


def init_sf(x0, xf):
    rad = np.sqrt((xf[0]-x0[0])**2 + (xf[1]-x0[1])**2)
    sf = rad * ( ( xf[2]**2 )/5 + 1 )
    return sf

# Could be improved to make a 3rd order guess by iteratively zeroing 
# one parameter and solving for the others. For now, it just sets all params
# but the first two to zero
def init_p(sf, x0, xf):
    t0 = x0[2]; tf = xf[2];
    k0 = x0[3]; kf = xf[3];

    dt = tf-t0
    dk = kf-k0

    init_p = np.zeros((POLY_DEG, 1))
    init_p[0] = 2*dt/sf - dk
    init_p[1] = (dk - init_p[0])/sf
            
    return init_p


# Need to solve lambdaT * dg_dq = -dJ_dq
# To find my set of starting lambdas
def init_lambda(q, x0, xf): 
    dg_dq = g_dq(q, x0, xf) 
    dJ_dq = J_dq(q)

    dg_dq_T_pinv = np.linalg.pinv(np.transpose(dg_dq))
    lambduh = np.dot( dg_dq_T_pinv , np.transpose(-dJ_dq) )
    return lambduh
    

# sf, p
q = [1.1, 0, 33, -82, 41.5]

x0 = [0, 0, 0, 0]
xd = [0.70102248, 0.52060821, -1.22559075, -7.68353244]; 


sf_guess = init_sf(x0, xd)
p_guess = init_p(sf_guess, x0, xd)
q_guess = np.insert(p_guess, 0, sf_guess)

lambda_guess = init_lambda(q_guess, x0, xd)

#p_opt = fsolve(grad_L, p, (x0, xd))


calc_f(q_guess, plot=True) 
calc_f(q, plot=True) 

plt.show()
