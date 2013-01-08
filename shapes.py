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

        self._xPos = 0
        self._yPos = 0
        self._zPos = 0

        self._displayListIndex = self.create_and_get_GL_object()

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

    # External getters and setters for
    # the instance variables.

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

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color

class MovingShape(Shape):
    ''' Defines a moving Shape '''
    def __init__(self):
        super(MovingShape, self).__init__()

        # Direction and speed
        self._velocity = Vector([0.0, 0.0, 0.0])    
        self._speed = 0

        # Jumping variables
        self._jumping = False
        self._jumpSpeed = 0

        # Falling variables
        self._falling = False
        self._fallTime = 0

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
        # NOTE: An involuntary "small bounce" now occurs after a jump because
        # the sphere gets to far down. We can change this, do we want to?
        if self._jumping:
            self._velocity = self._velocity.v_add(Vector([0, self._jumpSpeed \
                                                          / 1000.0, 0]))

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
        ''' Checks if the shape should fall, if so makes it fall.
            If it touches ground, stop falling. '''
        # TODO: The sphere "falls" even though it is held up by the edges
        # of two edges, making it behave unpredictably instead of just lying
        # as it should. Also, when rolling over edges, it falls to fast.
        # Both these problems are because fallTime and velocity increases
        # as if it was falling freely even though it is not. Should be fixed.

            # The sphere touches ground: set on right height, stop falling,
            # stop jumping, reset falltime
        if self._yPos < constants.GROUND_LEVEL:
            self._yPos = constants.GROUND_LEVEL
            self.reset_jump_and_fall()

            # The sphere should fall: make it keep falling
        if self._falling:
            self._fallTime += 1.0
            self._velocity = self._velocity.\
                             v_add(Vector([0.0, - self._fallTime * \
                                           constants.GRAVITY / constants.SLOW_DOWN,
                                                          0.0]))

            # The sphere shouldn't fall, reset falltime
        else:
            self.reset_jump_and_fall()

    # External getters and setters for
    # the instance variables.

    def get_jump_height(self):
        return (self._jumpSpeed * self._maxJumpTime / 2 -
                constants.GRAVITY / 2 * (self._maxJumpTime / 2)**2) / 1000.0

    def set_jump_height(self, height):
        self._jumpSpeed = (height * 2000.0 + constants.GRAVITY * 
                (self._maxJumpTime / 2)**2) / self._maxJumpTime
        self._maxJumpTime = self._jumpSpeed / (constants.GRAVITY / 2)

    def get_speed(self):
        return self._speed

    def set_speed(self, speed):
        self._speed = speed

