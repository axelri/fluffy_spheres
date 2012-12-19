import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

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
