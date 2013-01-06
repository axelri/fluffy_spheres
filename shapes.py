from math import *
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from vector import Vector
import matrix 
import constants

class Shape(object):
    ''' Defines a generic 3D shape with suitable instance variables
    and methods. All other shapes should inherit from this.
    Need to inherit from *object* in order to be fully usable by subclasses.
    Subclasses of Shape must define a method draw_shape with OpenGL
    instructions on how to draw the particular shape in 3D space.'''
    def __init__(self):
        ''' Constructor for the Shape object. Takes one optional
        color argument'''
        # TODO: maybe better to make Shape an abstract base class?
        # check out the abc module in python
        if self.__class__.__name__ == 'Shape':
            raise Exception('Shape must be subclassed in order to be used!')

        # instance variables, these should
        # only be used by the internal methods
        self._xPos = 0
        self._yPos = 0
        self._zPos = 0

        # Direction and speed
        self._velocity = Vector([0.0, 0.0, 0.0])    
        self._speed = 0
        self._displayListIndex = self.create_and_get_GL_object()

        # Jumping variables
        self._jumping = False
        self._jumpSpeed = 0

        # Falling variables
        self._falling = False
        self._fallTime = 0

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

    def translate_and_rotate(self):
        ''' Translates and rotates the shape to the current position '''
        glTranslate(self._xPos, self._yPos, self._zPos)

    def move(self, directions):
        ''' Move around in 3D space using the keyboard.
        Takes an array containing X and Z axis directions.
        Directions must be either 1, -1 or 0.'''

        # Set directions
        xDir = directions[0]
        zDir = directions[2]

        # Compute the new position of the sphere
        xVel = xDir * self._speed
        zVel = zDir * self._speed
        self._xPos += xVel
        self._zPos += zVel
        self._velocity = Vector([xVel, 0, zVel])


    def jump(self):
        ''' Is called to make the shape jump, sets self._jumping to True '''
        # NOTE: The object must also be falling in order to return to ground;
        # for the sphere this is fixed by check_fall()
        self._jumping = True

    def update_jump(self):
        ''' Checks if the shape should jump, if so makes it continue along the
        jumping parabola '''
        # TODO: Small bounce after jump?
        # NOTE: An involuntary "small bounce" now occurs after a jump because the sphere gets to far down.
        # We can change this, do we want to?
        if self._jumping:
            self._velocity = self._velocity.v_add(Vector([0, self._jumpSpeed / 1000.0, 0]))

    def fall(self):
        ''' Makes the shape fall. '''
        self._falling = True

    def reset_jump_and_fall(self):
        ''' Makes the shape stop jumping and falling, resets fallTime '''
        if self._jumping:
            self._jumping = False
        if self._falling:
            self._falling = False
            self._fallTime = 0

    def update_fall(self):
        ''' Checks if the shape should fall, if so makes it fall. If it touches ground, stop falling. '''

            # The sphere touches ground: set on right height, stop falling, stop jumping, reset falltime
        if self._yPos < constants.GROUND_LEVEL:
            self._yPos = constants.GROUND_LEVEL
            self.reset_jump_and_fall()

            # The sphere should fall: make it keep falling
        if self._falling:
            self._fallTime += 1.0
            self._velocity = self._velocity.v_add(Vector([0.0, - self._fallTime * constants.GRAVITY \
                                                          / constants.SLOW_DOWN , 0.0]))

            # The sphere shouldn't fall, reset falltime
        else:
            self.reset_jump_and_fall()

    def update(self):
        ''' Updates the object coordinates and then
        draws the object.'''
        self.draw()

    def get_distance_shape(self, shape2):
        ''' Returns the distance between the positions of
            self and shape2 as a vector '''
        return Vector([shape2._xPos - self._xPos,
                       shape2._yPos - self._yPos,
                       shape2._zPos - self._zPos])

    def get_distance_point(self, point):
        ''' Returns the distance between the position of the shape
            and a point as a vector '''
        if point.__class__.__name__ == 'Vector':
            p = point.get_value()
        else:
            p = point
        return Vector([p[0] - self._xPos,
                       p[1] - self._yPos,
                       p[2] - self._zPos])

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

    def get_jump_height(self):
        return (self._jumpSpeed * self._maxJumpTime / 2 -
                constants.GRAVITY / 2 * (self._maxJumpTime / 2)**2) / 1000.0

    def set_jump_height(self, height):
        self._jumpSpeed = (height * 2000.0 + constants.GRAVITY * 
                (self._maxJumpTime / 2)**2) / self._maxJumpTime
        self._maxJumpTime = self._jumpSpeed / (constants.GRAVITY / 2)

