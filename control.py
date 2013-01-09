import pygame
from pygame.locals import *
from OpenGL.GLU import *
from math import *
from constants import *

def check_user_action(players, cubelist):
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
        # Check for jumping
        if keyState[player.get_jump_key()]:
            player.get_shape().jump()

        # Get the directions and move the object
        directions = get_user_directions(player.get_move_left_key(),
                        player.get_move_right_key(), 
                        player.get_move_forward_key(),
                        player.get_move_backward_key(), keyState)
        player.get_shape().move(directions, cubelist)

    return True

def get_user_directions(moveLeft, moveRight,
            moveForward, moveBackward, keyState):
    ''' Gets input from the user. Takes 4 KEY parameters
    and a map of the current keyboard key state. Returns an array 
    of directions on the X and Z axis. The directions can be
    1, -1 or 0 '''
    xDir = keyState[moveRight] - keyState[moveLeft]
    zDir = keyState[moveBackward] - keyState[moveForward]

    return [xDir, 0.0, zDir]

class Camera:
    def __init__(self):
        # The distance from the camera to the player
        self._xDist = CAMERA_X_DISTANCE
        self._yDist = CAMERA_Y_DISTANCE
        self._zDist = CAMERA_Z_DISTANCE

        # The position of the camera
        self._xPos = self._xDist
        self._yPos = self._yDist
        self._zPos = self._zDist

        self._xAngle = 0.0
        # self._yAngle = 0.0

        # The up vector for the camera
        self._up = [0.0, 1.0, 0.0]        

    def view(self, playerX, playerY, playerZ):
        ''' Calculates a translation/rotation matrix
        to move the camera to the right position and
        multiplies it with the current matrix used by
        OpenGL '''
        gluLookAt(self._xPos, self._yPos, self._zPos,
                  playerX, playerY, playerZ,
                  self._up[0], self._up[1], self._up[2])

    def move(self, playerX, playerY, playerZ):
        ''' Moves the camera to the right position based
        on the movement of the player and the mouse '''
        mouseX, mouseY = pygame.mouse.get_pos()

        diffX = (mouseX - WINDOW_WIDTH / 2.0) * pi / 180.0
        # diffY = (mouseY - WINDOW_HEIGHT / 2.0) * pi / 180.0

        # self._xAngle += diffX
        # self._yAngle += diffY

        # self._xPos = playerX + sin(self._xAngle) * self._zDist
        # self._zPos = playerZ + cos(self._xAngle) * self._zDist
        self._xPos = playerX + sin(diffX) * self._zDist
        self._zPos = playerZ + cos(diffX) * self._zDist

        # pygame.mouse.set_pos(WINDOW_WIDTH / 2,
                        # WINDOW_HEIGHT / 2)

    def update(self, playerX, playerY, playerZ):
        ''' Updates the camera '''
        self.move(playerX, playerY, playerZ)
        self.view(playerX, playerY, playerZ)
