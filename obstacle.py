class Obstacle(object):
    def __init__(self, cp, color='red'):
        self.center_pos = cp
        self.color = color

    def render(self, canvas, zoom_level):
        pass 

class CircleObstacle(Obstacle):
    def __init__(self, cp, r, color='green'):
        super(CircleObstacle, self).__init__(cp, color)
        self.rad = r
        
    def render(self, canvas, zl):
        canvas_hw = canvas.winfo_width()/2
        canvas_hh = canvas.winfo_height()/2
        pos = (canvas_hw+self.center_pos[0]*zl, canvas_hh+self.center_pos[1]*zl)
        canvas.create_oval(pos[0]-self.rad*zl, pos[1]-self.rad*zl, pos[0]+self.rad*zl, pos[1]+self.rad*zl, outline=self.color, tag='obstacle')

class RectangleObstacle(Obstacle):
    def __init__(self, cp, dim, color='blue'):
        super(RectangleObstacle, self).__init__(cp, color)
        self.dim = dim

    def render(self, canvas, zl):
        canvas_hw = canvas.winfo_width()/2
        canvas_hh = canvas.winfo_height()/2
        rect_hw = self.dim[0]/2
        rect_hh = self.dim[1]/2
        pos = (canvas_hw+self.center_pos[0]*zl, canvas_hh+self.center_pos[1]*zl)
        canvas.create_rectangle(pos[0]-rect_hw*zl, pos[1]-rect_hh*zl, pos[0]+rect_hw*zl, pos[1]+rect_hh*zl, outline=self.color, tag='obstacle')
        canvas.create_line(pos[0]-rect_hw*zl, pos[1]-rect_hh*zl, pos[0]+rect_hw*zl, pos[1]+rect_hh*zl, fill=self.color, tag='obstacle')
        canvas.create_line(pos[0]+rect_hw*zl, pos[1]-rect_hh*zl, pos[0]-rect_hw*zl, pos[1]+rect_hh*zl, fill=self.color, tag='obstacle')
