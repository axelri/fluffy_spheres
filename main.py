import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import constants
import shapes

def init_main():
    "Initiate pygame, initiate OpenGL, create a window, setup OpenGL"
    pygame.init()
    pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT), 
            OPENGL|DOUBLEBUF)
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

def check_user_action(playableObj, 
            moveLeft=constants.DEFAULT_MOVE_LEFT_BUTTON,
            moveRight=constants.DEFAULT_MOVE_RIGHT_BUTTON,
            moveForward=constants.DEFAULT_MOVE_FORWARD_BUTTON,
            moveBackward=constants.DEFAULT_MOVE_BACKWARD_BUTTON,
            jump=constants.DEFAULT_JUMP_BUTTON):
    ''' Checks if the user wants to move
    the playable object, or quit the came, then delegates to the methods
    of that object. Takes one playable object.'''
    # Check for qutting
    currentEvents = pygame.event.get() # cache current events
    for event in currentEvents:
        if event.type == QUIT or \
            (event.type == KEYDOWN and event.key == K_ESCAPE):
            return False

    # Check for movements
    keyState = pygame.key.get_pressed()
    if keyState[moveLeft] != 0 or \
            keyState[moveRight] != 0 or \
            keyState[moveForward] != 0 or \
            keyState[moveBackward] != 0:
        # Get the directions and move the object
        directions = get_user_directions(moveLeft, moveRight,
                moveForward, moveBackward, keyState)
        playableObj.move(directions)

    # Check for jumping
    if keyState[jump]:
        playableObj.jump()

    return True

def get_user_directions(moveLeft, moveRight,
            moveForward, moveBackward, keyState):
    ''' Gets input from the user. Takes 4 button parameters
    and a map of the current keyboard key state. Returns an array 
    of directions on the X and Z axis. The directions can be
    1, -1 or 0 '''
    xDir = keyState[moveRight] - keyState[moveLeft]
    zDir = keyState[moveBackward] - keyState[moveForward]

    return [xDir, zDir]

def main():
    # Begin main routine
    init_main()
    # Create a Clock object to maintain framerate
    clock = pygame.time.Clock()
    # Initialize list of all the objects in the current 3D space
    objects = []
    sphere = shapes.Sphere()
    objects.append(sphere)

    run = True
    while run:

        # TODO: Why this?
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        #xPos = sphere.get_XPos()
        #yPos = sphere.get_YPos()
        #zPos = sphere.get_ZPos()
        
        #gluLookAt(xPos, yPos + 3.0, zPos + 6.0,
        #          xPos, yPos ,zPos,
        #          0.0, 1.0, 0.0)

        gluLookAt(0.0, 3.0, 10.0,
                  0.0, 0.0, 0.0,
                  0.0, 1.0, 0.0)


        run = check_user_action(sphere)
        # update the object, translate
        # and then draw it
        for obj in objects:
            obj.update()
        pygame.display.flip()

        clock.tick(constants.WINDOW_FPS) # Sync with 60 FPS

if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print err
    finally:
        pygame.quit()
