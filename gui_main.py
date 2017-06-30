#! /usr/bin/python

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from src import draw
from src import world

display = (1280, 854)

zoom = 50
min_z = 1
max_z = 500.0

def initGL():
    # fovy, aspect, znear, zfar
    gluPerspective(45, display[0]/float(display[1]), min_z, max_z+1)
    glClearColor(*draw.LIGHT_GREY)

def main():
    global zoom

    pygame.init()
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Motion Planning")
    initGL()

    planner_world = world.World()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    zoom *= 1.1 
                    if zoom > max_z:
                        zoom = max_z
                if event.button == 5:
                    zoom /= 1.1
                    if zoom < min_z:
                        zoom = min_z
                    
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glTranslatef(0.0, 0.0, -zoom)

        planner_world.process()
        planner_world.render(-zoom) 

        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
    main()
