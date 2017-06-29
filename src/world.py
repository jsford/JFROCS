import lcm
from LCM.exlcm import *
import select

import math

import vehicle
import obstacle

class World():
    def __init__(self):
        
        self.car = vehicle.Vehicle('ego', 'src/car_small.png', pos=(0,0))
        self.obstacles = []

        self.lcm = lcm.LCM()
        self.positionpose_sub = self.lcm.subscribe("POSITIONPOSE", self.handle_positionpose_msg)
        self.kinematics_sub = self.lcm.subscribe("KINEMATICS", self.handle_kinematics_msg)
        
        
    def render(self, canvas):
        self.car.render(canvas)
    
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
        
