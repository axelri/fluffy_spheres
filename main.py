import shapes
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def init_main():
    "Initiate pygame, initiate OpenGL, create a window, setup OpenGL"
    pygame.init()
    pygame.display.set_mode((640,480), OPENGL|DOUBLEBUF)
    pygame.display.set_caption("Fluffy spheres") 

    pygame.mouse.set_visible(0)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_COLOR_MATERIAL)

    glShadeModel(GL_SMOOTH)
    glDisable(GL_CULL_FACE)
    glColorMaterial(GL_FRONT, GL_DIFFUSE)

    glClearColor(0.1, 0.0, 0.1, 0.0)
    
            #Setup the camera
    glMatrixMode(GL_PROJECTION)

            #For the smaller window
    gluPerspective(45.0, 640/480.0, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def check_clear():
    """Clear the window, check if user has closed the window or pressed escape,
    if so, return 0"""
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    for event in pygame.event.get():
        if event.type == QUIT or \
            (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False
    return True

def main():
    # Begin main routine
    init_main()
    # Create a Clock object to maintain framerate
    clock = pygame.time.Clock()
    # Every shape object now creates itself in the OpenGL 3D plane
    sphere = shapes.Sphere()

    run = True
    while run:

        run = check_clear()
        glLoadIdentity()
        gluLookAt(0.0, 3.0, 6.0,
                  0.0, 0.0 ,0.0,
                  0.0, 1.0, 0.0)

        sphere.move()
        sphere.draw()
        pygame.display.flip()

        clock.tick(60)

if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print err
    finally:
        pygame.quit()
#main()
#pygame.quit()
