from OpenGL.GL import *
from OpenGL.GLU import *

import lcm
from LCM.exlcm import *
import select

import math

import vehicle
import lane
import obstacle
import draw


class World():
    def __init__(self):
        
        self.car = vehicle.Vehicle('ego', 'src/car_small.png', pos=(0,0))
        self.lane = lane.Lane()

        self.lcm = lcm.LCM()
        self.positionpose_sub = self.lcm.subscribe("POSITIONPOSE", self.handle_positionpose_msg)
        self.kinematics_sub = self.lcm.subscribe("KINEMATICS", self.handle_kinematics_msg)
        self.scenario_sub = self.lcm.subscribe("SCENARIO", self.handle_scenario_msg)

        self.origin = None
        
        
    def render(self):

        # Translate everything else to be centered on the car.
        center  = self.car.get_pos()
        heading = self.car.get_heading() * 180.0/math.pi - 90

        glPushMatrix()
        #glTranslatef(center[0], center[1], 0)
        glRotate(heading, 0, 0, 1.0)

        self.car.render()

        self.lane.render()

        # Undo the translation to car coordinates.
        glPopMatrix()
        
    def process(self):
        timeout = 0.01
        rfds, wfds, efds = select.select([self.lcm.fileno()], [], [], timeout)
        if rfds:
            self.lcm.handle()

    def handle_kinematics_msg(self, channel, data):
        msg = kinematics_t.decode(data)

    def handle_positionpose_msg(self, channel, data):
        msg = positionpose_t.decode(data)
        self.car.pos = (msg.east_m, msg.north_m)
        self.car.theta_rad = msg.yaw_rad

    def handle_scenario_msg(self, channel, data):
        msg = scenario_t.decode(data)
    
        if self.origin == None:
            self.origin = self.car.pos
            glTranslatef(self.origin[0], self.origin[1], 0.0)

        self.lane.update(self.car.pos,
                         self.car.theta_rad,
                         msg.left_boundary_point,
                         msg.center_point,
                         msg.right_boundary_point,
                         msg.default_trajectory_point)
       
        