class RotatingShape(MovingShape):
    ''' Defines a Shape that rotates while it moves.'''
    def __init__(self):
        # Stores the rotation matrix of the shape, initiates it as identity
        self._rotation = 0.0
        self._rotationAxis = Vector([0.0, 0.0, 0.0])
        self._rotationMatrix = matrix.identity()

        super(RotatingShape, self).__init__()

    def move(self, directions, cubelist):
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
            self._rotationAxis = Vector([0.0, 1.0, 0.0]).\
                                 cross(self._velocity.normalize())
        else:
            self._rotationAxis = Vector([0.0, 1.0, 0.0]).cross(self._velocity)
        
        # NOTE: The vector [0,1,0] should really be the normal
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
        for cube in cubelist:
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
        # TODO: The movements around some edges are to jerky, fix.
        # Also, I don't think it takes corners into account, and thus can fall
        # through them
        distance = self.get_distance_shape(cube)

        cubeEdges = cube.get_edges()
        normals = cube.get_normals()
        sideLength = cube.get_side_length()

        unit_vectors = [[Vector('e_y'), Vector('e_z')],
                        [Vector('e_x'), Vector('e_z')],
                        [Vector('e_x'), Vector('e_y')]]

        ### Check if it touches one of the sides ###

                # A little more abstract, but shortens the code by cyclic permutation
        for i in range(3):
            if abs(distance.dot(normals[2*i])) <= sideLength / 2 \
               and abs(distance.dot(normals[2*(i+1)%len(normals)])) <= sideLength / 2 \
               and abs(distance.dot(normals[2*(i+2)%len(normals)])) \
               <= sideLength / 2 + self._radius:
                if distance.dot(normals[2*(i+2)%len(normals)]) < 0:
                    return normals[2*(i+2)%len(normals)]
                else:
                    return normals[(2*(i+2)+1)%len(normals)]

        ### Check if it touches one of the edges ###
                
        for i in range(3):
            EdgeDistance = self.get_abs_distance_edge(cube, cubeEdges[4*i]).\
                           proj_plane(unit_vectors[i][0], unit_vectors[i][1])
            if abs(EdgeDistance.norm()) <= self._radius and \
                abs(distance.dot(normals[2*i])) <= sideLength / 2:
                if distance.dot(normals[2*(i+1)%len(normals)]) < 0:
                    if distance.dot(normals[2*(i+2)%len(normals)]) < 0:
                        return self.get_distance_point(cubeEdges[4*i]).\
                               proj_plane(unit_vectors[i][0], unit_vectors[i][1])
                    else:
                        return self.get_distance_point(cubeEdges[4*i+1]).\
                               proj_plane(unit_vectors[i][0], unit_vectors[i][1])
                else:
                    if distance.dot(normals[2*(i+2)%len(normals)]) < 0:
                        return self.get_distance_point(cubeEdges[4*i+2]).\
                               proj_plane(unit_vectors[i][0], unit_vectors[i][1])
                    else:
                        return self.get_distance_point(cubeEdges[4*i+3]).\
                               proj_plane(unit_vectors[i][0], unit_vectors[i][1])                   

                # The sphere doesn't touch the cube
        else:
            return False

    def get_abs_distance_edge(self, cube, edge):
        ''' Returns the distance from the sphere to the center of the
            closest one of the four edges (defined by edge) of the cube. '''
        edge = edge.get_value()
        sideLength = cube.get_side_length()
        xDist = min([abs(edge[0] - self._xPos), abs(edge[0] - sideLength - self._xPos)])
        yDist = min([abs(edge[1] - self._yPos), abs(edge[1] - sideLength - self._yPos)])
        zDist = min([abs(edge[2] - self._zPos), abs(edge[2] - sideLength - self._zPos)])
        return Vector([xDist, yDist, zDist])
    
    def push(self, cube, side):
        ''' Makes the sphere push the cube on the side of the cube defined by the
        normal vector side '''
        cube.move(side.v_mult(-1.0).get_value())
        self._velocity = self._velocity.v_add(side.v_mult(cube.get_speed()))


    def check_collision(self, cube):
        ''' Checks if there has been a collision between the sphere and a cube,
        defines what to do if so. '''
        distance = self.get_distance_shape(cube)
        side = self.collide_cube(cube)
        sideLength = cube.get_side_length()
        speed = self._velocity.norm()
        self.check_fall(cube, side)
        if side:
                # The sphere is on top of the cube, don't fall through
            if side == cube._upNormal:
                self.reset_jump_and_fall()
                self._yPos = sideLength
                
                # The sphere collides with another side of the cube,
                # push on that side
            elif side in cube.get_normals():
                self.push(cube, side)

                # The collision is with an edge, stop the sphere
                # from moving in that direction
            else:
                self._velocity = self._velocity.v_add(side.v_mult(-speed))

    def check_fall(self, cube, side):
        ''' Checks if the sphere should be falling (is in the air and not
            on top of the cube). If so, fall. '''
        if self._yPos > constants.GROUND_LEVEL and side != cube._upNormal:
                self.fall()

    def get_radius(self):
        return self._radius

