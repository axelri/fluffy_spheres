# Test of the physics engine

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import shapes
import render
import physics
import games
import vectors


pygame.init()
pygame.display.set_mode((640, 480), OPENGL|DOUBLEBUF)

glEnable(GL_DEPTH_TEST)
#glEnable(GL_LIGHTING)
#glEnable(GL_LIGHT0)

glClearColor(0.0, 0.0, 0.0, 0.0)

glMatrixMode(GL_PROJECTION)

gluPerspective(45.0, 640.0/480.0, 0.1, 100.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

PLANE_POINTS = [[-10.0, 0.0, -10.0], [10.0, 0.0, -10.0],
                [10.0, 0.0, 10.0], [-10.0, 0.0, 10.0]]


speed = 0.1
xPos = 0.0
yPos = 5.0
zPos = 0.0
pos = [xPos, yPos, zPos]

otherPos = [-2.0, 5.0, 0.0]

planePoints = PLANE_POINTS

pos = vectors.Vector(pos)
otherPos = vectors.Vector(otherPos)

planeOutVec = [0]*len(planePoints)
for i in range(len(planePoints)):
    out = planePoints[i]
    planeOutVec[i] = vectors.Vector(out)

sphere = shapes.Sphere(pos = pos)

#cube = shapes.Cube(pos = otherPos)

plane = shapes.Surface(points = planeOutVec)


#objectList = [cube]
#sceneList = []

objectList = []
sceneList = [plane]


game = games.Game(sphere, objectList, sceneList)

run = True
lastDirection = vectors.Vector()


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

    direction = vectors.Vector([xDir, yDir, zDir])

    if not direction.is_zero():
        direction = direction.normalize()

    velChange = (sphere.get_velocity() - lastDirection*speed)\
                .projected(vectors.Vector([1.0, 0.0, 0.0]), vectors.Vector([0.0, 0.0, 1.0]))

    if direction != lastDirection:
        sphere.add_velocity((direction - lastDirection )* speed - velChange)
        lastDirection = direction


    physics.update_physics(game)
    render.render(game)

pygame.quit()
