#!/usr/bin/python

from Tkinter import *
import tkMessageBox as messagebox
from PIL import Image, ImageTk
from math import *
import time
import random
import sys

from draw_funcs import *
from  planner import *


class JFROCS_gui:
    def __init__(self, width, height, rndf_fname):
        # Init the RoadWorldModel
        self.rwm = RNDF(rndf_fname)

        # Init the planner
        self.planner = Planner(self, self.rwm)

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
        self.canvas.old_zoom_level = 0.0
        self.canvas.zoom_level = 1.0
        self.canvas.zoom_center = (self.canvas.winfo_width()/2, self.canvas.winfo_height()/2)

        # Add Freq. Display
        self.freq_disp = Text(self.top, height=1, width=7, borderwidth=0, highlightthickness=0,
                              background=LIGHT_GREY)
        self.freq_disp.grid(row=1, column=1, sticky='ne', pady=(30,0), padx=(0,30))

        # Add Cursor Coord. Display
        self.mouse_coord_disp = Text(self.top, height=1, width=20, borderwidth=0, highlightthickness=0,
                              background=LIGHT_GREY)
        self.mouse_coord_disp.grid(row=1, column=1, sticky='se', pady=(0,10), padx=(0,30))
        
        self.canvas.bind("<Motion>", self.mouse_move)

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
        # Get canvas dimensions. Quit if it's 0x0
        canvas_hw = self.canvas.winfo_width()/2
        canvas_hh = self.canvas.winfo_height()/2
        if (canvas_hw == 0 and canvas_hh == 0): return

        # Render the car
        zl = self.canvas.zoom_level
        if(zl != self.canvas.old_zoom_level):
            self.car = self.car_original.resize((int(zl*m2pix(1.75)), int(zl*m2pix(1.75)*self.car_original.size[1]/self.car_original.size[0])), Image.ANTIALIAS)

        car = self.car.rotate(theta, expand=True)
        car = ImageTk.PhotoImage(car) 
        self.canvas.car = car   # Keep a reference
        self.canvas.delete("car")
        self.canvas.create_image((canvas_hw+zl*pos[0],canvas_hh+zl*pos[1]), image=car, tag="car")

        # Render the rwm
        self.rwm.render(self.canvas, zl)

        # Render the obstacles
        self.canvas.delete('obstacle')
        for o in obstacles:
            o.render(self.canvas, zl)

        # Turn this into drawing the roadworldmodel
        self.canvas.delete('line')
        for l in lines:
            self.canvas.create_line(canvas_hw+zl*l[0],canvas_hh+zl*l[1],canvas_hw+zl*l[2],canvas_hh+zl*l[3], fill='white', tag='line')

    # Click and drag the canvas using the mouse
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)
    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    # Update the current mouse coordinates on the canvas
    def mouse_move(self, event):
        mx = self.canvas.canvasx(event.x)
        my = self.canvas.canvasy(event.y)

        canvas_hw = self.canvas.winfo_width()/2
        canvas_hh = self.canvas.winfo_height()/2
        zl = self.canvas.zoom_level

        self.mouse_coord_disp.delete('1.0', END)
        self.mouse_coord_disp.insert('1.0', "("+format(pix2m(mx-canvas_hw)/zl,'.2f')+", "
                                               +format(pix2m(my-canvas_hh)/zl,'.2f')+")", "STYLE")
        self.mouse_coord_disp.tag_config("STYLE", foreground='white', justify='right')
        

    # Zoom using mouse scrollwheel 
    def zoomerP(self,event):
        self.canvas.old_zoom_level = self.canvas.zoom_level
        self.canvas.zoom_level *= 1.1
        self.canvas.zoom_level = min(self.canvas.zoom_level, 5)
    def zoomerM(self,event):
        self.canvas.old_zoom_level = self.canvas.zoom_level
        self.canvas.zoom_level /= 1.1 
        self.canvas.zoom_level = max(self.canvas.zoom_level, .01)


if __name__ == "__main__":

    if len(sys.argv) == 2:
        rndf_fname = sys.argv[1]
    elif len(sys.argv) == 1:
        rndf_fname = "scenarios/SchenleyNonStopClockwise/RNDF.txt"
    else:
        print "Usage: ./gui_main <rndf>"
        exit()
    
    jfrocs_gui = JFROCS_gui(960, 700, rndf_fname)
    jfrocs_gui.mainloop() 














