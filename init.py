import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from constants import *
from player import Player
import shapes

def init_window():
    ''' Initiate pygame, initiate OpenGL, create a window, setup OpenGL'''
    
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 
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
    gluPerspective(45.0, float(WINDOW_WIDTH)/float(WINDOW_HEIGHT), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init_main():
    ''' Initiate the window, player and all other entities '''
    
    # Initialize OpenGL and pygame related objects
    init_window()
    # Create a Clock object to maintain framerate
    clock = pygame.time.Clock()
    # Initialize list of all the objects associated with a player
    playableShapes = []
    playableShapes.append(shapes.Sphere())

    # List all cubes to be used
    cubelist = []
    cube = shapes.Cube()
    cube2 = shapes.Cube()
    cubelist.append(cube)
    cubelist.append(cube2)
    
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
    
    return playableShapes, players, cubelist, clock
