#!/usr/bin/python

from Tkinter import *
import tkMessageBox as messagebox
from PIL import Image, ImageTk
from math import *
import time
import random

from  planner import *

# Colors
LIGHT_BLUE    = "#0092CB"
SKY_BLUE      = "#2375DB"
CHARCOAL      = "#1E1E1E"
DARK_GREY     = "#282828"
LIGHT_GREY    = "#3C3C3C"

PASTEL_RED    = "#E80531"
PASTEL_BLUE   = "#3843FF"
PASTEL_GREEN  = "#46D150"
BABY_BLUE     = "#90CDFF"
PASTEL_YELLOW = "#F9FF11"


class JFROCS_gui:
    def __init__(self, width, height):
        # Init the planner
        self.planner = Planner()

        # Load car model
        self.car = Image.open("car_smallest.png")

        # Init the TK Window
        self.top = Tk()
        self.top.title("Jordan Ford Racing")
        self.width = width
        self.height = height

        win_size_str = str(width) + "x" + str(height)
        self.top.geometry(win_size_str)
        
        self.top.configure(background=CHARCOAL)

        # Add Start Button
        self.start_button = Button(self.top, text = "Start", command = self.planner.start_callback,
                                   background=PASTEL_GREEN, borderwidth=0, highlightthickness=0)
        self.start_button.place(x=20,y=150)
        self.start_button.config( height=1, width=4);

        # Add Pause Button
        self.pause_button = Button(self.top, text = "Pause", command = self.planner.pause_callback,
                                   background=SKY_BLUE, borderwidth=0, highlightthickness=0)
        self.pause_button.place(x=20,y=200)
        self.pause_button.config( height=1, width=4);

        # Add Stop Button
        self.stop_button = Button(self.top, text = "Stop", command = self.planner.stop_callback,
                                  background=PASTEL_RED, borderwidth=0, highlightthickness=0)
        self.stop_button.place(x=20,y=250)
        self.stop_button.config( height=1, width=4);

        # Add Canvas
        self.canvas = Canvas(self.top, width=814, height=440,
                             background=LIGHT_GREY, borderwidth=0, highlightthickness=0)
        self.canvas.place(x=100, y=50)

        # Add Freq. Display
        self.freq_disp = Text(self.top, height=1, width=7, borderwidth=0, highlightthickness=0,
                              background=LIGHT_GREY)
        self.freq_disp.place(x=860, y=55)

        # Add text display box
        self.text_out = Text(self.top, height=10, width=116, borderwidth=0, highlightthickness=0,
                             background=LIGHT_GREY)
        self.text_out.insert('3.0', 'Jordan Ford Racing Operator Control Station\n', 'WHITE')
        self.text_out.tag_config("WHITE", foreground='white')
        self.text_out.place(x=100, y=500)
        
        # Add Jeep Logo (Just for fun!)
        jeep_logo = Image.open("jeep_logo.png")
        jeep_logo  = jeep_logo.resize((100,100), Image.ANTIALIAS)
        jeep_logo = ImageTk.PhotoImage(jeep_logo)
        self.logo = Label(self.top, image=jeep_logo, borderwidth=0)
        self.logo.image = jeep_logo
        self.logo.place(x=0, y=self.height-100)

    # Run the tk mainloop.
    def mainloop(self):
        self.top.after(0, self.execute)
        self.top.mainloop();

    # Calls the planner and reschedules itself
    def execute(self):
        tic = time.clock()
        self.planner.execute(self)
        toc = time.clock()
        period = max(0, 20-int(floor(toc-tic)))
        self.top.after(period, self.execute)
        self.freq_disp.delete('1.0', END)
        self.freq_disp.insert('1.0', str(1000/period)+" Hz\n", "WHITE")
        self.freq_disp.tag_config("WHITE", foreground='white')

    # Is called by the planner to draw the world 
    def render(self):
        self.canvas.create_line(0,0,200,200,fill='red')
        
        


if __name__ == "__main__":
    jfrocs_gui = JFROCS_gui(960, 700)
    jfrocs_gui.mainloop() 

