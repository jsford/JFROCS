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


class VehicleState:
    def __init__(self, x, y, theta, k, v, a):
        self.x = x
        self.y = y
        self.theta = theta
        self.k = k
        self.v = v
        self.a = a

    def posvec(self):
        return array([self.x, self.y, self.theta, self.k])
    def velvec(self):
        return array([self.v, self.a])


class Trajectory:
    def __init__(self, vs0, vsf, NUM_POINTS=1000):
        self.vs0 = vs0
        self.vsf = vsf
        self.tf = -1;
        self.sf = -1;
        self.pos_params = zeros((4,))
        self.vel_params = zeros((4,))
        self.NUM_POINTS = NUM_POINTS

    # This function returns a 4xPLOT_POINTS array
    # where each column is an [x,y,theta,k]' coordinate
    # representing a point along the trajectory described
    # by q.
    # Note: q = [sf, p]
    def plot_state(self, PLOT_POINTS=1000):

        # For convenience
        p  = self.pos_params
        sf = self.sf 
        theta0 = self.vs0.theta

        plot_x     = zeros((PLOT_POINTS, ))
        plot_y     = zeros((PLOT_POINTS, ))
        plot_theta = zeros((PLOT_POINTS, ))
        plot_k     = zeros((PLOT_POINTS, ))

        sk        = 0; k            = 0;
        x         = 0; y            = 0;
        dx        = 0; dy           = 0; 
        prev_dx   = 0; prev_dy      = 0;
        theta     = 0; prev_theta   = 0;

        for i in range(0, PLOT_POINTS):
            sk = i*sf/(PLOT_POINTS-1)

            k  = polyval(p, sk) 
            
            if(i==0):
                x = 0;
                y = 0;
                theta = 0;
                prev_dx   = 0;
                prev_dy   = 0;
                prev_theta = 0;
            else:
                theta = polyval(array([0, p[0], p[1]/2.0, p[2]/3.0, p[3]/4.0]), sk)
                dx = prev_dx*(i-1)/i + (cos(theta) + cos(prev_theta))/(2*i)
                dy = prev_dy*(i-1)/i + (sin(theta) + sin(prev_theta))/(2*i)
                x  = sk*dx
                y  = sk*dy

                prev_dx = dx
                prev_dy = dy
                prev_theta = theta


            plot_x[i]     = cos(theta0)*x-sin(theta0)*y+self.vs0.x
            plot_y[i]     = cos(theta0)*y+sin(theta0)*x+self.vs0.y
            plot_theta[i] = theta+theta0
            plot_k[i]     = sk
        
        return vstack((plot_x, plot_y, plot_theta, plot_k)) 

    # This function does the forward dynamics to find the state
    # as a function of the coefficient vector p and the arclength s
    # Note: q = [sf, p]
    def get_state(self):
        temp_vs = VehicleState(0,0,0,0, -1,-1)

        # For convenience
        p = self.pos_params
        sf = self.sf

        w = 0; s = 0; f = 0; g = 0;
        x = 0; y = 0;
        theta = 0;

        for i in range(0, self.NUM_POINTS+1):
            if ( i==0 or i==self.NUM_POINTS):
                w = 1
            elif ( i%2 == 1 ):
                w = 4
            else:
                w = 2
            
            s = sf*i/(self.NUM_POINTS-1) 
            theta = polyval(array([0, p[0], p[1]/2.0, p[2]/3.0, p[3]/4.0]), s)
            f = cos(theta)
            g = sin(theta)
            x += w*f
            y += w*g

        x *= sf/(3*self.NUM_POINTS)
        y *= sf/(3*self.NUM_POINTS)

        temp_vs.x = x
        temp_vs.y = y
        temp_vs.theta = polyval(array([0, p[0], p[1]/2.0, p[2]/3.0, p[3]/4.0]), sf) % (2*pi)
        temp_vs.k = polyval(p, sf) 

        # Normalize theta to [-pi, pi]
        theta1 = (temp_vs.theta+2*pi) % (2*pi)
        theta2 = theta1 - 2*pi
        
        if( abs(theta1) <= abs(theta2) ):
            temp_vs.theta = theta1
        else:
            temp_vs.theta = theta2

        return temp_vs

    # Estimate the arclength and polynomial coefficients required to 
    # get from x0 = [0,0,0,0] to xf
    def init_params(self):
        
        # Convenient renaming
        t0 = self.vs0.theta; tf = self.vsf.theta;
        k0 = self.vs0.k;     kf = self.vsf.k;

        sf = self.sf

        # Estimate the arclength from x0 to xf
        rad = sqrt((self.vs0.x - self.vsf.x)**2 + (self.vs0.y - self.vsf.y)**2)     # Crow-flies dist. from x0 to xf
        self.sf = rad * ( ( tf**2 )/5 + 1 )

        # Estimate the polynomial params to get from x0 to xf
        # I don't understand this, and I don't see where in the paper it is justified.
        self.pos_params[0] = k0
        self.pos_params[1] = 6*tf/sf**2 - (2*kf+4*k0)/sf 
        self.pos_params[2] = 3*(k0+kf)/sf**2 - 6*tf/sf**3
        self.pos_params[3] = 0

    # If x0 and x1 represent identical vehicle states, return True. 
    # Else, return False.
    def same_state(self, x0, x1):
        if  ( (abs(x0[0]-x1[0]) <= 0.001) and 
              (abs(x0[1]-x1[1]) <= 0.001) and
              (abs( (x0[2]-x1[2]) % (2*pi) ) <=  0.01) and
              (abs(x0[3]-x1[3]) <= 0.005) ): return True
        else:
            return False

    def calc_Jacobian(self):
        j = zeros((4,4))                   # This will become the Jacobian

        # For convenience
        sf = self.sf                       
        p  = self.pos_params

        w = 0; s = 0; f = 0; g = 0;
        theta = 0; k = 0;

        x1 = 0; x2 = 0; x3 = 0;
        y1 = 0; y2 = 0; y3 = 0;
                
        for i in range(0, self.NUM_POINTS+1):         # NUM_POINTS+1 to match Tianyu. I think it's a bug.
            if (i==0 or i == self.NUM_POINTS):
                w = 1
            elif (i%2 == 1):
                w = 4
            else:
                w = 2
            
            s = sf*i/float(self.NUM_POINTS-1)
            theta = polyval(array([0, p[0], p[1]/2.0, p[2]/3.0, p[3]/4.0]), s) % (2*pi)
            f = cos(theta)
            g = sin(theta)

            x1 += w*g*s**2
            y1 += w*f*s**2

            x2 += w*g*s**3
            y2 += w*f*s**3

            x3 += w*g*s**4
            y3 += w*f*s**4
        

        x1 *= sf/(3.0*self.NUM_POINTS); x2 *= sf/(3.0*self.NUM_POINTS); x3 *= sf/(3.0*self.NUM_POINTS);
        y1 *= sf/(3.0*self.NUM_POINTS); y2 *= sf/(3.0*self.NUM_POINTS); y3 *= sf/(3.0*self.NUM_POINTS);

        # GetBiasThetaByS
        theta = polyval(array([0, p[0], p[1]/2.0, p[2]/3.0, p[3]/4.0]), sf) % (2*pi)
        k     = polyval(p, sf)

        # d?/dsf                                # d?/dp1
        j[0,0] = cos(theta);                    j[0,1] = -x1/2.0;       # dx/d?
        j[1,0] = sin(theta);                    j[1,1] =  y1/2.0;       # dy/d?
        j[2,0] = k;                             j[2,1] = (sf**2)/2.0;   # dtheta/d?
        j[3,0] = p[1]+2*p[2]*sf+3*p[3]*sf**2;   j[3,1] = sf;            # dk/d?

        # d?/dp2                                # d?/dp3
        j[0,2] = -x2/3.0;                       j[0,3] = -x3/4.0;       # dx/d?
        j[1,2] =  y2/3.0;                       j[1,3] =  y3/4.0;       # dy/d?
        j[2,2] = (sf**3)/3.0;                   j[2,3] = (sf**4)/4.0;   # dtheta/d?
        j[3,2] = sf**2;                         j[3,3] = sf**3;         # dk/d?

        return j

    def generate_pos_profile(self, backstep=True):

        # Normalize the final heading to [-pi, pi]
        theta1 = (self.vsf.theta+2*pi) % (2*pi)
        theta2 =  theta1-2*pi
        if (abs(theta1) <= abs(theta2)):
            self.vsf.theta = theta1
        else:
            self.vsf.theta = theta2

        # Generate an initial guess for the correct parameters
        self.init_params()
        
        # Plot the inital guess in purple
        plots = self.plot_state()
        plt.plot(plots[0,:], plots[1,:], color='purple')

        # Find out what vehicle state results with the initial parameter guess
        temp_vs = self.get_state()
        # See how far from the goal we are
        last_dist = linalg.norm(self.vsf.posvec()-temp_vs.posvec())

        # Iterate until we converge to the goal or run out the iteration clock
        iteration = 0
        while not self.same_state(temp_vs.posvec(), self.vsf.posvec()):
            if(iteration >= 20):
                disp('Reached Iteration limit. Stopping.')
                return False

            jacobi = self.calc_Jacobian() 

            param = self.vsf.posvec()-temp_vs.posvec()
            delta = dot(linalg.inv(jacobi), param)

            # Forward step by delta
            self.sf            += delta[0]       # Arclength
            self.pos_params[0] += 0              # p0 stays the same
            self.pos_params[1] += delta[1]       # p1
            self.pos_params[2] += delta[2]       # p2
            self.pos_params[3] += delta[3]       # p3

            temp_vs = self.get_state()

            # See Section 5. of RootFindingMethods.pdf for a discussion of 
            # backstepping line search. Basically, if you overshot the goal, 
            # back off by half until you get closer.
            if (backstep == True):
                backstep_count = 0
                while(backstep_count < 4 ):
                    # If you went too far, reduce delta to delta/2.0
                    dist = linalg.norm(self.vsf.posvec() - temp_vs.posvec())
                    if( dist > last_dist ):
                        delta /= 2.0
                        self.sf            -= delta[0]       # Arclength
                        self.pos_params[0] -= 0              # p0 stays the same
                        self.pos_params[1] -= delta[1]       # p1
                        self.pos_params[2] -= delta[2]       # p2
                        self.pos_params[3] -= delta[3]       # p3

                        backstep_count += 1
                        temp_vs = self.get_state()
                    else:
                        break

            last_dist = linalg.norm(self.vsf.posvec() - temp_vs.posvec())
            iteration += 1

        return True 

    
if __name__ == "__main__":

    # TODO: Non-zero theta0 seems to break it
    vs0 = VehicleState(0,0,0,0, 8,-1)
    vsf = VehicleState(1,1,0,0, 4, 0)

    traj = Trajectory(vs0, vsf)

    success = traj.generate_pos_profile()
    
    print traj.get_state().posvec()

    if success:
        plots = traj.plot_state()
        plt.plot(plots[0,:], plots[1,:], color='red')
        print plots[0,-1], plots[1,-1]

        plt.xlim(-2, 2)
        plt.ylim(-2, 2)
        sns.despine()
        plt.show()

    else:
        print "Failed to generate a trajectory."


