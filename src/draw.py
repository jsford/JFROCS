# Colors
LIGHT_BLUE    = (0.0000, 0.5725, 0.7961, 1.0)
SKY_BLUE      = (0.1373, 0.4588, 0.8588, 1.0)
CHARCOAL      = (0.1176, 0.1176, 0.1176, 1.0)
DARK_GREY     = (0.1569, 0.1569, 0.1569, 1.0)
LIGHT_GREY    = (0.2353, 0.2353, 0.2353, 1.0)

PASTEL_RED    = (0.9098, 0.0196, 0.1922, 1.0)
PASTEL_BLUE   = (0.2196, 0.2627, 1.0000, 1.0)
PASTEL_GREEN  = (0.2745, 0.8196, 0.3137, 1.0)
BABY_BLUE     = (0.5647, 0.8039, 1.0000, 1.0)
PASTEL_YELLOW = (0.9765, 1.0000, 0.0667, 1.0)


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
