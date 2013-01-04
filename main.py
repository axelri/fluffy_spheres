#!/usr/bin/env python

import traceback
import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from constants import *
from player import Player
from gamespace import GameSpace
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

def check_user_action(players, gameSpace):
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
    for player in players:
        for key in player.get_move_keys():
            if keyState[key] != 0:
                # Get the directions and move the object
                directions = get_user_directions(player.get_move_left_key(),
                        player.get_move_right_key(), 
                        player.get_move_forward_key(),
                        player.get_move_backward_key(), keyState)
                if gameSpace.is_valid_move(player.get_shape(), directions):
                    player.get_shape().move(directions)
                    break # break out of inner loop; only move once

    for player in players:
        # Check for jumping
        if keyState[player.get_jump_key()]:
            player.get_shape().jump()

    return True

def get_user_directions(moveLeft, moveRight,
            moveForward, moveBackward, keyState):
    ''' Gets input from the user. Takes 4 KEY parameters
    and a map of the current keyboard key state. Returns an array 
    of directions on the X and Z axis. The directions can be
    1, -1 or 0 '''
    xDir = keyState[moveRight] - keyState[moveLeft]
    zDir = keyState[moveBackward] - keyState[moveForward]

    return [xDir, zDir]

def main():
    ''' Main routine of the game.'''
    # TODO: Make some kind of initializing methods
    # Initialize OpenGL and pygame related objects
    init_window()
    # Create a Clock object to maintain framerate
    clock = pygame.time.Clock()
    # Initialize list of all the objects associated with a player
    playableShapes = []
    playableShapes.append(shapes.Sphere())
    playableShapes.append(shapes.Cube())
    playableShapes[0].set_xPos(-2)
    playableShapes[1].set_xPos(2)
    playableShapes[0].set_yPos(SPHERE_RADIUS)
    playableShapes[1].set_yPos(CUBE_SIDE / 2.0)

    playableShapes.append(shapes.Cube(color=[1, 0, 0], side=10))
    playableShapes[2].set_yPos(-5)
    # List of all the players currently playing
    players = []
    player = Player("The Player", playableShapes[0], DEFAULT_MOVE_LEFT_KEY, 
            DEFAULT_MOVE_RIGHT_KEY, DEFAULT_MOVE_FORWARD_KEY,
            DEFAULT_MOVE_BACKWARD_KEY, DEFAULT_JUMP_KEY)
    players.append(player)
    player2 = Player("The other Player", playableShapes[1], K_j, K_l,
            K_i, K_k, K_o)
    players.append(player2)
    gameSpace = GameSpace(playableShapes)

    run = True
    while run:

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


        run = check_user_action(players, gameSpace)
        # update the object, translate
        # and then draw it
        for shape in playableShapes:
            shape.update()
        pygame.display.flip()

        clock.tick(WINDOW_FPS) # Sync with 60 FPS

if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print err
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
