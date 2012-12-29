import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from vector import *
from matrix import *
from math import *

class Shape(object):
    ''' Defines a generic 3D shape with suitable instance variables
    and methods. All other shapes should inherit from this.
    Need to inherit from *object* in order to be fully usable by subclasses.'''
    def __init__(self, displayListIndex):
        ''' Constructor for the Shape object. Takes one parameter
        describing the position in and OpenGL displayList.'''
        # instance variables, these should
        # only be used by the internal methods
        self._xPos = 0
        self._yPos = 0
        self._zPos = 0
    
        
        self._speed = 0
        self.color = [0, 0, 0]
        self._displayListIndex = displayListIndex

    def draw(self):
        ''' Draws a generic shape in the 3D space.'''
        glPushMatrix()
        self.translate_and_rotate()
        glCallList(self._displayListIndex)
        glPopMatrix()

    def create_and_get_GL_object(self):
        '''Compiles the drawing of a generic object for faster rendering,
        then returns the index of the OpenGL displayList'''
        glColor3fv(self.color)
        displayListIndex = glGenLists(1)
        glNewList(displayListIndex, GL_COMPILE)
        self.draw_shape()
        glEndList()
        return displayListIndex

    # external getters and setters for
    # the instance variables.
    # This way our API (the external calls to the object) can remain
    # the same, even if we want to change the class internally

    def get_XPos(self):
        return self._xPos

    def set_XPos(self, xPos):
        self._xPos = xPos

    def get_YPos(self):
        return self._yPos

    def set_YPos(self, yPos):
        self._yPos = yPos

    def get_ZPos(self):
        return self._zPos

    def set_ZPos(self, zPos):
        self._zPos = zPos

    def get_Speed(self):
        return self._speed

    def set_Speed(self, speed):
        self._speed = speed

class Sphere(Shape):
    ''' Defines a 3D sphere. Inherits from Shape. Can move
    around in 3D space'''
    def __init__(self):
        ''' Constructor for the Sphere class. Calls the constructor for the
        Shape class. This way the new Sphere object will hold all the
        instance variables and methods defined in the Shape class.'''
        self.color = [0.5, 1, 0]
        
        displayListIndex = self.create_and_get_GL_object()
        super(Sphere, self).__init__(displayListIndex)

        # initiliaze/set values unique to Sphere
        self._speed = 0.05

        self._xAxis = Vector([1.0, 0.0, 0.0])
        self._yAxis = Vector([0.0, 1.0, 0.0])
        self._zAxis = Vector([0.0, 0.0, 1.0])

        self._velocity = Vector([0.0, 0.0, 0.0])

        # Stores the rotation matrix of the sphere, initiates it as identity
        self._rotation = 0.0
        self._rotationAxis = Vector([0.0, 0.0, 0.0])
        self._rotationMatrix = identity()

    def draw_shape(self):
        ''' The drawing routine for Sphere (you are welcome to change the
        name if you want to) '''
        glutSolidSphere(1, 20, 20)
    def move(self):
        ''' Move around in 3D space using the keyboard.'''
        # TODO: Make generic and move to Shape
        keyState = pygame.key.get_pressed()
        # D positive, a negative, 0 if not pressed
        xDir = keyState[K_d] - keyState[K_a]
        zDir = keyState[K_s] - keyState[K_w]

        # Compute the new position of the sphere
        xVel = xDir * self._speed
        zVel = zDir * self._speed
        self._xPos += xVel
        self._zPos += zVel

        # Calculate the direction the sphere moves in
        self._velocity = Vector([xVel, 0.0, zVel])
        self._rotation = self._velocity.norm()
        if self._rotation:
            self._velocity = self._velocity.normalize()

        # Calculate the direction of the movement relative to the sphere-fix coordinate system
        newVelocity = self._velocity.proj_syst(self._xAxis, self._yAxis, self._zAxis)
        newVelocity = newVelocity.v_mult(self._rotation)

        # Calculate the axis of rotation
        rot_Axis = Vector([0, 1, 0]).cross(self._velocity)

        # Project the axis of rotation on the sphere-fix coordinate system
        self._rotationAxis = rot_Axis.proj_syst(self._xAxis, self._yAxis, self._zAxis)
        #self._rotationAxis = self._yAxis.cross(newVelocity)

        # Update the coorinate axises        
        dt_xAxis = self._rotationAxis.v_mult(-1.0).cross(self._xAxis)
        dt_yAxis = self._rotationAxis.v_mult(-1.0).cross(self._yAxis)
        dt_zAxis = self._rotationAxis.v_mult(-1.0).cross(self._zAxis)
        
        self._xAxis = self._xAxis.v_add(dt_xAxis)
        self._yAxis = self._yAxis.v_add(dt_yAxis)
        self._zAxis = self._zAxis.v_add(dt_zAxis)

        self._xAxis = self._xAxis.normalize()
        self._yAxis = self._yAxis.normalize()
        self._zAxis = self._zAxis.normalize()

        # Generate a rotation matrix to describe the current rotation
        rot_matrix = generate_rotation_matrix(self._rotationAxis, self._rotation)
        self._rotationMatrix = matrix_mult(self._rotationMatrix, rot_matrix)

    def translate_and_rotate(self):
        glTranslate(self._xPos, self._yPos, self._zPos)
        glMultMatrixf(self._rotationMatrix)
