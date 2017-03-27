#!/usr/bin/python

from Tkinter import *
import tkMessageBox as messagebox
from PIL import Image, ImageTk
from math import *
import time
import random

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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
        self.planner = Planner(self)

        # Load car model
        self.car_original = Image.open("car_small.png")

        # Init the TK Window
        self.top = Tk()
        self.top.title("Jordan Ford Racing")
        self.width = width
        self.height = height

        win_size_str = str(width) + "x" + str(height)
        self.top.geometry(win_size_str)
        
        self.top.configure(background=CHARCOAL)

        # Create frame for buttons
        self.button_frame = Frame(self.top, width = 100, height = 200, bg=CHARCOAL)
        self.button_frame.grid(row=1, column=0, pady = (150,0), sticky='nsew')

        # Add Start Button
        self.start_button = Button(self.button_frame, text = "Start", command = self.planner.start_callback,
                                   background=PASTEL_GREEN, borderwidth=0, highlightthickness=0)
        self.start_button.pack(pady=(0,5))
        self.start_button.config( height=1, width=4);

        # Add Pause Button
        self.pause_button = Button(self.button_frame, text = "Pause", command = self.planner.pause_callback,
                                   background=SKY_BLUE, borderwidth=0, highlightthickness=0)
        self.pause_button.pack(pady=5)
        self.pause_button.config( height=1, width=4);

        # Add Stop Button
        self.stop_button = Button(self.button_frame, text = "Stop", command = self.planner.stop_callback,
                                  background=PASTEL_RED, borderwidth=0, highlightthickness=0)
        self.stop_button.pack(pady=(5,0))
        self.stop_button.config( height=1, width=4);

        # Add Canvas
        self.canvas = Canvas(self.top, width=814, height=440,
                             background=LIGHT_GREY, borderwidth=0, highlightthickness=0)
        self.canvas.grid(row=1, column=1, columnspan=1, rowspan=2, pady=(30, 10), padx=(10,30),
                         ipadx=30, ipady=30, sticky='nsew')
        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)
        self.canvas.bind("<Button-4>", self.zoomerM)
        self.canvas.bind("<Button-5>", self.zoomerP)
        self.canvas.zoom_level = 1.0
        self.canvas.zoom_center = (self.canvas.winfo_width()/2, self.canvas.winfo_height()/2)

        # Add Freq. Display
        self.freq_disp = Text(self.top, height=1, width=7, borderwidth=0, highlightthickness=0,
                              background=LIGHT_GREY)
        self.freq_disp.grid(row=1, column=1, sticky='ne', pady=(30,0), padx=(0,30))

        # Add text display box
        self.text_out = Text(self.top, height=10, width=116, borderwidth=0, highlightthickness=0,
                             background=LIGHT_GREY)
        self.text_out.insert('3.0', 'Jordan Ford Racing Operator Control Station\n', 'WHITE')
        self.text_out.tag_config("WHITE", foreground='white')
        self.text_out.grid(row=3, column=1, columnspan=1, rowspan=2, padx=(10,30), pady=(0,30), sticky='ew')

        # Create frame for graphs
        #self.graph_frame = Frame(self.top, width=200, height=600, bg=CHARCOAL)
        #self.graph_frame.grid(row=1, column=2, rowspan=4, pady=30, padx=(0,30), sticky='nsew')

        # Add Jeep Logo (Just for fun!)
        jeep_logo = Image.open("jeep_logo.png")
        jeep_logo  = jeep_logo.resize((100,100), Image.ANTIALIAS)
        jeep_logo = ImageTk.PhotoImage(jeep_logo)
        self.logo = Label(self.top, image=jeep_logo, borderwidth=0)
        self.logo.image = jeep_logo
        self.logo.grid(row=4,column=0,padx=(10,0))

        # Handle resizing
        self.top.grid_rowconfigure(1, weight=2)
        self.top.grid_columnconfigure(1, weight=2)

    # Run the tk mainloop.
    def mainloop(self):
        self.top.after(0, self.execute)
        self.top.mainloop();

    # Calls the planner and reschedules itself
    def execute(self):
        tic = time.clock()
        self.planner.execute()
        toc = time.clock()
        period = max(0, 20-int(floor(toc-tic)))
        self.top.after(period, self.execute)
        self.freq_disp.delete('1.0', END)
        self.freq_disp.insert('1.0', str(1000/period)+" Hz\n", "WHITE")
        self.freq_disp.tag_config("WHITE", foreground='white')

    # Is called by the planner to draw the world 
    def render(self, theta, pos, obstacles, lines):
        # Render the car
        zl = self.canvas.zoom_level
        car = self.car_original.resize((int(zl*50), int(zl*50*self.car_original.size[1]/self.car_original.size[0])), Image.ANTIALIAS)
        car = car.rotate(theta, expand=True)
        car = ImageTk.PhotoImage(car) 
        self.canvas.car = car   # Keep a reference
        canvas_hw = self.canvas.winfo_width()/2
        canvas_hh = self.canvas.winfo_height()/2
        self.canvas.delete("car")
        self.canvas.create_image((canvas_hw+zl*pos[0],canvas_hh+zl*pos[1]), image=car, tag="car")

        # Render the obstacles
        self.canvas.delete('obstacle')
        for o in obstacles:
            rad = o.rad * zl
            pos = (canvas_hw+o.pos[0]*zl, canvas_hh+o.pos[1]*zl)
            self.canvas.create_oval(pos[0]-rad, pos[1]-rad, pos[0]+rad, pos[1]+rad, outline=PASTEL_RED, tag="obstacle")

        self.canvas.delete('line')
        for l in lines:
            self.canvas.create_line(canvas_hw+zl*l[0],canvas_hh+zl*l[1],canvas_hw+zl*l[2],canvas_hh+zl*l[3], fill='white', tag='line')


    # Click and drag the canvas using the mouse
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)
    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    # Zoom using...something 
    def zoomerP(self,event):
        self.canvas.zoom_level *= 1.1
    def zoomerM(self,event):
        self.canvas.zoom_level *= 0.9 
        
        
        
        


if __name__ == "__main__":
    jfrocs_gui = JFROCS_gui(960, 700)
    jfrocs_gui.mainloop() 

