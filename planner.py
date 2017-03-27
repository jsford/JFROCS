class Obstacle:
    def __init__(self, rad, pos):
        self.rad = rad
        self.pos = pos


class Planner:
    def __init__(self, gui):
        self.active = False
        self.gui = gui

        self.car_theta = 0
        self.car_pos = (100,-100)
        
        o1 = Obstacle(15, (100,100))
        o2 = Obstacle(25, (200,100))
        self.obs = [o1, o2]

        l1 = (0,0,100,100)
        l2 = (0,0,-400,30)
        self.lines = [l1, l2]
    
    def execute(self): 
        # Planning goes here
        self.gui.render(self.car_theta, self.car_pos, self.obs, self.lines)
        if (self.active):
            self.car_theta+=1

    def start_callback(self):
        self.active = True
        self.gui.text_out.insert('2.0', 'STARTING\n', 'WHITE')

    def pause_callback(self):
        self.active = False
        self.gui.text_out.insert('2.0', 'PAUSING\n', 'WHITE')

    def stop_callback(self):
        self.active = False
        self.gui.text_out.insert('2.0', 'STOPPING\n', 'WHITE')
        
