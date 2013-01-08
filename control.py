import pygame
from pygame.locals import *

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
