# TODO: Split to multiple files? I think that we are beginning to loose
# the clarity, it is too long... I suggest to have the abstract classes:
# Shape, MovingShape and RotatingShape in one file, and the other ones:
# Sphere, Surface and Cube in another. Any thoughts on that Axel?

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

    def get_center(self):
        return [self._xPos, self._yPos, self._zPos]

    def set_center(self, center):
        self._xPos, self._yPos, self._zPos = center[0], center[1], center[2]

    def move_center(self, movement):
        self._xPos += movement[0]
        self._yPos += movement[1]
        self._zPos += movement[2]

class Surface(Shape):
    ''' Defines a surface '''
    def __init__(self, length = constants.SURFACE_SIZE,
                 width = constants.SURFACE_SIZE,
                 center = [0.0, constants.GROUND_LEVEL, 0.0], 
                 normal = Vector('e_y'),
                 color = constants.SURFACE_COLOR,
                 friction = constants.FRICTION):
        self._color = color
        self._length = length       # (if normal is 'e_y', this is size in z-direction)
        self._width = width         # (if normal is 'e_y', this is size in x-direction)
        self._normal = normal
        self._friction = friction
        if self._normal.norm() != 1.0:
            if self._normal.norm() == 0.0:
                raise Exception('The normal cannot be a zero vector!')
            self._normal = self._normal.normalize()
        self._center = center
        # The direction in which the "length will be drawn"
        self._lengthDir = Vector('e_x').cross(self._normal) 
        if self._lengthDir.norm() == 0.0: # The normal is parallell to 'e_x'
            self._lengthDir = Vector('e_z')
        # The direction in which the "width will be drawn"        
        self._widthDir = self._normal.cross(Vector('e_z'))
        if self._widthDir.norm() == 0.0: # The normal is parallell to 'e_z'
            self._widthDir = Vector('e_x')

        # The "absolute value of the length-position of the points"
        lengthPos = self._lengthDir.v_mult(self._length)
        # The "absolute value of the width-position of the points"
        widthPos = self._widthDir.v_mult(self._width)
        
        self._initPoints = [lengthPos.v_mult(-1.0).v_add(widthPos.v_mult(-1.0)).get_value(),
                        lengthPos.v_mult(-1.0).v_add(widthPos).get_value(),
                        lengthPos.v_add(widthPos).get_value(),
                        lengthPos.v_add(widthPos.v_mult(-1.0)).get_value()]

        # TODO: Quite ugly solution, fix?
        self._points = self._initPoints
        super(Surface, self).__init__()

        self.set_center(self._center)

        self.update_points()
                       

    def draw_shape(self):
        glBegin(GL_QUADS)
        glColor4fv(self._color)
        glNormal3fv(self._normal.get_value())
        for point in self._points:
            glVertex3fv(point)
        glEnd()   

    def update_points(self):
        ''' Updates the surfaces points to the current location of the surface '''
        self._points = [Vector(self._initPoints[0]).v_add(Vector(self._center)).get_value(),
                        Vector(self._initPoints[1]).v_add(Vector(self._center)).get_value(),
                        Vector(self._initPoints[2]).v_add(Vector(self._center)).get_value(),
                        Vector(self._initPoints[3]).v_add(Vector(self._center)).get_value()]

        # TODO: Remove? Do we need them?
        self._edges = [[self._points[0], self._points[1]],
                       [self._points[1], self._points[2]],
                       [self._points[2], self._points[3]],
                       [self._points[3], self._points[0]]]        

    def get_points(self):
        return self._points

    def get_edges(self):
        return self._edges

    def get_normal(self):
        return self._normal

    def get_surface_vectors(self):
        return [self._widthDir, self._normal, self._lengthDir]

    def get_size(self):
        return [self._length, self._width]

    def get_friction(self):
        return self._friction

