from OpenGL.GL import *
from OpenGL.GLU import *

from math import *
from draw import *

from LCM.exlcm import boundarypoint_t


class Lane:
    def __init__(self):
        self.pos = None
        self.theta = None
        self.left = []
        self.center = []
        self.right = [] 
        self.traj = []

    def update(self, pos, theta, left, center, right, traj):
        self.pos = pos
        self.theta = theta + pi/2.0
        self.left = left
        self.center = center
        self.right = right
        self.traj = traj

    def render(self):
        self.render_line(self.left, PASTEL_RED)
        self.render_line(self.center, SKY_BLUE)
        self.render_line(self.right, PASTEL_RED)
        self.render_line(self.traj, PASTEL_YELLOW)

    def render_line(self, line, color=SKY_BLUE, tag='line'):

        if len(line) > 0:

            glPushMatrix()
            glColor(*color)

            old_pt = (line[0].x_cm/100.0, line[0].y_cm/100.0)
            for b in range(1, len(line)):
            
                pt = (line[b].x_cm/100.0,
                      line[b].y_cm/100.0)

                glBegin(GL_LINE_STRIP)
                glVertex2f(old_pt[0], old_pt[1])
                glVertex2f(pt[0], pt[1])
                glEnd()

                old_pt = pt

            glPopMatrix()
                

