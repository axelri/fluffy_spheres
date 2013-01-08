import traceback
import sys
from init import *

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

def main():
    ''' Main routine of the game.'''

    playableShapes, players, cubelist, clock = init_main()

    run = True
    while run:

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        #xPos = player.get_shape().get_XPos()
        #yPos = player.get_shape().get_YPos()
        #zPos = player.get_shape().get_ZPos()
        
        #gluLookAt(xPos, yPos + 3.0, zPos + 10.0,
        #          xPos, yPos + 1.5, zPos,
        #          0.0, 1.0, 0.0)

        gluLookAt(0.0, 3.0, 10.0,
                  0.0, 1.5, 0.0,
                  0.0, 1.0, 0.0)

        run = check_user_action(players, cubelist)
        # update the object, translate
        # and then draw it
        for shape in playableShapes:
            #shape.update(direction, cubelist)
            shape.update()
        for cube in cubelist:      
            cube.update()
            cube.update_edges()
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
