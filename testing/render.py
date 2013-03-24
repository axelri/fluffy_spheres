import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import shapes

#def render(game, collisionInfo):
def render(game):
    ''' Draws the player and all other entities at their current position '''

    player, objectList, sceneList = game.get_objects()

    #collisionPoint, penetrationNormal, penetrationDepth = collisionInfo

    assert isinstance(player, shapes.Shape), \
           'Player must be a Shape object'
    assert isinstance(objectList, list), \
           'objectList must be a list of Shape objects'
    assert isinstance(sceneList, list), \
           'sceneList must be a list of Shape objects'
    for item in objectList:
        assert isinstance(item, shapes.Shape), \
               'objectList must be a list of Shape objects'
    for item in sceneList:
        assert isinstance(item, shapes.Shape), \
               'sceneList must be a list of Shape objects'

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    glLoadIdentity()
    #gluLookAt(pos[0], pos[1] + 4, pos[2] + 10,     # A point of reference is
    #          pos[0], pos[1], pos[2],              # needed, otherwise this 
    #          0, 1, 0)                             # is pointless.

    gluLookAt(0, 10, 20,
              0, 0, 0,
              0, 1, 0)

    #gluLookAt(0, 2, 4,
    #          0, 0, 0,
    #          0, 1, 0)

    pos = player.get_pos().value
    
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    player.draw()
    glPopMatrix()

    for item in objectList:
        pos = item.get_pos().value
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        item.draw()
        glPopMatrix()

    
    for item in sceneList:
        pos = item.get_pos().value
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        item.draw()
        glPopMatrix()

##    if collisionPoint:
##        colPos = collisionPoint.value
##        glPushMatrix()
##        glTranslatef(colPos[0], colPos[1], colPos[2])
##        drawCross([1.0, 1.0, 1.0])
##        glPopMatrix()
##        drawVector(penetrationNormal.value)
    
    pygame.display.flip()
    pygame.time.wait(10)
