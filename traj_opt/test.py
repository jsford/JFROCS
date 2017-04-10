#!/usr/bin/python

import matplotlib.pyplot as plt
import matplotlib.colors
import seaborn as sns
import pdb
from numpy import *
from scipy.optimize import fsolve

epsilon = 1e-3
POLY_DEG = 4

# Uses Horner's Method to evaluate a polynomial 
# with a given set of coefficients at a given set of points.
# coeffs = [p0, p1, ..., pn]
# samples = [t0, t1, ..., tm]
# return:   p0 + p1*samples + p2*samples^2 + ...
def polyval(coeffs, samples):
    vals = samples*coeffs[-1]
    for i in range(coeffs.size-2, 0, -1):
        vals = samples*(vals+coeffs[i])
    vals += coeffs[0]
    return vals

# This function returns a 4xNUM_POINTS array
# where each column is an [x,y,theta,k]' coordinate
# representing a point along the trajectory described
# by q.
# Note: q = [sf, p]
def plot_state(q, x0, NUM_POINTS=1000):

    sf = q[0]

    plot_x     = zeros((NUM_POINTS, ))
    plot_y     = zeros((NUM_POINTS, ))
    plot_theta = zeros((NUM_POINTS, ))
    plot_k     = zeros((NUM_POINTS, ))

    sk    = 0; k        = 0;
    x     = 0; y        = 0;
    dx    = 0; dy       = 0; 
    dx1   = 0; dy1      = 0;
    theta = 0; theta1   = 0;

    for i in range(0, NUM_POINTS):
        sk = i*sf/(NUM_POINTS)

        k  = polyval(q[1:], sk) 
        
        if(i==0):
            x = 0;
            y = 0;
            theta = 0;
            dx1   = 0;
            dy1   = 0;
            theta1 = theta;
        else:
            theta = polyval(array([0, q[1], q[2]/2.0, q[3]/3.0, q[4]/4.0]), sk)
            dx = dx1*(i-1)/i + (cos(theta) + cos(theta1))/(2*i)
            dy = dy1*(i-1)/i + (sin(theta) + sin(theta1))/(2*i)
            x  = sk*dx
            y  = sk*dy

            dx1 = dx
            dy1 = dy
            theta1 = theta
        
        plot_x[i]     = cos(x0[2])*x-sin(x0[2])*y+x0[0]
        plot_y[i]     = cos(x0[2])*y+sin(x0[2])*x+x0[1]
        plot_theta[i] = theta+x0[2]
        plot_k[i]     = sk
    
    return vstack((plot_x, plot_y, plot_theta, plot_k)) 

# This function does the forward dynamics to find the state
# as a function of the coefficient vector p and the arclength s
# Note: q = [sf, p]
def get_state(q, NUM_POINTS=1000):
    temp_x = zeros((4,))

    sf = q[0]                       # For convenience

    w = 0; s = 0; f = 0; g = 0;
    x = 0; y = 0;
    theta = 0;

    for i in range(0, NUM_POINTS+1):
        if ( i==0 or i==NUM_POINTS):
            w = 1
        elif ( i%2 == 1 ):
            w = 4
        else:
            w = 2
        
        s = sf*i/(NUM_POINTS-1) 
        theta = polyval(array([0, q[1], q[2]/2.0, q[3]/3.0, q[4]/4.0]), s)
        f = cos(theta)
        g = sin(theta)
        x += w*f
        y += w*g

    x *= sf/(3*NUM_POINTS)
    y *= sf/(3*NUM_POINTS)

    temp_x[0] = x
    temp_x[1] = y
    temp_x[2] = polyval(array([0, q[1], q[2]/2.0, q[3]/3.0, q[4]/4.0]), sf) % (2*pi)
    temp_x[3] = polyval(q[1:], sf) 

    # Normalize theta to [-pi, pi]
    theta1 = (temp_x[2]+2*pi) % (2*pi)
    theta2 = theta1 - 2*pi
    
    if( abs(theta1) <= abs(theta2) ):
        temp_x[2] = theta1
    else:
        temp_x[2] = theta2

    return temp_x


# Estimate the arclength and polynomial coefficients required to 
# get from x0 = [0,0,0,0] to xf
def init_params(x0, xf):
    
    # Convenient renaming
    t0 = x0[2]; tf = xf[2];
    k0 = x0[3]; kf = xf[3];

    # This vector will hold 
    # [sf, p_1, p_2, ..., p_n]
    params = zeros((POLY_DEG+1, ))

    # Estimate the arclength from x0 to xf
    rad = sqrt((x0[0] - xf[0])**2 + (x0[1] - xf[1])**2)     # Crow-flies dist. from x0 to xf
    sf = rad * ( ( xf[2]**2 )/5 + 1 )   # Tianyu is adding 2*abs(theta)/5 here. Don't know why.

    params[0] = sf

    # Estimate the polynomial params to get from x0 to xf
    # I don't understand this, and I don't see where in the paper it is justified.
    params[1] = k0
    params[2] = 6*tf/sf**2 - (2*kf+4*k0)/sf 
    params[3] = 3*(k0+kf)/sf**2 - 6*tf/sf**3
    params[4] = 0

    return params


