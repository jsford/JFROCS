class Planner:
    def __init__(self):
        pass
    
    def execute(self, gui): 
        # Planning goes here
        gui.render()

    def start_callback(self):
        print "STARTING"

    def pause_callback(self):
        print "PAUSING"

    def stop_callback(self):
        print "STOPPING"
        
