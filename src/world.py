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
        
        
    def render(self, canvas):
        self.car.render(canvas)
        self.lane.render(canvas)

    
    def step(self):
        timeout = 0.01
        rfds, wfds, efds = select.select([self.lcm.fileno()], [], [], timeout)
        if rfds:
            self.lcm.handle()

    def handle_kinematics_msg(self, channel, data):
        msg = kinematics_t.decode(data)

    def handle_positionpose_msg(self, channel, data):
        msg = positionpose_t.decode(data)
        self.car.pos = (msg.east_m, msg.north_m)
        self.car.theta = msg.yaw_rad - math.pi/2.0

    def handle_scenario_msg(self, channel, data):
        msg = scenario_t.decode(data)

        self.lane.update(self.car.pos,
                         self.car.theta,
                         msg.left_boundary_point,
                         msg.center_point,
                         msg.right_boundary_point,
                         msg.default_trajectory_point)
       
        
