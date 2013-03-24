#Test av GJK

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from shapesGJK import *
from GJK import *
import support
from draw import *
from render import *
from physics import *


pygame.init()
pygame.display.set_mode((640, 480), OPENGL|DOUBLEBUF)

glEnable(GL_DEPTH_TEST)

glClearColor(0.1, 0.0, 0.1, 0.0)

glMatrixMode(GL_PROJECTION)

gluPerspective(45.0, 640.0/480.0, 0.1, 100.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

class Game():
    ''' A class containing all the objects in the game '''
    def __init__(self, player, objectList, sceneList):
        self._player = player
        self._objectList = objectList
        self._sceneList = sceneList

    def get_objects(self):
        return self._player, self._objectList, self._sceneList

PLANE_POINTS = [[-10.0, 0.0, -10.0], [10.0, 0.0, -10.0],
                [10.0, 0.0, 10.0], [-10.0, 0.0, 10.0]]


speed = 0.1
xPos = 2.0
yPos = 5.0
zPos = 0.0
pos = [xPos, yPos, zPos]

otherPos = [-2.0, 0.0, 0.0]

points = CUBE_POINTS
icoPoints = ICO_POINTS
planePoints = PLANE_POINTS

pos = Vector(pos)
otherPos = Vector(otherPos)

cubeOutVec = [0]*len(points)
for i in range(len(points)):
    out = points[i]
    cubeOutVec[i] = Vector(out)

planeOutVec = [0]*len(planePoints)
for i in range(len(planePoints)):
    out = planePoints[i]
    planeOutVec[i] = Vector(out)

icoOutVec = [0]*len(icoPoints)
for i in range(len(icoPoints)):
    out = icoPoints[i]
    icoOutVec[i] = Vector(out)

#mainCube = Shape(cubeOutVec, pos, support.polyhedron)
sphere = Shape(Vector(), pos, support.sphere, [0.2, 1.0, 0.8])
#icosahedron = Shape(icoOutVec, pos, support.polyhedron)
#plane = Shape(planeOutVec, pos, support.polyhedron)

#otherCube = Shape(cubeOutVec, otherPos, support.polyhedron, GREEN)
#plane = Shape(planeOutVec, otherPos, support.polyhedron)
plane = Shape(planeOutVec, Vector(), support.polyhedron, [0.5, 0.0, 1.0])


#mainCube.update_points(pos)
#icosahedron.update_points(pos)
#plane.update_points(pos)

#otherCube.update_points(otherPos)
#plane.update_points(otherPos)

#objectList = [otherCube]
#sceneList = []

objectList = []
sceneList = [plane]

game = Game(sphere, objectList, sceneList)

glTranslatef(0.0, 0.0, -10.0)                #move back
glRotatef(25.0, 1.0, 0.0, 0.0) 

run = True


while run:

    #glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    currentEvents = pygame.event.get() # cache current events
    for event in currentEvents:
        if event.type == QUIT or \
            (event.type == KEYDOWN and event.key == K_ESCAPE):
            run = False

    keyState = pygame.key.get_pressed()

    xDir = keyState[K_d] - keyState[K_a]
    yDir = keyState[K_SPACE] - keyState[K_LSHIFT]
    zDir = keyState[K_s] - keyState[K_w]

    direction = Vector([xDir, yDir, zDir])

    if not direction.is_zero():
        direction = direction.normalize()

    #mainCube.update_pos(movement)
    #mainCube.update_points(movement)
    #icosahedron.update_pos(movement)
    #icosahedron.update_points(movement)
    #plane.update_pos(movement)
    #plane.update_points(movement)
    #sphere.update_pos(movement)

    #collided, collisionInfo = GJK(sphere, otherCube)
    collided, collisionInfo = GJK(sphere, plane)
    collisionPoint, penetrationNormal, penetrationDepth = collisionInfo
    #collided, collisionPoint = GJK(mainCube, otherCube)
    #collided, collisionPoint = GJK(plane, otherCube)

    #collided, collisionPoint = GJK(sphere, plane)
    #collided, collisionPoint = GJK(mainCube, plane)

    

    sphere.update_pos(direction*speed)

##    if collided:
##        #currentColor = RED
##        otherCube.set_color(RED)
##    else:
##        #currentColor = GREEN
##        otherCube.set_color(GREEN)

    #pos = mainCube.get_pos().get_value()
    #pos = icosahedron.get_pos().get_value()
    #pos = plane.get_pos().get_value()
##    pos = sphere.get_pos().get_value()

    render(game, collisionInfo)


##    if collisionPoint:
##        colPos = collisionPoint.value
##        glPushMatrix()
##        glTranslatef(colPos[0], colPos[1], colPos[2])
##        drawCross([1.0, 1.0, 1.0])
##        glPopMatrix()
##        drawVector(penetrationNormal.value)

    #pygame.display.flip()
    #pygame.time.wait(10)


pygame.quit()