class Cube(MovingShape):
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
        self.update_edges()

    def update(self, cubelist):
        # TODO: func doc
        super(Cube, self).update()
        self.update_edges()
        for cube in cubelist:
            if cube != self:
                self.check_collision(cube)

    def update_edges(self):
        ''' Updates the edges of the cube '''
        self._xyEdge1 = Vector([self._xPos + self._side/2, self._yPos + self._side/2, self._zPos])
        self._xyEdge2 = Vector([self._xPos + self._side/2, self._yPos - self._side/2, self._zPos])
        self._xyEdge3 = Vector([self._xPos - self._side/2, self._yPos + self._side/2, self._zPos])
        self._xyEdge4 = Vector([self._xPos - self._side/2, self._yPos - self._side/2, self._zPos])
        
        self._xzEdge1 = Vector([self._xPos + self._side/2, self._yPos, self._zPos + self._side/2])
        self._xzEdge2 = Vector([self._xPos + self._side/2, self._yPos, self._zPos - self._side/2])
        self._xzEdge3 = Vector([self._xPos - self._side/2, self._yPos, self._zPos + self._side/2])
        self._xzEdge4 = Vector([self._xPos - self._side/2, self._yPos, self._zPos - self._side/2])
        
        self._yzEdge1 = Vector([self._xPos, self._yPos + self._side/2, self._zPos + self._side/2])
        self._yzEdge2 = Vector([self._xPos, self._yPos - self._side/2, self._zPos + self._side/2])
        self._yzEdge3 = Vector([self._xPos, self._yPos + self._side/2, self._zPos - self._side/2])
        self._yzEdge4 = Vector([self._xPos, self._yPos - self._side/2, self._zPos - self._side/2])

    def draw_shape(self):
        ''' The drawing routine for Cube. '''
        glColor3fv(self._color)
        glutSolidCube(self._side)

    def push(self, cube2, side):
        ''' Makes the sphere push the cube on the side of the cube defined by the
        normal vector side '''
        cube2.move(side.v_mult(-1.0).get_value())

    def collide_cube(self, cube2):
        ''' Checks if the cube has collided with another cube.
        If there was a collision, return the normal of the side that
        the sphere collided with, else return False.
        (Very specific, might need to get more general) '''

        distance = self.get_distance_shape(cube2)

        normals = cube2.get_normals()
        sideLength = cube2.get_side_length()

        # TODO: Edit so that it can return other sides than front and back.
        for i in range(3):
            if abs(distance.dot(normals[2*i])) <= sideLength / 2 + self._side / 2 \
               and abs(distance.dot(normals[2*(i+1)%len(normals)])) <= sideLength / 2 + self._side / 2 \
               and abs(distance.dot(normals[2*(i+2)%len(normals)])) \
               <= sideLength / 2 + self._side / 2:
                if distance.dot(normals[2*(i+2)%len(normals)]) < 0:
                    return normals[2*(i+2)%len(normals)]
                else:
                    return normals[(2*(i+2)+1)%len(normals)]

    def check_collision(self, cube2):
        ''' Checks if there has been a collision between the cube and another cube,
        defines what to do if so. '''
        distance = self.get_distance_shape(cube2)
        side = self.collide_cube(cube2)
        sideLength = cube2.get_side_length()
        self.check_fall(cube2, side)
        if side:
                # The sphere is on top of the cube, don't fall through
            if side == cube2._upNormal:
                self.reset_jump_and_fall()
                self._yPos = sideLength
                
                # The sphere collides with another side of the cube,
                # push on that side
            elif side in cube2.get_normals():
                self.push(cube2, side)

    def check_fall(self, cube2, side):
        ''' Checks if the cube should be falling (is in the air and not
            on top of another cube). If so, fall. '''
        if self._yPos > constants.GROUND_LEVEL and side != cube2._upNormal:
                self.fall()

    # Getters and setters

    def get_side_length(self):
        ''' Returns the side length of the cube '''
        return self._side

    def get_normals(self):
        ''' Returns the normals of the cube's sides '''
        return [self._rightNormal, self._leftNormal,
                         self._upNormal, self._downNormal,
                         self._frontNormal, self._backNormal]
        
    def get_edges(self):
        ''' Returns the edges of the cube '''
        return [self._yzEdge1, self._yzEdge2, self._yzEdge3, self._yzEdge4,
                self._xzEdge1, self._xzEdge2, self._xzEdge3, self._xzEdge4,
                self._xyEdge1, self._xyEdge2, self._xyEdge3, self._xyEdge4]
