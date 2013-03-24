from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numbers
import shapes

CUBE_QUAD_VERTS = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
                   (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6))

CUBE_EDGES = ((0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
              (6,3), (6,4), (6,7), (5,1), (5,4), (5,7))


def cube_points(size):
    assert isinstance(size, numbers.Number), 'Input must be a number'
    assert size > 0, 'Input must be a positive number'
    h = size/2
    return [[h, -h, -h],  [h, h, -h],
            [-h, h, -h],  [-h, -h, -h],
            [h, -h, h],   [h, h, h],
            [-h, -h, h],  [-h, h, h]]


def cube(cube):
    assert isinstance(cube, shapes.Cube), 'Input must be a cube object'
    points = cube_points(cube.get_side())

    glColor3fv(cube.get_color())
    glBegin(GL_QUADS)
    for face in CUBE_QUAD_VERTS:
        for vert in face:     
            pos = points[vert]
            glVertex3fv(pos)
    glEnd()

    # TODO: Use something like "cube.get_line_color()" instead?
    glColor3f(0.0, 0.0, 0.0)    
    glBegin(GL_LINES)
    for line in CUBE_EDGES:
        for vert in line:
            pos = points[vert]
            glVertex3fv(pos)
    glEnd()

def plane(plane):
    assert isinstance(plane, shapes.Surface), 'Input must be a Surface object'
    glColor3fv(plane.get_color())
    glBegin(GL_QUADS)
    for point in plane.get_points():
        glVertex3fv(point.value)
    glEnd()

def sphere(sphere):
    assert isinstance(sphere, shapes.Sphere), 'Input must be a sphere object'
    glColor3fv(sphere.get_color())
    glutSolidSphere(sphere.get_radius(), 20, 20)
