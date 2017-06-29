#!/usr/bin/python

from Tkinter import *
from PIL import Image, ImageTk
import tkMessageBox as messagebox
from math import *
import time
import random
import sys

from src import *


class JFROCS_gui:
    def __init__(self, width, height, rndf_fname):

        # Init the vehicle(s)
        self.vehicle = vehicle.Vehicle('ego', 'resources/car_small.png', pos=(0,0))

        # Init the TK Window
        self.top = Tk()
        self.top.title("Motion Planner Visualization")
        self.width = width
        self.height = height

        win_size_str = str(width) + "x" + str(height)
        self.top.geometry(win_size_str)
        
        self.top.configure(background=draw.CHARCOAL)

        # Create frame for buttons
        self.button_frame = Frame(self.top, width = 100, height = 200, bg=draw.CHARCOAL)
        self.button_frame.grid(row=1, column=0, pady = (150,0), sticky='nsew')

        # Add Start Button
        self.start_button = Button(self.button_frame, text = "Start", command = self.start_callback,
                                   background=draw.PASTEL_GREEN, borderwidth=0, highlightthickness=0)
        self.start_button.pack(pady=(0,5))
        self.start_button.config( height=1, width=4);

        # Add Pause Button
        self.pause_button = Button(self.button_frame, text = "Pause", command = self.pause_callback,
                                   background=draw.SKY_BLUE, borderwidth=0, highlightthickness=0)
        self.pause_button.pack(pady=5)
        self.pause_button.config( height=1, width=4);

        # Add Stop Button
        self.stop_button = Button(self.button_frame, text = "Stop", command = self.stop_callback,
                                  background=draw.PASTEL_RED, borderwidth=0, highlightthickness=0)
        self.stop_button.pack(pady=(5,0))
        self.stop_button.config( height=1, width=4);

        # Add Canvas
        self.canvas = Canvas(self.top, width=814, height=440,
                             background=draw.LIGHT_GREY, borderwidth=0, highlightthickness=0)
        self.canvas.grid(row=1, column=1, columnspan=1, rowspan=2, pady=(30, 10), padx=(10,30),
                         ipadx=30, ipady=30, sticky='nsew')
        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)
        self.canvas.bind("<Button-4>", self.zoomerM)
        self.canvas.bind("<Button-5>", self.zoomerP)
        self.canvas.origin = (814/2, 440/2)
        self.canvas.old_zl = 0.0
        self.canvas.zl = 1.0
        self.canvas.zoom_center = (self.canvas.winfo_width()/2, self.canvas.winfo_height()/2)

        # Add Freq. Display
        self.freq_disp = Text(self.top, height=1, width=7, borderwidth=0, highlightthickness=0,
                              background=draw.LIGHT_GREY)
        self.freq_disp.grid(row=1, column=1, sticky='ne', pady=(30,0), padx=(0,30))

        # Add Cursor Coord. Display
        self.mouse_coord_disp = Text(self.top, height=1, width=20, borderwidth=0, highlightthickness=0,
                              background=draw.LIGHT_GREY)
        self.mouse_coord_disp.grid(row=1, column=1, sticky='se', pady=(0,10), padx=(0,30))
        
        self.canvas.bind("<Motion>", self.mouse_move)

        # Add text display box
        self.text_out = Text(self.top, height=10, width=116, borderwidth=0, highlightthickness=0,
                             background=draw.LIGHT_GREY)
        self.text_out.insert('3.0', 'Jordan Ford Racing Operator Control Station\n', 'WHITE')
        self.text_out.tag_config("WHITE", foreground='white')
        self.text_out.grid(row=3, column=1, columnspan=1, rowspan=2, padx=(10,30), pady=(0,30), sticky='ew')

        # Create frame for graphs
        #self.graph_frame = Frame(self.top, width=200, height=600, bg=CHARCOAL)
        #self.graph_frame.grid(row=1, column=2, rowspan=4, pady=30, padx=(0,30), sticky='nsew')

        # Add Jeep Logo (Just for fun!)
        jeep_logo = Image.open("resources/jeep_logo.png")
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
        self.vehicle.step()
        toc = time.clock()

        self.freq_disp.delete('1.0', END)
        self.freq_disp.insert('1.0', format(1.0/(max(toc-tic, 0.01)), '.0f')+" Hz\n", "STYLE")
        self.freq_disp.tag_config("STYLE", foreground='white', justify='right')

        self.render()

        self.top.after(20, self.execute)

    # Is called by the planner to draw the world 
    def render(self):
        # Get canvas dimensions. Quit if it's 0x0
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        if (canvas_w == 0 and canvas_h == 0): return

        # Render the vehicle
        self.vehicle.render(self.canvas)

    # Click and drag the canvas using the mouse
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)
    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    # Update the current mouse coordinates on the canvas
    def mouse_move(self, event):
        mx = draw.screen2world_x(self.canvas, self.canvas.canvasx(event.x))
        my = draw.screen2world_y(self.canvas, self.canvas.canvasy(event.y))

        self.mouse_coord_disp.delete('1.0', END)
        self.mouse_coord_disp.insert('1.0', "("+format(draw.pix2m(mx),'.2f')+", "
                                               +format(draw.pix2m(my),'.2f')+")", "STYLE")
        self.mouse_coord_disp.tag_config("STYLE", foreground='white', justify='right')
        

    # Zoom using mouse scrollwheel 
    def zoomerP(self,event):
        MAX_ZOOM = 3
        if (self.canvas.zl >= MAX_ZOOM): self.canvas.zl = MAX_ZOOM; return;

        (mx, my) = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        # Move the origin to a new point calculated from the zoom center
        self.canvas.origin = (self.canvas.origin[0] - (mx-self.canvas.origin[0])*0.1,
                              self.canvas.origin[1] - (my-self.canvas.origin[1])*0.1)

        self.canvas.old_zl = self.canvas.zl
        self.canvas.zl *= 1.1

    def zoomerM(self,event):
        MIN_ZOOM = 0.01 
        if (self.canvas.zl <= MIN_ZOOM): self.canvas.zl = MIN_ZOOM; return;

        (mx, my) = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        # Move the origin to a new point calculated from the zoom center
        self.canvas.origin = (mx - (mx-self.canvas.origin[0])/1.1,
                              my - (my-self.canvas.origin[1])/1.1)

        self.canvas.old_zl = self.canvas.zl
        self.canvas.zl /= 1.1 
    
    def start_callback(self):
        pass
    def pause_callback(self):
        pass
    def stop_callback(self):
        pass


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


