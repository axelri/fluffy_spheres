from math import *
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from vector import Vector
import matrix 
import constants

# PLEASE add new generic object functionality to the Shape class,
# instead of adding it to one of the subclasses

class Shape(object):
    ''' Defines a generic 3D shape with suitable instance variables
    and methods. All other shapes should inherit from this.
    Need to inherit from *object* in order to be fully usable by subclasses.
    Subclasses of Shape must define a method draw_shape with OpenGL
    instructions on how to draw the particular shape in 3D space.'''
    def __init__(self):
        ''' Constructor for the Shape object. Takes one optional
        color argument'''

        # instance variables, these should
        # only be used by the internal methods
        self._xPos = 0
        self._yPos = 0
        self._zPos = 0
    
        self._speed = 0
        self._displayListIndex = self.create_and_get_GL_object()

        # Stores the rotation matrix of the shape, initiates it as identity
        self._rotation = 0.0
        self._rotationAxis = Vector([0.0, 0.0, 0.0])
        self._rotationMatrix = matrix.identity()

        # Jumping variables
        self._jumpTimeLeft = 0 # TODO: Necessary?
        self._jumpSpeed = 0
        self._jumpHeight = 0
        self._jumpTime = 0

        # Direction and speed
        self._velocity = Vector([0.0, 0.0, 0.0])

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
        self.draw_shape() # unique to every subclass
        glEndList()
        return displayListIndex

    def translate_and_rotate(self):
        # TODO: func doc
        glTranslate(self._xPos, self._yPos, self._zPos)
        glMultMatrixf(self._rotationMatrix)

    def move(self, directions):
        ''' Move around in 3D space using the keyboard.
        Takes an array containing X and Z axis directions.
        Directions must be either 1, -1 or 0.'''

        # Set directions
        xDir = directions[0]
        zDir = directions[1]

        # Compute the new position of the sphere
        xVel = xDir * self._speed
        zVel = zDir * self._speed
        self._xPos += xVel
        self._zPos += zVel

        # Calculate the direction the shape moves in
        self._velocity = Vector([xVel, 0.0, zVel])
        self._rotation = self._velocity.norm()  
        # TODO: This needs to be adjusted for the radius of the
        # sphere (shape) in the generic case, but right now the
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
        rot_matrix = matrix.generate_rotation_matrix(self._rotationAxis, self._rotation)
        self._rotationMatrix = matrix.matrix_mult(rot_matrix, self._rotationMatrix)

    def jump(self):
        # TODO: func doc
        if not self._jumpTimeLeft:
            self._jumpTimeLeft = self._jumpTime

    def update_jump(self):
        # TODO: func doc
        # TODO: Ball degradation, lower and lower jumps?
        if self._jumpTimeLeft:
            self._jumpTimeLeft -= 1
            jumpTime = self._jumpTime - self._jumpTimeLeft
            self._yPos = (self._jumpSpeed * jumpTime - 
                    0.005 * jumpTime**2) * self._jumpHeight/4.5
        # The "/4.5" part is there because the maximum of 
        # the equation normally is 4.5

    def update(self):
        ''' Updates the object coordinates and then
        draws the object.'''
        self.update_jump()
        self.draw()

    # external getters and setters for
    # the instance variables.
    # This way our API (the external calls to the object) can remain
    # the same, even if we want to change the class internally

    def get_xPos(self):
        return self._xPos

    def set_xPos(self, xPos):
        self._xPos = xPos

    def get_yPos(self):
        return self._yPos

    def set_yPos(self, yPos):
        self._yPos = yPos

    def get_zPos(self):
        return self._zPos

    def set_zPos(self, zPos):
        self._zPos = zPos

    def get_speed(self):
        return self._speed

    def set_speed(self, speed):
        self._speed = speed

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color

class Sphere(Shape):
    ''' Defines a 3D sphere. Inherits from Shape. Can move
    around in 3D space'''
    def __init__(self, color=constants.SPHERE_COLOR,
                radius=constants.SPHERE_RADIUS):
        ''' Constructor for the Sphere class. Calls the constructor for the
        Shape class. This way the new Sphere object will hold all the
        instance variables and methods defined in the Shape class.'''
        # These variables are important to 
        # OpenGL compilation, and must be
        # initialized prior to calling superclass constructor
        self._color = color
        self._radius = radius
        
        super(Sphere, self).__init__()

        # initialize/set values unique to Sphere
        self._speed = constants.SPHERE_SPEED
        self._jumpSpeed = constants.SPHERE_JUMP_SPEED
        self._jumpHeight = constants.SPHERE_JUMP_HEIGHT
        self._jumpTime = constants.SPHERE_JUMP_TIME

    def draw_shape(self):
        ''' The drawing routine for Sphere (you are welcome to change the
        name if you want to) '''
        glColor3fv(self._color)
        # self._color/self._radius defined only in subclass
        # since draw_shape is unqiue to the subclass
        #glutSolidSphere(self._radius, 40, 40)  # For nicer looking sphere
        glutSolidSphere(self._radius, 10, 10)   # To look at rotation
