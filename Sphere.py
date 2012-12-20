import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Shape:
    ''' Defines a generic 3D shape with suitable instance variables
    and methods. All other shapes should inherit from this.'''
    def __init__(self, displayListIndex):
        ''' Constructor for the Shape object. Takes one parameter
        describing the position in and OpenGL displayList.'''
        # instance variables, these should
        # only be used by the internal methods
        self._xPos = 0
        self._yPos = 0
        self._zPos = 0
        self._displayListIndex = displayListIndex

    def draw(self):

class Sphere:
    def __init__(self, displayListIndex):
        # _<some> = private variables
        # only internal methods shall call these
        self._xPos = 0
        self._yPos = 0
        self._zPos = 0
        self._speed = 0.05
        self._displayListIndex = displayListIndex

    def update(self):
        keyState = pygame.key.get_pressed()
        # D positive, a negative, 0 if not pressed
        xDir = keyState[K_d] - keyState[K_a]
        zDir = keyState[K_w] - keyState[K_s]
        self.xPos += x_dir * self.speed
        self.zPos += z_dir * self.speed

        self.draw()

    def draw(self):
        glPushMatrix()
        glTranslate(self._xPos, self._yPos, self._zPos)
        glCallList(self._displayListIndex)
        glPopMatrix()