class RotatingShape(Shape):
    ''' Defines a Shape that rotates while it moves.'''
    def __init__(self):
        # Stores the rotation matrix of the shape, initiates it as identity
        self._rotation = 0.0
        self._rotationAxis = Vector([0.0, 0.0, 0.0])
        self._rotationMatrix = matrix.identity()

        super(RotatingShape, self).__init__()

    def move(self, directions, cube):
        ''' Move around in 3D space using the keyboard.
        Takes an array containing X and Z axis directions.
        Directions must be either 1, -1 or 0.'''

        # TODO: should probably use super instead, but
        # the local variables make it hard.
        # Set directions
        xDir = directions[0]
        zDir = directions[2]

        # Compute the new position of the sphere
        xVel = xDir * self._speed
        zVel = zDir * self._speed

        # Calculate the direction the shape moves in
        self._velocity = Vector([xVel, 0.0, zVel])
        self._rotation = self._velocity.norm() / self._radius

        # Calculate the axis of rotation
        if self._rotation:
            self._rotationAxis = Vector([0.0, 1.0, 0.0]).cross(self._velocity.normalize())
        else:
            self._rotationAxis = Vector([0.0, 1.0, 0.0]).cross(self._velocity)
        
        # The vector [0,1,0] should really be the normal
        # of the surface in the contact point, but that
        # can be changed later if we want to make the sphere
        # roll on other surfaces than a plain floor.
        
        # Generate a rotation matrix to describe the current rotation
        rot_matrix = matrix.generate_rotation_matrix(self._rotationAxis, self._rotation)
        self._rotationMatrix = matrix.matrix_mult(rot_matrix, self._rotationMatrix)

        # Adjust the norm of velocity
        self._velocity = self._velocity.v_mult(self._rotation)

        # Update velocity in y-direction
        self.update_jump()
        self.update_fall()
        
        # Check if there was a collision with cube
        self.check_collision(cube)

        # Calculate new position
        Vel = self._velocity.get_value()
        self._xPos += Vel[0]
        self._yPos += Vel[1]
        self._zPos += Vel[2]

    def translate_and_rotate(self):
        ''' Translates and rotates the shape to the current position '''
        # Translate according to parent class
        super(RotatingShape, self).translate_and_rotate()
        # Do rotation unique to the subclass
        glMultMatrixf(self._rotationMatrix)

