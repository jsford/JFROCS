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


# Unit conversions

# Feet to meters
def ft2m(dim):
    return dim*0.3048

# Meters to Feet
def m2ft(dim):
    return dim*3.2808399

# Meters to Pixels
# The scale factor is 50/1.75 because a 1.75m wide car should be 50 pix wide.
def m2pix(m):
    return m*50.0/1.75

# Pixels to Meters
# The scale factor is 1.75/50 because a 1.75m wide car should be 50 pix wide.
def pix2m(p):
    return p*1.75/50.0


# Viewport Transformations

# Scale by the zoom level and translate by the origin
def world2screen_x(canvas, x):
    return (x)*canvas.zl + canvas.origin[0]

# Invert the y-axis, scale by the zoom level, and translate by the origin
def world2screen_y(canvas, y):
    return (-y)*canvas.zl + canvas.origin[1]

# Undo translation, then undo scaling.
def screen2world_x(canvas, x):
    return (x - canvas.origin[0])/canvas.zl
    
# Undo translation, then undo scaling, then undo the inversion of the y-axis
def screen2world_y(canvas, y):
    return -(y - canvas.origin[1])/canvas.zl
