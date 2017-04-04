#!/usr/bin/python

import matplotlib.pyplot as plt
import pdb
from numpy import *
from scipy.optimize import fsolve

epsilon = 1e-3
POLY_DEG = 4
CONSTRAINTS = 4

# Uses Horner's Method to evaluate a polynomial 
# with a given set of coefficients at a given set of points.
def polyval(coeffs, samples):
    vals = samples*coeffs[-1]
    for i in range(coeffs.size-2, 0, -1):
        vals = samples*(vals+coeffs[i])
    vals += coeffs[0]
    return vals

# This function does the forward dynamics to find the state
# as a function of the coefficient vector p and the arclength s
# Note: q = [sf, p]
def calc_f(q, plot=False, color='black'):
    s = arange(0, q[0], epsilon)
    k = polyval(q[1:POLY_DEG+1], s)

    theta = cumsum(k)*epsilon 
    x = cumsum(cos(theta))*epsilon 
    y = cumsum(sin(theta))*epsilon 
    if(plot):
        plt.plot(x, y, color)

    return array([x[-1],y[-1],theta[-1],k[-1]])

def boundary_function_g(q, x0, xd):
    return (calc_f(q) + x0) - xd 

def g_dq(q, x0, xd):
    grad = zeros((q.size, 4))
    for p_idx in range(0, q.size):
        perturbed = q.copy()
        perturbed[p_idx] += epsilon
        tmp = transpose(boundary_function_g(q, x0, xd)
                         - boundary_function_g(perturbed, x0, xd))
        grad[p_idx,:] = tmp.reshape(4,)
    divide(grad, epsilon)
    return transpose(grad)

def cost_function_J(q):
    s = arange(0, q[0], epsilon)
    k = polyval(q[1:POLY_DEG+1], s)

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
    q = params[0:POLY_DEG+1].reshape(POLY_DEG+1,)
    l_mult = params[POLY_DEG+1:].reshape(4,1)
    return cost_function_J(q) + dot(boundary_function_g(q, x0, xd), l_mult)


def grad_L(params, x0, xd):
    grad = zeros((len(params), ))
    
    for p_idx in range(0, len(params)):
        center = calc_L(params, x0, xd)
        perturbed_params = params
        params[p_idx] += epsilon
        plus = calc_L(params, x0, xd)
        grad[p_idx] = (plus-center)/epsilon
    return grad

def init_params(xf):
    
    # Enforce the starting coordinate to be
    # [x,y,theta,k] = [0,0,0,0]
    x0 = zeros((1, 4)).reshape((4, ))

    # Normalize the final heading to [0, 2*pi)
    theta1 = (xf[2]+2*pi) % (2*pi)
    theta2 =  theta1-2*pi
    if (abs(theta1) <= abs(theta2)):
        xf[2] = theta1
    else:
        xf[2] = theta2

    # This vector will hold 
    # [sf, p_1, p_2, ..., p_n, lambda_1, ...., lambda_m]
    # It will be used in the Lagrange Multiplier step
    params = zeros((POLY_DEG+CONSTRAINTS+1, ))

    # Estimate the arclength from x0 to xf
    rad = sqrt(xf[0]**2 + xf[1]**2)
    sf = rad * ( ( xf[2]**2 )/5 + 1 )   # Tianyu is adding 2*abs(theta)/5 here. Don't know why.

    params[0] = sf

    # Estimate the polynomial params to get from x0 to xf
    t0 = x0[2]; tf = xf[2];
    k0 = x0[3]; kf = xf[3];

    dt = tf-t0
    dk = kf-k0

    #params[1] = 2*dt/sf - dk
    #params[2] = (dk - params[1])/sf
    #params[3:POLY_DEG+1] = 0

    params[1] = k0
    params[2] = 6*tf/sf**2 - 4*k0/sf - 2*kf/sf 
    params[3] = 3*(k0+kf)/sf**2 - 6*tf/sf**3
    params[4] = 0

    # Estimate the lagrange multipliers
    dg_dq = g_dq(params[0:POLY_DEG+1], x0, xf) 
    dJ_dq = J_dq(params[0:POLY_DEG+1])

    dg_dq_T_pinv = linalg.pinv(transpose(dg_dq))
    lambduh = dot(dg_dq_T_pinv, transpose(-dJ_dq)).reshape((CONSTRAINTS,))
    
    params[-lambduh.size:] = lambduh

    return params

# sf, p
q = array([1.1, 0, 33, -82, 41.5])

# [X, Y, T, K]
xd = array([0.70102248, 0.52060821, -1.22559075, -7.68353244]);

param_guess = init_params(xd)

#q_opt = fsolve(grad_L, param_guess, (x0, xd)).reshape(1, POLY_DEG+1+4)


calc_f(param_guess[0:5], plot=True, color='red') 
calc_f(q, plot=True, color='blue') 
#calc_f(q_opt, plot=True, color='green') 

plt.show()