class Sphere(RotatingShape):
    ''' Defines a 3D sphere. Can move around (roll) in 3D space'''
    def __init__(self, color=constants.SPHERE_COLOR,
                radius=constants.SPHERE_RADIUS):
        ''' Constructor for the Sphere class. Calls the constructor for the
        Shape class. This way the new Sphere object will hold all the
        instance variables and methods defined in the Shape class.'''
        self._color = color
        self._radius = radius
        
        super(Sphere, self).__init__()

        # Initialize/set values unique to Sphere
        self._speed = constants.SPHERE_SPEED
        self._jumpSpeed = constants.SPHERE_JUMP_SPEED
        self._maxJumpTime = self._jumpSpeed / (constants.GRAVITY / 2)

    def draw_shape(self):
        ''' The drawing routine for Sphere '''
        glColor3fv(self._color)
        #glutSolidSphere(self._radius, 40, 40)  # For nicer looking sphere
        glutSolidSphere(self._radius, 10, 10)   # To look at rotation

    def collide_cube(self, cube):
        ''' Checks if the sphere has collided with the cube.
        If there was a collision, return the normal of the side that
        the sphere collided with, else return False. If it collides with an
        edge, return the distance vector from the center of the sphere
        to the edge, projected on the corresponding plane (this represents
        the "normal" of the edge).
        (Very specific, might need to get more general) '''
        # TODO: Remove redundance in the code (is it possible to calculate which side or edge
        # the sphere collides with in one call, e.g. a for-loop, instead of three ifs?)
        distance = self.get_distance_shape(cube)
        cubeEdges = cube.get_edges()
        xyEdgeDistance = self.get_abs_distance_edge(cube, cubeEdges[0]).proj_plane(Vector([1.0, 0.0, 0.0]), Vector([0.0, 1.0, 0.0]))
        xzEdgeDistance = self.get_abs_distance_edge(cube, cubeEdges[1]).proj_plane(Vector([1.0, 0.0, 0.0]), Vector([0.0, 0.0, 1.0]))
        yzEdgeDistance = self.get_abs_distance_edge(cube, cubeEdges[2]).proj_plane(Vector([0.0, 1.0, 0.0]), Vector([0.0, 0.0, 1.0]))

        ### Check if it touches one of the sides ###

                # The sphere touches either the front or the back side of the cube
        if abs(distance.dot(cube._leftNormal)) <= cube._side / 2 \
           and abs(distance.dot(cube._upNormal)) <= cube._side / 2 \
           and abs(distance.dot(cube._frontNormal)) <= cube._side / 2 + self._radius:
                # Check which
            if distance.dot(cube._frontNormal) > 0:
                return cube._backNormal
            else:
                return cube._frontNormal
            
                # The sphere touches either the left or right side of the cube
        elif abs(distance.dot(cube._frontNormal)) <= cube._side / 2 \
             and abs(distance.dot(cube._upNormal)) <= cube._side / 2 \
             and abs(distance.dot(cube._leftNormal)) <= cube._side / 2 + self._radius:
                # Check which
            if distance.dot(cube._leftNormal) > 0:
                return cube._rightNormal
            else:
                return cube._leftNormal
            
                # The sphere touches either the top or bottom of the cube
        elif abs(distance.dot(cube._frontNormal)) <= cube._side / 2 \
             and abs(distance.dot(cube._leftNormal)) <= cube._side / 2 \
             and abs(distance.dot(cube._upNormal)) <= cube._side / 2 + self._radius:
                # Check which
            if distance.dot(cube._upNormal) > 0:
                return cube._downNormal
            else:
                return cube._upNormal

        ### Check if it touches one of the edges ###
            
                # The sphere touches an xyEdge of the cube
        elif abs(xyEdgeDistance.norm()) <= self._radius and \
            abs(distance.dot(cube._frontNormal)) <= cube._side / 2:
            edge = cubeEdges[0].get_value()
                # The sphere touches one of the right xyEdges
            if distance.dot(cube._leftNormal) > 0:
                # Check which
                if distance.dot(cube._upNormal) > 0:
                    # Lower right xyEdge
                    return self.get_distance_point([edge[0], edge[1] - cube._side, edge[2]]).proj_plane(Vector([1.0, 0.0, 0.0]), Vector([0.0, 1.0, 0.0]))
                else:
                    # Upper right xyEdge
                    return self.get_distance_point([edge[0], edge[1], edge[2]]).proj_plane(Vector([1.0, 0.0, 0.0]), Vector([0.0, 1.0, 0.0]))
                # The sphere touches one of the left xyEdges
            else:
                if distance.dot(cube._upNormal) > 0:
                    # Lower left xyEdge
                    return self.get_distance_point([edge[0] - cube._side, edge[1] - cube._side, edge[2]]).proj_plane(Vector([1.0, 0.0, 0.0]), Vector([0.0, 1.0, 0.0]))
                else:
                    # Upper left xyEdge
                    return self.get_distance_point([edge[0] - cube._side, edge[1], edge[2]]).proj_plane(Vector([1.0, 0.0, 0.0]), Vector([0.0, 1.0, 0.0]))

                # The sphere touches an xzEdge of the cube
        elif abs(xzEdgeDistance.norm()) <= self._radius and \
            abs(distance.dot(cube._upNormal)) <= cube._side / 2:
            edge = cubeEdges[1].get_value()
                # The sphere touches one of the right xzEdges
            if distance.dot(cube._leftNormal) > 0:
                # Check which
                if distance.dot(cube._frontNormal) > 0:
                    # Farther right xyEdge
                    return self.get_distance_point([edge[0], edge[1], edge[2] - cube._side]).proj_plane(Vector([1.0, 0.0, 0.0]), Vector([0.0, 0.0, 1.0]))
                else:
                    # Nearer right xzEdge
                    return self.get_distance_point([edge[0], edge[1], edge[2]]).proj_plane(Vector([1.0, 0.0, 0.0]), Vector([0.0, 0.0, 1.0]))
                # The sphere touches one of the left xzEdges
            else:
                if distance.dot(cube._frontNormal) > 0:
                    # Farther left xzEdge
                    return self.get_distance_point([edge[0] - cube._side, edge[1], edge[2] - cube._side]).proj_plane(Vector([1.0, 0.0, 0.0]), Vector([0.0, 0.0, 1.0]))
                else:
                    # Nearer left xzEdge
                    return self.get_distance_point([edge[0] - cube._side, edge[1], edge[2]]).proj_plane(Vector([1.0, 0.0, 0.0]), Vector([0.0, 0.0, 1.0]))

                # The sphere touches an yzEdge of the cube
        elif abs(yzEdgeDistance.norm()) <= self._radius and \
            abs(distance.dot(cube._leftNormal)) <= cube._side / 2:
            edge = cubeEdges[2].get_value()
                # The sphere touches one of the farther yzEdges
            if distance.dot(cube._frontNormal) > 0:
                # Check which
                if distance.dot(cube._upNormal) > 0:
                    # Lower farther yzEdge
                    return self.get_distance_point([edge[0], edge[1] - cube._side, edge[2] - cube._side]).proj_plane(Vector([0.0, 1.0, 0.0]), Vector([0.0, 0.0, 1.0]))
                else:
                    # Upper farther yzEdge
                    return self.get_distance_point([edge[0], edge[1], edge[2] - cube._side]).proj_plane(Vector([0.0, 1.0, 0.0]), Vector([0.0, 0.0, 1.0]))
                # The sphere touches one of the nearer yzEdges
            else:
                if distance.dot(cube._upNormal) > 0:
                    # Lower nearer yzEdge
                    return self.get_distance_point([edge[0], edge[1] - cube._side, edge[2]]).proj_plane(Vector([0.0, 1.0, 0.0]), Vector([0.0, 0.0, 1.0]))
                else:
                    # Upper nearer yzEdge
                    return self.get_distance_point([edge[0], edge[1], edge[2]]).proj_plane(Vector([0.0, 1.0, 0.0]), Vector([0.0, 0.0, 1.0]))

                # The sphere doesn't touch the cube
        else:
            return False

    def get_abs_distance_edge(self, cube, edge):
        ''' Returns the distance from the sphere to the center of the
            closest one of the four edges (defined by edge) of the cube. '''
        edge = edge.get_value()
        xDist = min([abs(edge[0] - self._xPos), abs(edge[0] - cube._side - self._xPos)])
        yDist = min([abs(edge[1] - self._yPos), abs(edge[1] - cube._side - self._yPos)])
        zDist = min([abs(edge[2] - self._zPos), abs(edge[2] - cube._side - self._zPos)])
        return Vector([xDist, yDist, zDist])
    
    def push(self, cube, side):
        ''' Makes the sphere push the cube on the side of the cube defined by the
        normal vector side '''
        cube.move(side.v_mult(-1.0).get_value())
        self._velocity = self._velocity.v_add(side.v_mult(cube._speed))


    def check_collision(self, cube):
        ''' Checks if there has been a collision between the sphere and a cube,
        defines what to do if so. '''
        distance = self.get_distance_shape(cube)
        side = self.collide_cube(cube)
        speed = self._velocity.norm()
        self.check_fall(cube, side)
        if side:
                # The sphere is on top of the cube, don't fall thru
            if side == cube._upNormal:
                self.reset_jump_and_fall()
                self._yPos = cube._side
                
                # The sphere collides with another side of the cube, push on that side
            elif side in cube.get_normals():
                self.push(cube, side)
                # The collision is with an edge, stop the cube from moving in that direction
            else:
                self._velocity = self._velocity.v_add(side.v_mult(-speed))
                


    def check_fall(self, cube, side):
        ''' Checks if the sphere should be falling (is in the air and not on top of the cube)
        If so, fall. '''
        if self._yPos > 0 and side != cube._upNormal:
                self.fall()

