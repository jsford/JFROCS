#!/usr/bin/python

import matplotlib.pyplot as plt
import pdb
from numpy import *
from scipy.optimize import fsolve

epsilon = 1e-3
POLY_DEG = 4

# This function describes state as a function of the 
# parameter vector p and the arclength s
# Inputs:          q    dim: (1, POLY_DEG+1)
# Output:   [x,y,t,k]   dim: (1, 4)
def calc_f(q, plot=False, color='black'):
    s = arange(0, q[0,0], epsilon)
    s = s[:, newaxis]
    u = q[0,1] + s*(q[0,2] + s*(q[0,3] + s*(q[0,4])))

    k = u 
    theta = cumsum(k)*epsilon 
    x = cumsum(cos(theta))*epsilon 
    y = cumsum(sin(theta))*epsilon 
    if(plot):
        plt.plot(x, y, color)

    return matrix([x[-1],y[-1],theta[-1],k[-1]])

def boundary_function_g(q, x0, xd):
    h = calc_f(q) + x0
    g = h-xd
    return g.reshape((1,POLY_DEG))

# Change this to output a matrix 
# with (x,y,k,t)' on the side and (sf, p1, p2, p3, p4) on the top
def g_dq(q, x0, xd):
    grad = zeros((len(q), 4))
    for p_idx in range(0, len(q)):
        perturbed = q.copy()
        q[p_idx] += epsilon
        tmp = transpose(boundary_function_g(q, x0, xd)
                         - boundary_function_g(perturbed, x0, xd))
        grad[p_idx,:] = tmp.reshape(4,)
    divide(grad, epsilon)
    return transpose(grad)

def cost_function_J(q):
    s = arange(0, q[0,0], epsilon)
    k = q[0,1] + s*(q[0,2] + s*(q[0,3] + s*q[0,4]))

    sum_squares = 0.5*sum(k*k)
    return sum_squares 

def J_dq(q):
    grad = zeros((1, len(q)))
    for p_idx in range(0, len(q)):
        perturbed = q.copy()
        perturbed[p_idx] += epsilon
        grad[:,p_idx] = (cost_function_J(q) - cost_function_J(perturbed))/epsilon
    return grad


def calc_L(params, x0, xd):
    q = params[0:POLY_DEG+1].reshape(1, POLY_DEG+1)
    l_mult = params[POLY_DEG+1:].reshape(4,1)
    return cost_function_J(q) +  boundary_function_g(q, x0, xd) * l_mult


def grad_L(params, x0, xd):
    grad = zeros((1, len(params)))
    
    for p_idx in range(0, len(params)):
        center = calc_L(params, x0, xd)
        perturbed_params = params
        params[p_idx] += epsilon
        plus = calc_L(params, x0, xd)
        grad[:, p_idx] = (plus-center)/epsilon
    return grad[0,:]


def init_sf(x0, xf):
    rad = sqrt((xf[0,0]-x0[0,0])**2 + (xf[0,1]-x0[0,1])**2)
    sf = rad * ( ( xf[0,2]**2 )/5 + 1 )
    return sf

# Could be improved to make a 3rd order guess by iteratively zeroing 
# one parameter and solving for the others. For now, it just sets all params
# but the first two to zero
# Input:    sf      scalar
#           x0      matrix  (1, 4)
#           xf      matrix  (1, 4)
# Output:   init_p  matrix  (1, POLY_DEG)
def init_p(sf, x0, xf):
    t0 = x0[0,2]; tf = xf[0,2];
    k0 = x0[0,3]; kf = xf[0,3];

    dt = tf-t0
    dk = kf-k0

    init_p = zeros((1, POLY_DEG))
    init_p[0,0] = 2*dt/sf - dk
    init_p[0,1] = (dk - init_p[0,0])/sf
            
    return init_p


# Need to solve lambdaT * dg_dq = -dJ_dq
# To find my set of starting lambdas
def init_lambda(q, x0, xf): 
    dg_dq = g_dq(q, x0, xf) 
    dJ_dq = J_dq(q)

    dg_dq_T_pinv = linalg.pinv(transpose(dg_dq))
    lambduh = dg_dq_T_pinv * transpose(-dJ_dq)
    return lambduh.reshape(1,4)
    

# sf, p
q = matrix([1.1, 0, 33, -82, 41.5])

x0 = zeros((1, POLY_DEG)) 
xd = matrix([0.70102248, 0.52060821, -1.22559075, -7.68353244]);


sf_guess = init_sf(x0, xd)
p_guess = init_p(sf_guess, x0, xd)
q_guess = insert(p_guess, 0, sf_guess)
q_guess = q_guess[newaxis, :]           # Enforce row vector

lambda_guess = init_lambda(q_guess, x0, xd)
param_guess = concatenate((q_guess, lambda_guess), axis=1)

q_opt = fsolve(grad_L, param_guess, (x0, xd)).reshape(1, POLY_DEG+1+4)


calc_f(q_guess, plot=True, color='red') 
calc_f(q, plot=True, color='blue') 
calc_f(q_opt, plot=True, color='green') 

plt.show()
