from Tkinter import *
from PIL import Image, ImageTk
from math import *
from draw import *

import lcm
from LCM.exlcm import *
import select


class Vehicle:
    def __init__(self, name, texture_fname, pos=(0,0), theta=0, width_m=1.75, lightweight=False):
        self.name = name
        self.pos = pos
        self.theta = theta 
        self.width_m = width_m
        self.texture = Image.open(texture_fname) 
        self.lightweight = lightweight

        self.lcm = lcm.LCM()
        self.kinematics_sub = self.lcm.subscribe("POSITIONPOSE", self.handle_positionpose_msg)


        # Static variables for render function
        self.render_old_zl = -1
        self.render_old_theta = float('nan')
    
    def handle_positionpose_msg(self, channel, data):
        msg = positionpose_t.decode(data)
        self.pos = (msg.east_m, msg.north_m)
        self.theta = msg.yaw_rad - 3.1415926535/2.0

    # Check for a kinematics_t or position_pose message and update the vehicle state
    def step(self):
        timeout = 0.01
        rfds, wfds, efds = select.select([self.lcm.fileno()], [], [], timeout)
        if rfds:
            self.lcm.handle()

    def render(self, canvas):
        zl = canvas.zl
        canvas.delete(self.name)

        if (self.lightweight):
            # Make the car twice as long as it is wide
            (hw, hh) = (m2pix(self.width_m/2.0), m2pix(self.width_m))
            hyp = sqrt(hw*hw+hh*hh)
            phi = atan(hw/hh)

            # Clockwise order
            a1 = self.theta + phi
            a2 = self.theta - phi
            a3 = a1 + pi
            a4 = a2 + pi 

            p1 = (world2screen_x(canvas, self.pos[0] + hyp*cos(a1)), 
                  world2screen_y(canvas, self.pos[1] + hyp*sin(a1)))
            p2 = (world2screen_x(canvas, self.pos[0] + hyp*cos(a2)), 
                  world2screen_y(canvas, self.pos[1] + hyp*sin(a2)))
            p3 = (world2screen_x(canvas, self.pos[0] + hyp*cos(a3)), 
                  world2screen_y(canvas, self.pos[1] + hyp*sin(a3)))
            p4 = (world2screen_x(canvas, self.pos[0] + hyp*cos(a4)), 
                  world2screen_y(canvas, self.pos[1] + hyp*sin(a4)))
            p5 = (world2screen_x(canvas, self.pos[0] + hh*cos(self.theta)), 
                  world2screen_y(canvas, self.pos[1] + hh*sin(self.theta)))

            canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill='orange', width=3, tag=self.name)
            canvas.create_line(p2[0], p2[1], p3[0], p3[1], fill='orange', width=3, tag=self.name)
            canvas.create_line(p3[0], p3[1], p4[0], p4[1], fill='orange', width=3, tag=self.name)
            canvas.create_line(p4[0], p4[1], p1[0], p1[1], fill='orange', width=3, tag=self.name)
            canvas.create_line(p4[0], p4[1], p5[0], p5[1], fill='orange', width=3, tag=self.name)
            canvas.create_line(p3[0], p3[1], p5[0], p5[1], fill='orange', width=3, tag=self.name)
            return

        if (zl != self.render_old_zl):
            self.render_car_pil = self.texture.resize((int(zl*m2pix(self.width_m)),
                 int(zl*m2pix(self.width_m))*self.texture.size[1]/self.texture.size[0]),
                 Image.ANTIALIAS)

        if (self.theta != self.render_old_theta or zl != self.render_old_zl):
            # Don't resize an image and assign it to the same name. It freaks out.
            self.render_car_pil_rot = self.render_car_pil.rotate(180*self.theta/pi, expand=True, resample=Image.BICUBIC)

        self.render_car = ImageTk.PhotoImage(self.render_car_pil_rot)
        canvas.delete(self.name)
        canvas.create_image((world2screen_x(canvas, self.pos[0]),
                                 world2screen_y(canvas, self.pos[1])), image=self.render_car, tag=self.name)
        self.render_old_zl = zl
        self.render_old_theta = self.theta
