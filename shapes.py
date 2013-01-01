import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from vector import * # OK to import with * since it only contains one class def
from matrix import * # TODO: Maybe import instead and use matrix.<some> 
# since we're using as a singleton ('loose functions')
import constants # TODO: Same as above
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
        self.color = constants.SPHERE_COLOR
        
        displayListIndex = self.create_and_get_GL_object()
        super(Sphere, self).__init__(displayListIndex)

        # initiliaze/set values unique to Sphere
        self._speed = constants.SPHERE_SPEED

        self._velocity = Vector([0.0, 0.0, 0.0])

        # Stores the rotation matrix of the sphere, initiates it as identity
        # TODO: refactor to Shape
        self._rotation = 0.0
        self._rotationAxis = Vector([0.0, 0.0, 0.0])
        self._rotationMatrix = identity()

        # TODO: refactor to Shape
        self._jumping = 0
        self._jumpSpeed = constants.SPHERE_JUMP_SPEED
        self._jumpHeight = constants.SPHERE_JUMP_HEIGHT

    def draw_shape(self):
        ''' The drawing routine for Sphere (you are welcome to change the
        name if you want to) '''
        glColor3fv(self.color)
        #glutSolidSphere(1, 40, 40)             # For nicer looking sphere
        glutSolidSphere(1, 10, 10)              # To look at rotation

    def move(self):
        ''' Move around in 3D space using the keyboard.'''
        # TODO: Make generic and move to Shape
        keyState = pygame.key.get_pressed()

        # Take input
        
        # D positive, a negative, 0 if not pressed
        xDir = keyState[K_d] - keyState[K_a]
        zDir = keyState[K_s] - keyState[K_w]

        # Commence jumping if user presses space
        if keyState[K_SPACE]:
            self.jump()

        # Calculate new y-position in the jump
        self.update_jump()

        # Compute the new position of the sphere
        xVel = xDir * self._speed
        zVel = zDir * self._speed
        self._xPos += xVel
        self._zPos += zVel

        # Calculate the direction the sphere moves in
        self._velocity = Vector([xVel, 0.0, zVel])
        self._rotation = self._velocity.norm()  # This needs to be adjusted for the radius of the
                                                # sphere in the generic case, but right now the
                                                # radius is 1 so we don't need to yet
        if self._rotation:
            self._velocity = self._velocity.normalize()

        # Calculate the axis of rotation
        self._rotationAxis = Vector([0, 1, 0]).cross(self._velocity)
                                                # The vector [0,1,0] should really be the normal
                                                # of the surface in the contact point, but that
                                                # can be changed later if we want to make the sphere
                                                # roll on other surfaces than a plain floor.
        
        # Generate a rotation matrix to describe the current rotation
        rot_matrix = generate_rotation_matrix(self._rotationAxis, self._rotation)
        self._rotationMatrix = matrix_mult(rot_matrix, self._rotationMatrix)
        
    def jump(self):
        if not self._jumping:
            self._jumping = constants.SPHERE_JUMP_TIME

    def update_jump(self):
        if self._jumping:
            self._jumping -= 1
            jumpTime = constants.SPHERE_JUMP_TIME - self._jumping
            self._yPos = (self._jumpSpeed * jumpTime - 0.005 * jumpTime**2) * self._jumpHeight/4.5
        # The "/4.5" part is there because the maximum of the equation normally is 4.5

    def translate_and_rotate(self):
        glTranslate(self._xPos, self._yPos, self._zPos)
        glMultMatrixf(self._rotationMatrix)
