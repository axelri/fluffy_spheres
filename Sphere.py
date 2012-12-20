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
        self.pos = [0, 0, 0]
        self.speed = 0.05
        self.displayListIndex = displayListIndex

    def update(self):
        keyState = pygame.key.get_pressed()
        # D positive, a negative, 0 if not pressed
        x_dir = keyState[K_d] - keyState[K_a]
        z_dir = keyState[K_w] - keyState[K_s]
        self.pos[0] += x_dir * self.speed
        self.pos[2] += z_dir * self.speed

        self.draw()

    def draw(self):
        glPushMatrix()
        glTranslate(self.pos[0], self.pos[1], self.pos[2])
        glCallList(self.displayListIndex)
        glPopMatrix()
