#Test av GJK

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from shapesGJK import *
from GJK import *


pygame.init()
pygame.display.set_mode((640, 480), OPENGL|DOUBLEBUF)

glEnable(GL_DEPTH_TEST)

glClearColor(0.1, 0.0, 0.1, 0.0)

glMatrixMode(GL_PROJECTION)

gluPerspective(45.0, 640.0/480.0, 0.1, 100.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()


CUBE_POINTS = [
    [0.5, -0.5, -0.5],  [0.5, 0.5, -0.5],
    [-0.5, 0.5, -0.5],  [-0.5, -0.5, -0.5],
    [0.5, -0.5, 0.5],   [0.5, 0.5, 0.5],
    [-0.5, -0.5, 0.5],  [-0.5, 0.5, 0.5]
]

#colors are 0-1 floating values
CUBE_COLORS = (
    (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0),
    (1, 0, 1), (1, 1, 1), (0, 0, 1), (0, 1, 1)
)

CUBE_QUAD_VERTS = (
    (0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
    (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6)
)

CUBE_EDGES = (
    (0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
    (6,3), (6,4), (6,7), (5,1), (5,4), (5,7),
)

GREEN = (0, 1, 0)
RED = (1, 0, 0)

currentColor = GREEN

def drawMainCube():
    "draw the cube"
    allpoints = zip(CUBE_POINTS, CUBE_COLORS)

    glBegin(GL_QUADS)
    for face in CUBE_QUAD_VERTS:
        for vert in face:
            pos, color = allpoints[vert]
            glColor3fv(color)
            glVertex3fv(pos)
    glEnd()

    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINES)
    for line in CUBE_EDGES:
        for vert in line:
            pos, color = allpoints[vert]
            glVertex3fv(pos)

    glEnd()

def drawOtherCube():
    "draw the cube"
    glColor3fv(currentColor)

    allpoints = zip(CUBE_POINTS, CUBE_COLORS)

    glBegin(GL_QUADS)
    for face in CUBE_QUAD_VERTS:
        for vert in face:     
            pos, color = allpoints[vert]
            glVertex3fv(pos)
    glEnd()

    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINES)
    for line in CUBE_EDGES:
        for vert in line:
            pos, color = allpoints[vert]
            glVertex3fv(pos)
    glEnd()

def update_points(points, pos):
    ''' Updates the points to the new position.
        Takes original points (centered at origin) and
        new position as input'''
    out = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    for i in range(len(points)):
        for j in range(len(points[i])):
            out[i][j] = points[i][j] + pos[j]
    return out



speed = 0.1
xPos = 2.0
yPos = 0.0
zPos = 0.0
pos = [xPos, yPos, zPos]

otherPos = [-2.0, 0.0, 0.0]

mainPoints = update_points(CUBE_POINTS, pos)
otherPoints = update_points(CUBE_POINTS, otherPos)

pos = Vector(pos)
otherPos = Vector(otherPos)

for i in range(len(mainPoints)):
    mainPoints[i] = Vector(mainPoints[i])

for i in range(len(otherPoints)):
    otherPoints[i] = Vector(otherPoints[i])


mainCube = Shape(mainPoints, pos)
otherCube = Shape(otherPoints, otherPos)


glTranslatef(0.0, 0.0, -10.0)                #move back
glRotatef(25.0, 1.0, 0.0, 0.0) 

run = True

while run:

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    currentEvents = pygame.event.get() # cache current events
    for event in currentEvents:
        if event.type == QUIT or \
            (event.type == KEYDOWN and event.key == K_ESCAPE):
            run = False

    keyState = pygame.key.get_pressed()

    xDir = keyState[K_d] - keyState[K_a]
    yDir = keyState[K_SPACE] - keyState[K_LSHIFT]
    zDir = keyState[K_s] - keyState[K_w]

    movement = Vector([xDir, yDir, zDir]).v_mult(speed)

    mainCube.update_pos(movement)
    mainCube.update_points(movement)

    #distance = mainCube.get_pos().v_add(otherCube.get_pos().v_mult(-1.0)).norm()

    #if distance < mainCube.get_boundary() + otherCube.get_boundary():
    #    collided = GJK(mainCube, otherCube)
    #else:
    #    collided = False

    collided = GJK(mainCube, otherCube)

    if collided:
        currentColor = RED
    else:
        currentColor = GREEN

    pos = mainCube.get_pos().get_value()

    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    drawMainCube()
    glPopMatrix()


    glPushMatrix()
    glTranslatef(-2.0, 0.0, 0.0)
    drawOtherCube()
    glPopMatrix()


    pygame.display.flip()
    pygame.time.wait(10)


pygame.quit()
