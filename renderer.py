from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from shapesGJK import *
from draw import *

def render(player, objectList, sceneList):
    ''' Draws the player and all other entities at their current position '''

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

    pos = player.get_pos().get_value()

    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    #glColor3fv([0.2, 1.0, 0.8])
    glColor3fv(player.get_color())
    glutSolidSphere(1, 40, 40)
    glPopMatrix()

    for item in objectList:
        pos = item.get_pos().get_value()
        glPushMatrix()
        glColor3fv(item.get_color())
        glTranslatef(pos[0], pos[1], pos[2])
        drawOtherCube()
        glPopMatrix()

    
    #for item in sceneList:
        #glPushMatrix()
        #glTranslatef(-2.0, 0.0, 0.0)
        #drawOtherCube()
        #glPopMatrix()
