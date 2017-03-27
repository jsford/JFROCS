import Tkinter as tk

from obstacle import *
from custom_colors import *
from parse_RNDF import *

class Planner:
    def __init__(self, gui, rwm):
        self.active = False
        self.gui = gui
        self.rwm = rwm

        self.car_theta = 0
        self.car_pos = (100,-100)
        
        o1 = CircleObstacle((100,100), 15, color=PASTEL_RED)
        o2 = CircleObstacle((200,100), 25, color=PASTEL_RED)
        r1 = RectangleObstacle((-50,-100), (50,30), color=PASTEL_RED)
        self.obs = [o1, o2, r1]

        self.lines = []

    
    def execute(self): 
        # Planning goes here
        self.gui.render(self.car_theta, self.car_pos, self.obs, self.lines)
        if (self.active):
            self.car_theta+=1

    def start_callback(self):
        self.active = True
        self.gui.text_out.delete(3.0,tk.END)
        self.gui.text_out.insert(3.0, 'STARTING\n', 'WHITE')

    def pause_callback(self):
        self.active = False
        self.gui.text_out.delete(3.0,tk.END)
        self.gui.text_out.insert(3.0, 'PAUSING\n', 'WHITE')

    def stop_callback(self):
        self.active = False
        self.gui.text_out.delete(3.0,tk.END)
        self.gui.text_out.insert(3.0, 'STOPPING\n', 'WHITE')
        