class Cube(Shape):
    ''' Defines a 3D cube. Can move around (glide) in 3D space.'''
    def __init__(self, color=constants.CUBE_COLOR,
                side=constants.CUBE_SIDE):
        self._color = color
        self._side = side

        super(Cube, self).__init__()

        self._speed = constants.CUBE_SPEED
        self._jumpSpeed = constants.CUBE_JUMP_SPEED
        self._maxJumpTime = self._jumpSpeed / (constants.GRAVITY / 2)

        # Normals to the sides of the cube, must be updated if we decide to
        # rotate the cube, otherwise they are constant
        self._rightNormal = Vector([1.0, 0.0, 0.0])
        self._leftNormal = Vector([-1.0, 0.0, 0.0])
        self._upNormal = Vector([0.0, 1.0, 0.0])
        self._downNormal = Vector([0.0, -1.0, 0.0])
        self._frontNormal = Vector([0.0, 0.0, 1.0])
        self._backNormal = Vector([0.0, 0.0, -1.0])

        # Defines the edges of the cube for better collision
        self._xyEdges = Vector([self._xPos + self._side/2, self._yPos + self._side/2, self._zPos])
        self._xzEdges = Vector([self._xPos + self._side/2, self._yPos, self._zPos + self._side/2])
        self._yzEdges = Vector([self._xPos, self._yPos + self._side/2, self._zPos + self._side/2])

    def get_normals(self):
        ''' Returns the normals of the cube '''
        return [self._rightNormal, self._leftNormal,
                         self._upNormal, self._downNormal,
                         self._frontNormal, self._backNormal]
        
    def get_edges(self):
        ''' Returns the edges of the cube '''
        return [self._xyEdges, self._xzEdges, self._yzEdges]

    def update_edges(self):
        ''' Updates the edges of the cube '''
        self._xyEdges = Vector([self._xPos + self._side/2, self._yPos + self._side/2, self._zPos])
        self._xzEdges = Vector([self._xPos + self._side/2, self._yPos, self._zPos + self._side/2])
        self._yzEdges = Vector([self._xPos, self._yPos + self._side/2, self._zPos + self._side/2])
        #print "edges", self._xyEdges.get_value(), self._xzEdges.get_value(), self._yzEdges.get_value()

    def draw_shape(self):
        ''' The drawing routine for Cube. '''
        glColor3fv(self._color)
        glutSolidCube(self._side)
