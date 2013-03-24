from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

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
    #glColor3fv(currentColor)

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

def drawCross(color):

    glColor3fv(color)
    glBegin(GL_LINES)
    glVertex3fv([-3.0, 0.0, 0.0])
    glVertex3fv([3.0, 0.0, 0.0])
    glVertex3fv([0.0, -3.0, 0.0])
    glVertex3fv([0.0, 3.0, 0.0])
    glVertex3fv([0.0, 0.0, -3.0])
    glVertex3fv([0.0, 0.0, 3.0])
    glEnd()

def drawPlane(plane):
    #glColor3fv([0.4, 0.4, 0.6])
    glColor3fv(plane.get_color())
    glBegin(GL_QUADS)
    for point in plane.get_points():
        glVertex3fv(point.value)
    glEnd()

PLANE_POINTS = [[0.0, -3.0, -3.0], [0.0, 3.0, -3.0],
                [0.0, 3.0, 3.0], [0.0, -3.0, 3.0]]

def drawVector(vector):
    glColor3fv([1.0, 1.0, 1.0])
    glBegin(GL_LINES)
    glVertex3fv([0.0, 0.0, 0.0])
    glVertex3fv(vector)
    glEnd()
