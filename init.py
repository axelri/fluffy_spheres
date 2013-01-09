import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from constants import *
from player import Player
from control import Camera
import shapes

def init_window():
    ''' Initiate pygame, initiate OpenGL, create a window, setup OpenGL'''
    
    pygame.init()
    FULLSCREEN_WIDTH = pygame.display.Info().current_w
    FULLSCREEN_HEIGHT = pygame.display.Info().current_h
    if HAVE_FULLSCREEN:
        pygame.display.set_mode((FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT), 
                OPENGL|DOUBLEBUF|FULLSCREEN)
    else:
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 
                OPENGL|DOUBLEBUF)

    pygame.display.set_caption("Fluffy spheres") 
    # NOTE: Locks all input events to the pygame window, maybe DANGEROUS
    pygame.event.set_grab(True)
    width = pygame.display.Info().current_w
    height = pygame.display.Info().current_h

    pygame.mouse.set_visible(0)
    pygame.mouse.set_pos(width/ 2.0,
                         height / 2.0)

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

    gluPerspective(45.0, float(width)/float(height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init_main():
    ''' Initiate the window, player and all other entities '''
    
    # Initialize OpenGL and pygame related objects
    init_window()
    # Create a Clock object to maintain framerate
    clock = pygame.time.Clock()

    # Create a camera object for viewing
    camera = Camera()
    # Initialize list of all the objects associated with a player
    playableShapes = []
    playableShapes.append(shapes.Sphere())

    # List of all cubes to be used
    cubelist = []
    cube = shapes.Cube()
    cube2 = shapes.Cube()
    #cube3 = shapes.Cube()
    cubelist.append(cube)
    cubelist.append(cube2)
    #cubelist.append(cube3)

    # List of all surfaces to be used
    surfList = []
    surface = shapes.Surface()
    surfList.append(surface)
    
    # List of all the players currently playing
    players = []
    player = Player("The Player", playableShapes[0], DEFAULT_MOVE_LEFT_KEY, 
            DEFAULT_MOVE_RIGHT_KEY, DEFAULT_MOVE_FORWARD_KEY,
            DEFAULT_MOVE_BACKWARD_KEY, DEFAULT_JUMP_KEY)
    players.append(player)

    # Set initial positions for all entities
    player.get_shape().set_xPos(-2)
    cube.set_xPos(2)
    cube2.set_zPos(-2)
    #cube3.set_zPos(2)
    
    return playableShapes, players, cubelist, surfList, clock, camera
