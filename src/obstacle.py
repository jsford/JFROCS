from draw import *

class Obstacle(object):
    def __init__(self, cp, color='red'):
        self.center_pos = cp
        self.color = color

    def render(self, canvas):
        pass 

class CircleObstacle(Obstacle):
    def __init__(self, cp, r, color='green'):
        super(CircleObstacle, self).__init__(cp, color)
        self.rad = r
        
    def render(self, canvas):
        canvas_hw = canvas.winfo_width()/2
        canvas_hh = canvas.winfo_height()/2
        p1 = (world2screen_x(canvas, self.center_pos[0]-self.rad), world2screen_y(canvas, self.center_pos[1]-self.rad))
        p2 = (world2screen_x(canvas, self.center_pos[0]+self.rad), world2screen_y(canvas, self.center_pos[1]+self.rad))
        canvas.create_oval(p1[0], p1[1], p2[0], p2[1], outline=self.color, tag='obstacle')

class RectangleObstacle(Obstacle):
    def __init__(self, cp, dim, color='blue'):
        super(RectangleObstacle, self).__init__(cp, color)
        self.dim = dim

    def render(self, canvas):
        rect_hw = self.dim[0]/2
        rect_hh = self.dim[1]/2
        p1 =  (world2screen_x(canvas, self.center_pos[0]-rect_hw),
               world2screen_y(canvas, self.center_pos[1]-rect_hh))
        p2 =  (world2screen_x(canvas, self.center_pos[0]-rect_hw),
               world2screen_y(canvas, self.center_pos[1]+rect_hh))
        p3 =  (world2screen_x(canvas, self.center_pos[0]+rect_hw),
               world2screen_y(canvas, self.center_pos[1]+rect_hh))
        p4 =  (world2screen_x(canvas, self.center_pos[0]+rect_hw),
               world2screen_y(canvas, self.center_pos[1]-rect_hh))
        canvas.create_rectangle(p1[0], p1[1], p3[0], p3[1], outline=self.color, tag='obstacle')
        canvas.create_line(p1[0], p1[1], p3[0], p3[1], fill=self.color, tag='obstacle')
        canvas.create_line(p2[0], p2[1], p4[0], p4[1], fill=self.color, tag='obstacle')