def calc_Jacobian(q, NUM_POINTS=100):
    j = zeros((4,4))                # This will become the Jacobian

    sf = q[0]                       # For convenience

    w = 0; s = 0; f = 0; g = 0;
    theta = 0; k = 0;

    x1 = 0; x2 = 0; x3 = 0;
    y1 = 0; y2 = 0; y3 = 0;
            
    for i in range(0, NUM_POINTS+1):         # NUM_POINTS+1 to match Tianyu. I think it's a bug.
        if (i==0 or i == NUM_POINTS):
            w = 1
        elif (i%2 == 1):
            w = 4
        else:
            w = 2
        
        s = sf*i/float(NUM_POINTS-1)
        theta = polyval(array([0, q[1], q[2]/2.0, q[3]/3.0, q[4]/4.0]), s) % (2*pi)
        f = cos(theta)
        g = sin(theta)

        x1 += w*g*s**2
        y1 += w*f*s**2

        x2 += w*g*s**3
        y2 += w*f*s**3

        x3 += w*g*s**4
        y3 += w*f*s**4
    

    x1 *= sf/(3.0*NUM_POINTS); x2 *= sf/(3.0*NUM_POINTS); x3 *= sf/(3.0*NUM_POINTS);
    y1 *= sf/(3.0*NUM_POINTS); y2 *= sf/(3.0*NUM_POINTS); y3 *= sf/(3.0*NUM_POINTS);

    # GetBiasThetaByS
    theta = polyval(array([0, q[1], q[2]/2.0, q[3]/3.0, q[4]/4.0]), sf) % (2*pi)
    k     = polyval(q[1:], sf)


    j[0,1] = -x1/2.0;      j[0,2] = -x2/3.0;      j[0,3] = -x3/4.0;      j[0,0] = cos(theta);
    j[1,1] =  y1/2.0;      j[1,2] =  y2/3.0;      j[1,3] =  y3/4.0;      j[1,0] = sin(theta);
    j[2,1] = (sf**2)/2.0;  j[2,2] = (sf**3)/3.0;  j[2,3] = (sf**4)/4.0;  j[2,0] = k;
    j[3,1] = sf;           j[3,2] = sf**2;        j[3,3] = sf**3;        j[3,0] = q[2]+2*q[3]*sf+3*q[4]*sf**2;

    return j


# If x0 and x1 represent identical vehicle states, return True. 
# Else, return False.
def same_state(x0, x1):
    if  ( (abs(x0[0]-x1[0]) <= 0.001) and 
          (abs(x0[1]-x1[1]) <= 0.001) and
          (abs( (x0[2]-x1[2]) % (2*pi) ) <=  0.01) and
          (abs(x0[3]-x1[3]) <= 0.005) ): return True
    else:
        return False

def optimize_params(x0, xf, backstep=True):

    # Normalize the final heading to [-pi, pi]
    theta1 = (xf[2]+2*pi) % (2*pi)
    theta2 =  theta1-2*pi
    if (abs(theta1) <= abs(theta2)):
        xf[2] = theta1
    else:
        xf[2] = theta2

    temp_p = init_params(x0, xf)

    temp_x = get_state(temp_p)
    
    last_dist = linalg.norm(xf-temp_x)

    iteration = 0
    while not same_state(temp_x, xf):
        if(iteration >= 20):
            disp('Reached Iteration limit. Stopping.')
            break

        jacobi = calc_Jacobian(temp_p, NUM_POINTS=100) 

        param = xf-temp_x
        delta = dot(linalg.inv(jacobi), param)

        # Forward step by delta
        temp_p[0] += delta[0]       # Arclength
        temp_p[1] += 0              # p0 stays the same
        temp_p[2] += delta[1]       # p1
        temp_p[3] += delta[2]       # p2
        temp_p[4] += delta[3]       # p3


        temp_x = get_state(temp_p)

        # If the path has gotten too long or too short, reset and try again
        # Not totally sure what the effect of this is... Seems like we should
        # try again with something similar, but different from our initial guess?
        # This seems like it will give up to me.
        if(temp_p[0] < 0 or temp_p[0] > 3*sqrt(xf[0]**2+xf[1]**2)):
            temp_p[0] = sqrt(xf[0]**2+xf[1]**2)
            temp_p[1] = 0
            temp_p[2] = 0
            temp_p[3] = 0
            temp_p[4] = 0

        # See Section 5. of RootFindingMethods.pdf for a discussion of 
        # backstepping. Basically, if you overshot the goal, 
        # back off by half until you get closer.
        elif (backstep == True):
            backstep_count = 0
            while(backstep_count < 4 ):
                # If you went too far, reduce delta to delta/2.0
                dist = linalg.norm(temp_x)
                if( linalg.norm(xf-temp_x) > last_dist ):
                    delta /= 2.0
                    temp_p[0] -= delta[0]       # Arclength
                    temp_p[1] -= 0              # p0 stays the same
                    temp_p[2] -= delta[1]       # p1
                    temp_p[3] -= delta[2]       # p2
                    temp_p[4] -= delta[3]       # p3

                    backstep_count += 1
                    temp_x = get_state(temp_p)
                else:
                    break

        last_dist = linalg.norm(temp_x)
        iteration += 1
    
    return temp_p

# TODO: Try generalizing to any polynomial degree.
#       Try scipy.optimize instead of Tianyu's thing.        
    
x0 = array([0,0,0,0])
xd = array([10,6,-pi/8,0])


plot = plt.plot()
params = optimize_params(x0, xd)

plots = plot_state(params, x0)
plt.plot(plots[0,:], plots[1,:], color='red')
plt.xlim(0, 12)
plt.ylim(-2, 10)
sns.despine()
plt.show()

