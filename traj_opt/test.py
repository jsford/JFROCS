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
def get_state(q, plot=False, color='black'):
    s = arange(0, q[0], epsilon)
    k = polyval(q[1:POLY_DEG+1], s)

    theta = cumsum(k)*epsilon 
    x = cumsum(cos(theta))*epsilon 
    y = cumsum(sin(theta))*epsilon 
    if(plot):
        plt.plot(x, y, color)

    return array([x[-1],y[-1],theta[-1],k[-1]])

# Estimate the arclength and polynomial coefficients required to 
# get from x0 = [0,0,0,0] to xf
def init_params(xf):
    
    # Convenient renaming
    tf = xf[2];
    kf = xf[3];


    # This vector will hold 
    # [sf, p_1, p_2, ..., p_n]
    params = zeros((POLY_DEG+1, ))

    # Estimate the arclength from x0 to xf
    rad = sqrt(xf[0]**2 + xf[1]**2)     # Crow-flies dist. from x0 to xf
    sf = rad * ( ( xf[2]**2 )/5 + 1 )   # Tianyu is adding 2*abs(theta)/5 here. Don't know why.

    params[0] = sf

    # Estimate the polynomial params to get from x0 to xf
    # I don't understand this, and I don't see where in the paper it is justified.
    k0 = 0
    params[1] = k0
    params[2] = 6*tf/sf**2 - 4*k0/sf - 2*kf/sf 
    params[3] = 3*(k0+kf)/sf**2 - 6*tf/sf**3
    params[4] = 0

    return params


def calc_Jacobian(q):
    j = zeros((4,4))                # This will become the jacobian
    N = 100;

    sf = q[0]                       # For convenience

    w = 0; s = 0; f = 0; g = 0;
    theta = 0; k = 0;
    x1 = 0; x2 = 0; x3 = 0;
    y1 = 0; y2 = 0; y3 = 0;
            
    for i in range(0, N+1):         # N+1 to match Tianyu. I think it's a bug.
        if (i==0 or i== N):
            w = 1
        elif (i%2 == 1):
            w = 4
        else:
            w = 2
        
        s = sf*i/float(N-1)
        # GetBiasThetaByS
        theta = polyval(array([0, q[1], q[2]/2.0, q[3]/3.0, q[4]/4.0]), sf)
        f = cos(theta)
        g = sin(theta)
        x1 += w*g*s**2
        x2 += w*g*s**3
        x3 += w*g*s**4
        y1 += w*f*s**2
        y2 += w*f*s**3
        y3 += w*f*s**4

    x1 *= sf/(3*N); x2 *= sf/(3*N); x3 *= sf/(3*N);
    y1 *= sf/(3*N); y2 *= sf/(3*N); y3 *= sf/(3*N);

    # GetBiasThetaByS
    theta = polyval(array([0, q[1], q[2]/2.0, q[3]/3.0, q[4]/4.0]), sf)
    k     = polyval(q[1:4], sf)

    j[0,0] = -x1/2.0;      j[0,1] = -x2/3.0;      j[0,2] = -x3/4.0;      j[0,3] = cos(theta);
    j[1,0] =  y1/2.0;      j[1,1] =  y2/3.0;      j[1,2] =  y3/4.0;      j[1,3] = sin(theta);
    j[2,0] = (sf**2)/2.0;  j[2,1] = (sf**3)/3.0;  j[2,2] = (sf**4)/4.0;  j[2,3] = k;
    j[3,0] = sf;           j[3,1] = sf**2;        j[3,2] = sf**3;        j[3,3] = q[1]+2*q[2]*sf+3*q[3]*sf**2;

    return j


# If x0 and x1 represent identical vehicle states, return True. 
# Else, return False.
def same_state(x0, x1):
    if  ( (abs(x0[0]-x1[0]) > 0.001) ): return False
    elif( (abs(x0[1]-x1[0]) > 0.001) ): return False
    elif( (abs(mod(x0[2]-x1[2], 2*pi)) >  0.01) ): return False
    elif( (abs(x0[3]-x1[3]) > 0.005) ):            return False
    else:
        return True

def optimize_params(xf):

    # Normalize the final heading to [0, 2*pi)
    theta1 = (xf[2]+2*pi) % (2*pi)
    theta2 =  theta1-2*pi
    if (abs(theta1) <= abs(theta2)):
        xf[2] = theta1
    else:
        xf[2] = theta2

    temp_p = init_params(xf)

    temp_x = get_state(temp_p)
    
    i = 0
    while not same_state(temp_x, xf):
        if(i > 20):
            disp('Reached Iteration limit. Stopping.')
            break
        jacobi = calc_Jacobian(temp_p) 

        param = temp_x-xf
        delta = dot(linalg.inv(jacobi), param)

        temp_p[0] -= delta[3]       # Arclength
        temp_p[1] -= delta[0]       # p0
        temp_p[2] -= delta[1]       # p1
        temp_p[3] -= delta[2]       # p2

        if(temp_p[0] < 0 or temp_p[0] > 3*sqrt(xf[0]**2+xf[1]**2)):
            temp_p[0] = sqrt(xf[0]**2+xf[1]**2)
            temp_p[1] = 0
            temp_p[2] = 0
            temp_p[3] = 0

        temp_x = get_state(temp_p)
        print temp_x
        exit()
        i += 1

    return temp_p
        
    
    

# sf, p
#q = array([1.1, 0, 33, -82, 41.5])

# [X, Y, T, K]
#xd = array([0.70102248, 0.52060821, -1.22559075, -7.68353244]);
xd2 = array([10,6,0,0])

param_guess = optimize_params(xd2)

get_state(param_guess[0:5], plot=True, color='red') 
#get_state(q, plot=True, color='blue') 

plt.show()
