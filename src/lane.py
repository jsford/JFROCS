from Tkinter import *
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

    def render(self, canvas):
        self.render_line(canvas, self.left, PASTEL_RED, tag='left_boundary')
        self.render_line(canvas, self.center, SKY_BLUE, tag='center_line')
        self.render_line(canvas, self.right, PASTEL_RED, tag='right_boundary')
        self.render_line(canvas, self.traj, PASTEL_YELLOW, tag='default_trajectory', dash=True)

    def render_line(self, canvas, line, color=SKY_BLUE, tag='line', dash=False):

        if len(line) > 0:
            canvas.delete(tag)

            # For typing convenience
            w2sx = lambda x: world2screen_x(canvas, x)
            w2sy = lambda y: world2screen_y(canvas, y)

            rot = lambda pt, theta: (pt[0]*cos(theta)-pt[1]*sin(theta),
                                 pt[0]*sin(theta)+pt[1]*cos(theta))

            trans = lambda pt, trans: (pt[0] + trans[0], pt[1] + trans[1])

            for b in range(1, len(line)):
            
                p2 = (line[b].x_cm/10.0,
                      line[b].y_cm/10.0)
                p2 = trans(rot(p2, self.theta), self.pos)
                if (b == 1):
                    p1 = (line[0].x_cm/10.0,
                          line[0].y_cm/10.0)
                    p1 = trans(rot(p1, self.theta), self.pos)

                if dash:
                    canvas.create_line(w2sx(p1[0]), w2sy(p1[1]), 
                                       w2sx(p2[0]), w2sy(p2[1]), 
                                       fill=color, width=3, tag=tag, dash=(2,4))
                else:
                    canvas.create_line(w2sx(p1[0]), w2sy(p1[1]), 
                                       w2sx(p2[0]), w2sy(p2[1]), 
                                       fill=color, width=3, tag=tag)
                p1 = p2
                