class MovingShape(Shape):
    ''' Defines a moving Shape '''
    # TODO: Make acceleration/force an instance variable? I think it might simplify
    # some of the functions, as it is right now it either needs to be a global or
    # be passed as an argument.
    def __init__(self):
        super(MovingShape, self).__init__()

        # Direction and speed
        self._velocity = Vector()    
        self._speed = 0

        # Jumping variables
        self._jumping = False
        self._jumpSpeed = 0

        self.set_yPos(self.get_border_distance())

    def move(self, directions, *args):
        ''' Move around in 3D space using the keyboard.
        Takes an array containing X , Y and Z axis directions.
        Directions must be either 1, -1 or 0.'''
        acceleration = args[0]
        direction = Vector(directions)

        if direction.norm():
            direction = direction.normalize().v_mult(self._speed)

        self._velocity = self._velocity.v_add(acceleration)

                # Calculate new position
        movementDir = self._velocity.v_add(direction)
        movement = movementDir.get_value()
        self._xPos += movement[0]
        self._yPos += movement[1]
        self._zPos += movement[2]
        return movementDir

    def collision_control(self, surfaceList, acceleration, currentFloor = Vector('e_y'),
                          currentFloorDot = 0.0):
        ''' Checks if the shape has collided with the surfaces
            in surfaceList, returns the acceleration the shape
            is affected by and the normal of the "flooriest"
            surface it has collided with. '''
        
        for surface in surfaceList:
            acceleration, normal = self.check_collision(surface, acceleration)
            currentFloor, currentFloorDot = self.check_floor(normal, currentFloor, currentFloorDot)

        return acceleration, currentFloor

    def check_floor(self, normal, currentFloor, currentFloorDot):
        newFloorDot = normal.dot(Vector('e_y'))
        if newFloorDot > currentFloorDot:
            currentFloorDot = newFloorDot
            currentFloor = normal
        return currentFloor, currentFloorDot

    def update(self, surfaceList, directions = [0.0, 0.0, 0.0],
               acceleration = constants.GRAV_ACC, currentFloor = Vector('e_y'),
               currentFloorDot = 0.0):
        ''' Checks for collision, then moves and draws the shape. '''
        acceleration, floor = self.collision_control(surfaceList, acceleration, currentFloor,
                          currentFloorDot)
        self.move(directions, acceleration, floor)
        super(MovingShape, self).update()
    

    def jump(self):
        ''' Is called to make the shape jump. If self._jumping is False
            sets self._jumping to True and adds a velocity upwards to
            self._velocity '''

        if not self._jumping:
            self._velocity = self._velocity.v_add(Vector([0, self._jumpSpeed \
                                                          / constants.SLOW_DOWN, 0]))
            self._jumping = True

    def reset_jump(self):
        ''' Resets jumping to False '''
        self._jumping = False

    def collide(self, surface):
        ''' Checks if the shape has collided with the surface.
            If it has, return True, else return False. '''
        points = surface.get_points()

        surfaceVectors = surface.get_surface_vectors()
        normal = surfaceVectors[1]
        size = surface.get_size()

        distance = Vector(self.get_center()).distance_vector(Vector(surface.get_center()))

        if abs(distance.dot(surfaceVectors[0])) < size[1]  \
           and abs(distance.dot(surfaceVectors[2])) < size[0]  \
           and abs(distance.dot(normal)) <= self.get_border_distance() \
           + abs(self._velocity.dot(normal)):
            return normal, normal.v_mult(distance.dot(normal))
        else:
            return False, normal.v_mult(distance.dot(normal))


    def check_collision(self, surface, acceleration):
        ''' Checks if the shape has collided with the surface,
            returns the acceleration the surface affects the
            shape with. '''
        normal, distance = self.collide(surface)
        if normal:
            #print "collided with", normal.get_value()
            acceleration = acceleration.v_add(normal.v_mult(-normal.dot(constants.GRAV_ACC)))
            self._velocity = self._velocity.v_add(self._velocity.v_mult(-surface.get_friction()))
            if distance.norm() < self.get_border_distance():
                self.move_center(normal.v_mult(self.get_border_distance()-distance.norm()).get_value())
            if self._velocity.dot(normal) < 0.0:
                self.reset_jump()
                acceleration = acceleration.v_add(normal.v_mult(-normal.dot(self._velocity)))
        
            return acceleration, normal
        return acceleration, Vector()

    # External getters and setters for
    # the instance variables.

    def get_jump_height(self):
        return (self._jumpSpeed * self._maxJumpTime / 2 -
                constants.GRAVITY / 2 * (self._maxJumpTime / 2)**2) \
                / constants.SLOW_DOWN

    def set_jump_height(self, height):
        self._jumpSpeed = (height * 2 * constants.SLOW_DOWN + constants.GRAVITY * 
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
        self._rotationMatrix = matrix.identity()

        super(RotatingShape, self).__init__()

    def move(self, directions, *args):
        # TODO: refactor first half to MovingShape
        # TODO: The rotation behaves strangely while falling, fix?
        ''' Move around in 3D space using the keyboard.
        Takes an array containing X and Z axis directions.
        Directions must be either 1, -1 or 0.'''
        floor = args[1]
        moveDir = super(RotatingShape, self).move(directions, *args)

        if self._jumping:
            moveDir = moveDir.proj_plane(Vector('e_x'), Vector('e_z'))

        # Angle of the rotation that will be executed, in radians
        rotation = moveDir.norm() / self._radius
        rotationAxis = floor.cross(moveDir)
        
        # Generate a rotation matrix to describe the current rotation
        rot_matrix = matrix.generate_rotation_matrix(rotationAxis, rotation)
        self._rotationMatrix = matrix.matrix_mult(rot_matrix, self._rotationMatrix)


    def translate_and_rotate(self):
        ''' Translates and rotates the shape to the current position '''
        super(RotatingShape, self).translate_and_rotate()
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
        glColor4fv(self._color)
        # glutSolidSphere(self._radius, 40, 40)  # For nicer looking sphere
        # glutSolidSphere(self._radius, 10, 10)   # To look at rotation
        glutSolidSphere(self._radius, 10, 40)   # To look at rotation
        # glutWireTeapot(self._radius)

    def collide(self, surface):
        ''' Checks if the sphere has collided with the surface,
            if so return the normal to the side. If it has collided
            with an edge of the surface, return the distance vector
            from the center of the sphere to the edge, projected on
            the corresponding plane (this represents the "normal"
            of the edge).'''
        normal1, distance1 = super(Sphere, self).collide(surface)
        normal2, distance2 = self.collide_edge(surface)
        if normal1:
            return normal1, distance1
        elif normal2:
            return normal2, distance2
        else:
            return False, distance1

    def collide_edge(self, surface):
        ''' Checks if the sphere has collided with an edge '''
        points = surface.get_points()

        surfaceVectors = surface.get_surface_vectors()
        normal = surfaceVectors[1]
        size = surface.get_size()

        edgeVectors = [surfaceVectors[2],
                   surfaceVectors[0],
                   surfaceVectors[2].v_mult(-1.0),
                   surfaceVectors[0].v_mult(-1.0)]

        for i in range(4):
            distance = Vector(points[i]).distance_vector(Vector(self.get_center()))\
                       .proj_plane(normal, edgeVectors[i])
            if distance.norm() <= self.get_radius() and \
               abs(distance.dot(edgeVectors[(i+1)%4])) < size[(i+1)%2]/2:
                print "Collided with edge", distance.get_value()
                print "Normal:", normal.get_value(), '\n'
                return distance.normalize(), distance
        return False, distance

    def collide_cube(self, cube, acceleration):
        # TODO: func doc
        acceleration, currentFloor = self.collision_control(cube.get_surfaces(), acceleration)

        
##        for side in cube.get_surfaces():
##            acceleration, normal = self.check_collision(side, acceleration)
####            currentFloor, currentFloorDot = self.check_floor(normal, currentFloor, currentFloorDot)
####            print "the acceleration is:", acceleration.get_value()
####            if normal.norm() < 0.0:
####                self.push(cube, normal)
        return acceleration, currentFloor

    def update(self, surfaceList, cubeList, directions = [0.0, 0.0, 0.0],
               acceleration = constants.GRAV_ACC):
        ''' Checks for collisions, updates position, draws sphere. '''
##        currentCubeFloor = Vector('e_y')
##        currentCubeFloorDot = 0.0
##        for cube in cubeList:
##            acceleration, cubeFloor = self.collide_cube(cube, acceleration)
##            currentCubeFloor, currentCubeFloorDot = self.check_floor(cubeFloor,
##                                                                     currentCubeFloor,
##                                                                     currentCubeFloorDot)
        super(Sphere, self).update(surfaceList, directions, acceleration)#, currentCubeFloor,
                                   #currentCubeFloorDot)
            


    def push(self, cube, side):
        ''' Makes the sphere push the cube on the side of the cube defined by the
        normal vector side '''
        cube.move(side.v_mult(-1.0).get_value())
        self._velocity = self._velocity.v_add(side.v_mult(cube.get_speed()))

    def get_border_distance(self):
        return self._radius

    def get_radius(self):
        return self._radius

class Cube(MovingShape):
    ''' Defines a 3D cube. Can move around (glide) in 3D space.'''
    # NOTE: To enable rotation while colliding: up vector should be the
    # surface normal in the collision point.
    def __init__(self, color=constants.CUBE_COLOR,
                side=constants.CUBE_SIDE):
        self._color = color
        self._side = side

        super(Cube, self).__init__()

        self._speed = constants.CUBE_SPEED
        self._jumpSpeed = constants.CUBE_JUMP_SPEED
        self._maxJumpTime = self._jumpSpeed / (constants.GRAVITY / 2)

        self._rightSurface = Surface(length = self._side / 2.0,
                                     width = self._side / 2.0,
                                     center = [self._xPos + self._side / 2.0,
                                               self._yPos,
                                               self._zPos],
                                     normal = Vector('e_x'),
                                     color = [0.0, 1.0, 0.0, 0.5])
        self._leftSurface = Surface(length = self._side / 2.0,
                                     width = self._side / 2.0,
                                     center = [self._xPos - self._side / 2.0,
                                               self._yPos,
                                               self._zPos],
                                     normal = Vector('e_x').v_mult(-1.0),
                                     color = [0.0, 1.0, 0.0, 0.5])
        self._upSurface = Surface(length = self._side / 2.0,
                                     width = self._side / 2.0,
                                     center = [self._xPos,
                                               self._yPos + self._side / 2.0,
                                               self._zPos],
                                     normal = Vector('e_y'),
                                     color = [0.0, 1.0, 0.0, 0.5])
        self._downSurface = Surface(length = self._side / 2.0,
                                     width = self._side / 2.0,
                                     center = [self._xPos,
                                               self._yPos - self._side / 2.0,
                                               self._zPos],
                                     normal = Vector('e_y').v_mult(-1.0),
                                     color = [0.0, 1.0, 0.0, 0.5])
        self._frontSurface = Surface(length = self._side / 2.0,
                                     width = self._side / 2.0,
                                     center = [self._xPos,
                                               self._yPos,
                                               self._zPos + self._side / 2.0],
                                     normal = Vector('e_z'),
                                     color = [0.0, 1.0, 0.0, 0.5])
        self._backSurface = Surface(length = self._side / 2.0,
                                     width = self._side / 2.0,
                                     center = [self._xPos,
                                               self._yPos,
                                               self._zPos - self._side / 2.0],
                                     normal = Vector('e_z').v_mult(-1.0),
                                     color = [0.0, 1.0, 0.0, 0.5])

        self._surfaces = [self._rightSurface,
                          self._leftSurface,
                          self._upSurface,
                          self._downSurface,
                          self._frontSurface,
                          self._backSurface]

    def update_surfaces(self):
        ''' Updates the cubes surfaces so that they align with the cube. '''
        for surface in self._surfaces:
            surface.set_center(Vector(self.get_center())\
                               .v_add(surface.get_normal()\
                                      .v_mult(self._side / 2.0)).get_value())
            surface.update_points()
            surface.update()

    def update(self, surfaceList):
        ''' Checks for collision, moves and draws the cube. '''
        self.update_surfaces()
        super(Cube, self).update(surfaceList)

        # Defines the edges of the cube for better collision
##        self.update_edges()
##        
##    def update(self, cubelist):
##        # TODO: func doc
##        # NOTE: the order makes the cubes push one another in
##        # opposite directions, fix with surfaces, maybe
##        # an instance variable "beingPushed" that prevents
##        # the particular surface from pushing back
##        # OR make the cube with the highest velocity dominate the others =)
##        super(Cube, self).update()
##        self.update_edges()
##        for cube in cubelist:
##            if cube != self:
##                self.check_collision(cube)
##
##    def update_edges(self):
##        ''' Updates the edges of the cube '''
##        self._xyEdge1 = Vector([self._xPos + self._side/2, self._yPos + self._side/2, self._zPos])
##        self._xyEdge2 = Vector([self._xPos + self._side/2, self._yPos - self._side/2, self._zPos])
##        self._xyEdge3 = Vector([self._xPos - self._side/2, self._yPos + self._side/2, self._zPos])
##        self._xyEdge4 = Vector([self._xPos - self._side/2, self._yPos - self._side/2, self._zPos])
##        
##        self._xzEdge1 = Vector([self._xPos + self._side/2, self._yPos, self._zPos + self._side/2])
##        self._xzEdge2 = Vector([self._xPos + self._side/2, self._yPos, self._zPos - self._side/2])
##        self._xzEdge3 = Vector([self._xPos - self._side/2, self._yPos, self._zPos + self._side/2])
##        self._xzEdge4 = Vector([self._xPos - self._side/2, self._yPos, self._zPos - self._side/2])
##        
##        self._yzEdge1 = Vector([self._xPos, self._yPos + self._side/2, self._zPos + self._side/2])
##        self._yzEdge2 = Vector([self._xPos, self._yPos - self._side/2, self._zPos + self._side/2])
##        self._yzEdge3 = Vector([self._xPos, self._yPos + self._side/2, self._zPos - self._side/2])
##        self._yzEdge4 = Vector([self._xPos, self._yPos - self._side/2, self._zPos - self._side/2])

    def draw_shape(self):
        ''' The drawing routine for Cube. '''
        glColor4fv(self._color)
        glutSolidCube(self._side)

##    def push(self, cube2, side):
##        ''' Makes the sphere push the cube on the side of the cube defined by the
##        normal vector side '''
##        cube2.move(side.v_mult(-1.0).get_value())

##    def collide_cube(self, cube2):
##        ''' Checks if the cube has collided with another cube.
##        If there was a collision, return the normal of the side that
##        the sphere collided with, else return False.
##        (Very specific, might need to get more general) '''
##
##        distance = self.get_distance_shape(cube2)
##
##        normals = cube2.get_normals()
##        sideLength = cube2.get_side_length()
##
##        for i in range(3):
##            if abs(distance.dot(normals[2*i])) < sideLength / 2 + self._side / 2 \
##               and abs(distance.dot(normals[2*(i+1)%len(normals)])) < sideLength / 2 + self._side / 2 \
##               and abs(distance.dot(normals[2*(i+2)%len(normals)])) \
##               <= sideLength / 2 + self._side / 2:
##                # TODO: A little ugly, but seems to work OK, maybe change later.
##                if abs(self._velocity.cross(normals[2*(i+2)%len(normals)]).norm()) < 0.0001:
##                    # NOTE: Should be "...norm() == 0:", but I take rounding errors into account
##                    if distance.dot(normals[2*(i+2)%len(normals)]) < 0:
##                        return normals[2*(i+2)%len(normals)]
##                    else:
##                        return normals[(2*(i+2)+1)%len(normals)]

    # Getters and setters

    def get_side_length(self):
        ''' Returns the side length of the cube '''
        return self._side

    def get_border_distance(self):
        return self._side / 2.0

    def get_surfaces(self):
        return self._surfaces

##    def get_normals(self):
##        ''' Returns the normals of the cube's sides '''
##        return [self._rightNormal, self._leftNormal,
##                         self._upNormal, self._downNormal,
##                         self._frontNormal, self._backNormal]
##        
##    def get_edges(self):
##        ''' Returns the edges of the cube '''
##        return [self._yzEdge1, self._yzEdge2, self._yzEdge3, self._yzEdge4,
##                self._xzEdge1, self._xzEdge2, self._xzEdge3, self._xzEdge4,
##                self._xyEdge1, self._xyEdge2, self._xyEdge3, self._xyEdge4]
##
