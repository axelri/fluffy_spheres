#Test av GJK

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from shapesGJK import *
from GJK import *
import support


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


X = 0.525731112119133606 

Z = 0.850650808352039932


ICO_POINTS = [
    [-X, 0.0, Z], [X, 0.0, Z], [-X, 0.0, -Z], [X, 0.0, -Z],
    [0.0, Z, X], [0.0, Z, -X], [0.0, -Z, X], [0.0, -Z, -X],
    [Z, X, 0.0], [-Z, X, 0.0], [Z, -X, 0.0], [-Z, -X, 0.0]]

ICO_VERTS = [
    [0,4,1], [0,9,4], [9,5,4], [4,5,8], [4,8,1],
    [8,10,1], [8,3,10], [5,3,8], [5,2,3], [2,7,3],
    [7,10,3], [7,6,10], [7,11,6], [11,0,6], [0,1,6],
    [6,1,10], [9,0,11], [9,11,2], [9,2,5], [7,2,11]]

def drawIco():
    'draw a icosahedron in lovely colors'
    glBegin(GL_TRIANGLES)
    for i in range(20):

       glColor3f((0.31*i)%1, (0.45*i)%1, (0.11*i)%1)

       glVertex3fv(ICO_POINTS[ICO_VERTS[i][0]])

       glVertex3fv(ICO_POINTS[ICO_VERTS[i][1]])

       glVertex3fv(ICO_POINTS[ICO_VERTS[i][2]])

    glEnd()




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

def drawCross():

    glColor3fv([1.0, 1.0, 1.0])
    glBegin(GL_LINES)
    glVertex3fv([-3.0, 0.0, 0.0])
    glVertex3fv([3.0, 0.0, 0.0])
    glVertex3fv([0.0, -3.0, 0.0])
    glVertex3fv([0.0, 3.0, 0.0])
    glVertex3fv([0.0, 0.0, -3.0])
    glVertex3fv([0.0, 0.0, 3.0])
    glEnd()

def drawPlane():
    glColor3fv([0.4, 0.4, 0.6])
    glBegin(GL_TRIANGLES)
    for point in plane.get_points():
        glVertex3fv(point.get_value())
    glEnd()

PLANE_POINTS = [[-1.0, 1.0, 0.0], [1.0, -1.0, 1.0], [1.0, -1.0, -1.0]]

speed = 0.1
xPos = 2.0
yPos = 0.0
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
icosahedron = Shape(icoOutVec, pos, support.sphere)
icosahedron = Shape(icoOutVec, pos, support.polyhedron)
otherCube = Shape(cubeOutVec, otherPos, support.polyhedron)
#plane = Shape(planeOutVec, pos, support.polyhedron)


#mainCube.update_points(pos)
icosahedron.update_points(pos)
otherCube.update_points(otherPos)
#plane.update_points(pos)

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

    movement = Vector([xDir, yDir, zDir]) * speed

    #mainCube.update_pos(movement)
    #mainCube.update_points(movement)
    icosahedron.update_pos(movement)
    icosahedron.update_points(movement)
    #plane.update_pos(movement)
    #plane.update_points(movement)

    #collided, collisionPoint = GJK(mainCube, otherCube)
    collided, collisionPoint = GJK(icosahedron, otherCube)
    #collided, collisionPoint = GJK(plane, otherCube)

    if collided:
        currentColor = RED
    else:
        currentColor = GREEN

    #pos = mainCube.get_pos().get_value()
    pos = icosahedron.get_pos().get_value()
    #pos = plane.get_pos().get_value()
    if collisionPoint:
        colPos = collisionPoint.get_value()

    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    #drawMainCube()
    drawIco()
    #drawPlane()
    glPopMatrix()


    glPushMatrix()
    glTranslatef(-2.0, 0.0, 0.0)
    drawOtherCube()
    glPopMatrix()

    if collisionPoint:
        glPushMatrix()
        glTranslatef(colPos[0], colPos[1], colPos[2])
        drawCross()
        glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(10)


pygame.quit()
