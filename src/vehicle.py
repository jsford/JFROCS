from OpenGL.GL import *
from OpenGL.GLU import *

from math import *
from draw import *

class Vehicle:
    def __init__(self, name, texture_fname, pos=(0,0), theta_rad=0, width_m=1.75):
        self.name = name
        self.pos = pos
        self.theta_rad = theta_rad      # theta = 0 is facing North. (+) is counter-clockwise.
        self.width_m = width_m

    def get_pos(self):
        return self.pos
    
    def get_heading(self):
        return self.theta_rad

    def render(self):

        # Make the car twice as long as it is wide
        (hw, hh) = (self.width_m/2.0, self.width_m)

        p1 = ( hw,  hh)     # Top right
        p2 = (-hw,  hh)     # Top left
        p3 = (-hw, -hh)     # Bottom right
        p4 = ( hw, -hh)     # Bottom left)
        p5 = (  0,  hh)     # Top Middle

        glColor4f(*PASTEL_BLUE)
    
        glBegin(GL_QUADS)
        glVertex2f(*p1)     # Top right
        glVertex2f(*p2)     # Top left
        glVertex2f(*p3)     # Bottom left
        glVertex2f(*p4)     # Bottom right
        glEnd()

        glBegin(GL_TRIANGLES)
        glColor4f(*PASTEL_RED)
        glVertex2f(*p3)     # Bottom left
        glVertex2f(*p4)     # Bottom right
        glVertex2f(*p5)     # Top middle
        glEnd()
        
        return

