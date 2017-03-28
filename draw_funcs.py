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

def ft2m(dim):
    return dim*0.3048

def m2ft(dim):
    return dim*3.2808399

def m2pix(m):
    return m*50.0/1.75
def pix2m(p):
    return p*1.75/50.0

def world2screen_x(canvas, x):
    #return (x-canvas.origin[0])*canvas.zl + canvas.winfo_width()/2
    return (x)*canvas.zl + canvas.winfo_width()/2

def world2screen_y(canvas, y):
    #return (y-canvas.origin[1])*canvas.zl + canvas.winfo_height()/2
    return (y)*canvas.zl + canvas.winfo_height()/2

def screen2world_x(canvas, x):
    #return (x - canvas.winfo_width()/2)/canvas.zl + canvas.origin[0]
    return (x - canvas.winfo_width()/2)/canvas.zl
    
def screen2world_y(canvas, y):
    #return (y - canvas.winfo_height()/2)/canvas.zl + canvas.origin[1]
    return (y - canvas.winfo_height()/2)/canvas.zl
