# Test of the physics engine

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from shapesGJK import *
import support
from draw import *
from render import *
from physics import *


pygame.init()
pygame.display.set_mode((640, 480), OPENGL|DOUBLEBUF)

glEnable(GL_DEPTH_TEST)

glClearColor(0.0, 0.0, 0.0, 0.0)

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
xPos = 0.0
yPos = 5.0
zPos = 0.0
pos = [xPos, yPos, zPos]

otherPos = [-2.0, 0.0, 0.0]

points = CUBE_POINTS
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

sphere = Shape([Vector()], pos, support.sphere, [0.2, 1.0, 0.8])
#cube = Shape(cubeOutVec, otherPos, support.polyhedron, GREEN)
#cube.update_points(cube.get_pos())

plane = Shape(planeOutVec, Vector(), support.polyhedron, [0.5, 0.0, 1.0], mass = 10000)


#objectList = [cube]
#sceneList = []

objectList = []
sceneList = [plane]


game = Game(sphere, objectList, sceneList)

run = True
lastDirection = Vector()


while run:

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

    velChange = (sphere.get_velocity() - lastDirection*speed)\
                .projected(Vector([1.0, 0.0, 0.0]), Vector([0.0, 0.0, 1.0]))

    if direction != lastDirection:
        sphere.add_velocity((direction - lastDirection )* speed - velChange)
        lastDirection = direction


    update_physics(game)
    render(game)

pygame.quit()
