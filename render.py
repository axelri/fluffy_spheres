from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from shapesGJK import *
from draw import *
import pygame
from pygame.locals import *

#def render(game, collisionInfo):
def render(game):
    ''' Draws the player and all other entities at their current position '''

    player, objectList, sceneList = game.get_objects()

    #collisionPoint, penetrationNormal, penetrationDepth = collisionInfo

    assert isinstance(player, Shape), \
           'Player must be a Shape object'
    assert isinstance(objectList, list), \
           'objectList must be a list of Shape objects'
    assert isinstance(sceneList, list), \
           'sceneList must be a list of Shape objects'
    for item in objectList:
        assert isinstance(item, Shape), \
               'objectList must be a list of Shape objects'
    for item in sceneList:
        assert isinstance(item, Shape), \
               'sceneList must be a list of Shape objects'

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    pos = player.get_pos().value

    glLoadIdentity()
    #gluLookAt(pos[0], pos[1] + 4, pos[2] + 10,     # A point of reference is
    #          pos[0], pos[1], pos[2],              # needed, otherwise this 
    #          0, 1, 0)                             # is pointless.

    gluLookAt(0, 10, 20,
              0, 0, 0,
              0, 1, 0)


    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    #glColor3fv([0.2, 1.0, 0.8])
    glColor3fv(player.get_color())
    glutSolidSphere(1, 40, 40)
    glPopMatrix()

    for item in objectList:
        pos = item.get_pos().value
        glPushMatrix()
        glColor3fv(item.get_color())
        glTranslatef(pos[0], pos[1], pos[2])
        drawOtherCube()
        glPopMatrix()

    
    for item in sceneList:
        drawPlane(item)

##    if collisionPoint:
##        colPos = collisionPoint.value
##        glPushMatrix()
##        glTranslatef(colPos[0], colPos[1], colPos[2])
##        drawCross([1.0, 1.0, 1.0])
##        glPopMatrix()
##        drawVector(penetrationNormal.value)
    
    pygame.display.flip()
    pygame.time.wait(10)
