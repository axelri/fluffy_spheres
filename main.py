import traceback
import sys
from init import *
from control import *

def main():
    ''' Main routine of the game.'''

    # Initiate OpenGL, the window, the player and all other entities
    playableShapes, players, cubeList, surfaceList, clock, camera = init_main()

    player = players[0]
    
    run = True
    while run:

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        xPos = player.get_shape().get_xPos()
        yPos = player.get_shape().get_yPos()
        zPos = player.get_shape().get_zPos()
        
        forwardVector = camera.update(xPos, yPos, zPos)
        glLightfv(GL_LIGHT0, GL_POSITION, LIGHT0_POSITION)

        # gluLookAt(0.0, 3.0, 10.0,
        #          0.0, 1.5, 0.0,
        #          0.0, 1.0, 0.0)

        run, directions = check_user_action(players, cubeList, forwardVector, surfaceList)
        # update the object, translate
        # and then draw it
        for shape in playableShapes:
            shape.update(directions, surfaceList)
        for cube in cubeList:      
            cube.update([0.0, 0.0, 0.0], surfaceList)
        for surface in surfaceList:
            surface.update()
        pygame.display.flip()

        clock.tick(WINDOW_FPS) # Sync with 60 FPS

if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
