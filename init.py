import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from constants import *
from player import Player
from control import Camera
from vector import Vector
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
    glEnable (GL_BLEND)
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glShadeModel(GL_SMOOTH)
    glDisable(GL_CULL_FACE)
    glColorMaterial(GL_FRONT, GL_DIFFUSE)

    glClearColor(0.1, 0.0, 0.1, 0.0)
    
    #Setup the camera
    glMatrixMode(GL_PROJECTION)

    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
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
    #cube = shapes.Cube(color=[1.0, 0.0, 0.0, 1.0])
   # cube2 = shapes.Cube(color=[0.0, 1.0, 0.0, 1.0])
   # cube3 = shapes.Cube(color=[0.0, 0.0, 1.0, 1.0])
    #cubelist.append(cube)
    #cubelist.append(cube2)
    #cubelist.append(cube3)

    # List of all surfaces to be used
    surfaceList = []
    bottomSurface = shapes.Surface()

    # TODO: We should really try to seperate out these init methods.
    # Refactor into smaller ones, and eventually script all this
    # from some outside environment.
    wall1 = shapes.Surface(width = 1.0,
                           center = [-SURFACE_SIZE, 1.0, 0.0],
                           normal = Vector('e_x'))
    wall2 = shapes.Surface(width = 1.0,
                           center = [SURFACE_SIZE, 1.0, 0.0],
                           normal = - Vector('e_x'))
    wall3 = shapes.Surface(length = 1.0,
                           center = [0.0, 1.0, -SURFACE_SIZE],
                           normal = Vector('e_z'))
    wall4 = shapes.Surface(length = 1.0,
                           center = [0.0, 1.0, SURFACE_SIZE],
                           normal = - Vector('e_z'))

    slope = shapes.Surface(normal = Vector([0.3, 1.0, 0.0]),
                           center = [-(SURFACE_SIZE + SURFACE_SIZE * 0.9553365),
                                     2.0 + SURFACE_SIZE * 0.286601, 0.0])

    ground = shapes.Surface(length = 30, width = 30,
                               center = [0.0, -3.0, 0.0],
                               normal = Vector('e_y'),
                            color = [0.0, 1.0, 0.0, 1.0])

    cubefront = shapes.Surface(length = 1, width = 1,
                               center = [0.0, 1.0, 1.0],
                               normal = Vector('e_z'))
    cubeback = shapes.Surface(length = 1, width = 1,
                               center = [0.0, 1.0, -1.0],
                               normal = - Vector('e_z'))
    cubetop = shapes.Surface(length = 1, width = 1,
                               center = [0.0, 2.0, 0.0],
                               normal = Vector('e_y'))
    cuberight = shapes.Surface(length = 1, width = 1,
                               center = [1.0, 1.0, 0.0],
                               normal = Vector('e_x'))
    cubeleft = shapes.Surface(length = 1, width = 1,
                               center = [-1.0, 1.0, 0.0],
                               normal = - Vector('e_x'))


    cube2front = shapes.Surface(length = 1, width = 1,
                               center = [-15.0, -2.0, 1.0],
                               normal = Vector('e_z'))
    cube2back = shapes.Surface(length = 1, width = 1,
                               center = [-15.0, -2.0, -1.0],
                               normal = - Vector('e_z'))
    cube2top = shapes.Surface(length = 1, width = 1,
                               center = [-15.0, -1.0, 0.0],
                               normal = Vector('e_y'))
    cube2right = shapes.Surface(length = 1, width = 1,
                               center = [-14.0, -2.0, 0.0],
                               normal = Vector('e_x'))
    cube2left = shapes.Surface(length = 1, width = 1,
                               center = [-16.0, -2.0, 0.0],
                               normal = - Vector('e_x'))

    surfaceList.extend([bottomSurface, wall1, wall2, wall3, wall4, slope])
    surfaceList.append(ground)
    #surfaceList.extend(cube.get_surfaces())
    surfaceList.extend([cubefront, cubeback, cubetop, cuberight, cubeleft])
    surfaceList.extend([cube2front, cube2back, cube2top, cube2right, cube2left])

    for surface in surfaceList:
        print "Center", surface.get_center()
        print "Normal", surface.get_normal().get_value()
        print "Points", surface.get_points()
        vectors = surface.get_surface_vectors()
        print "Surface vectors:"
        for vector in vectors:
            print '\t', vector.get_value()
        print ""


    
    # List of all the players currently playing
    players = []
    player = Player("The Player", playableShapes[0], DEFAULT_MOVE_LEFT_KEY, 
            DEFAULT_MOVE_RIGHT_KEY, DEFAULT_MOVE_FORWARD_KEY,
            DEFAULT_MOVE_BACKWARD_KEY, DEFAULT_JUMP_KEY)
    players.append(player)

    # Set initial positions for all entities
    player.get_shape().set_xPos(-2)
    #cube.set_xPos(2)
    #cube2.set_zPos(-2)
    #cube3.set_zPos(2)
    
    return playableShapes, players, cubelist, surfaceList, clock, camera
