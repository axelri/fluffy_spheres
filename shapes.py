import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

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
        self._displayListIndex = displayListIndex

    def draw(self):
        ''' Draws a generic shape in the 3D space.'''
        glPushMatrix()
        glTranslate(self._xPos, self._yPos, self._zPos)
        glCallList(self._displayListIndex)
        glPopMatrix()

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
        displayListIndex = self.create_and_get_GL_object()
        super(Sphere, self).__init__(displayListIndex)

        # initiliaze/set values unique to Sphere
        self._speed = 0.05

    def create_and_get_GL_object(self):
        '''Compiles the drawing of a sphere for faster rendering,
        then returns the index of the OpenGL displayList'''
        # TODO: Make generic and move to Shape
        glColor3f(0.5, 1, 0)
        displayListIndex = glGenLists(1)
        glNewList(displayListIndex, GL_COMPILE)
        glutSolidSphere(1, 20, 20)
        glEndList()
        return displayListIndex

    def move(self):
        ''' Move around in 3D space using the keyboard.'''
        # TODO: Make generic and move to Shape
        keyState = pygame.key.get_pressed()
        # D positive, a negative, 0 if not pressed
        xDir = keyState[K_d] - keyState[K_a]
        zDir = keyState[K_w] - keyState[K_s]
        self._xPos += xDir * self._speed
        self._zPos += zDir * self._speed
