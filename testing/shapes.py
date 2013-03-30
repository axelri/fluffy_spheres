import vectors
import quaternions
import supports
import numbers
import draw

class Shape(object):

    def __init__(self):

        # Linear motion
        self._pos = vectors.Vector()
        self._velocity = vectors.Vector()
        self._mass = float('inf')      # Makes it "immobile"
        self._force = vectors.Vector()

        # Angular motion
        self._orientation = quaternions.Quaternion()
        self._angularVelocity = vectors.Vector()
        self._invInertia = [[0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0]]   # Makes it unable to rotate
        self._torque = vectors.Vector()

        self._color = None

    def get_velocity(self):
        return self._velocity

    def set_velocity(self, velocity):
        assert isinstance(velocity, vectors.Vector), 'Velocity must be a vector'
        self._velocity = velocity

    def add_velocity(self, velocity):
        assert isinstance(velocity, vectors.Vector), 'Velocity must be a vector'
        self._velocity += velocity

    def get_angular_velocity(self):
        return self._angularVelocity

    def set_angular_velocity(self, velocity):
        assert isinstance(velocity, vectors.Vector), 'Velocity must be a vector'
        self._angularVelocity = velocity

    def add_angular_velocity(self, velocity):
        assert isinstance(velocity, vectors.Vector), 'Velocity must be a vector'
        self._angularVelocity += velocity

    def get_mass(self):
        return self._mass

    def set_mass(self, mass):
        assert isinstance(mass, numbers.Number), 'Mass must be a number'
        assert mass >= 0, 'Mass must be at least 0'
        self._mass = mass

    def get_invInertia(self):
        return self._invInertia

    def get_pos(self):
        return self._pos

    def set_pos(self, pos):
        assert isinstance(pos, vectors.Vector), 'Pos must be a vector'
        self._pos = pos

    def add_pos(self, pos):
        assert isinstance(pos, vectors.Vector), 'Pos must be a vector'
        self._pos += pos

    def get_color(self):
        return self._color

    def set_color(self, color):
        assert isinstance(color, list), 'Color must be a list'
        # NOTE: If we use alpha values this should be 4
        assert len(color) == 3, 'Color must be of length 3' 
        if __debug__:
            for item in color:
                assert isinstance(item, numbers.Number), \
                       'Every component of color must be a number'
                assert 0 <= item <= 1, \
                       'Every component of color must be a number between 0 and 1'
        self._color = color

class Sphere(Shape):

    def __init__(self, pos = vectors.Vector(), radius = 0.5,
                 mass = 1.0, color = [1.0, 0.5, 0.3]):
        super(Sphere, self).__init__()
        assert isinstance(pos, vectors.Vector), 'Pos must be a vector'
        assert isinstance(mass, numbers.Number), 'Mass must be a number'
        assert mass >= 0, 'Mass must be at least 0'
        assert isinstance(radius, numbers.Number), 'Radius must be a number'
        assert radius >= 0, 'Radius must be at least 0'
        assert isinstance(color, list), 'Color must be a list'
        # NOTE: If we use alpha values this should be 4
        assert len(color) == 3, 'Color must be of length 3'
        if __debug__:
            for item in color:
                assert isinstance(item, numbers.Number), \
                       'Every component of color must be a number'
                assert 0 <= item <= 1, \
                       'Every component of color must be a number between 0 and 1'
                
        self._pos = pos
        self._mass = mass
        self._radius = radius
        self._color = color
        I = 5/(2*self._mass*self._radius*self._radius)
        self._invInertia = [[I, 0.0, 0.0],
                            [0.0, I, 0.0],
                            [0.0, 0.0, I]]
        #self._orientation = quaternions.axis_angle_to_quat(Vector([1.0, 0.0, 0.0]), 0.0)
        #self._orientation = quaternions.Quaternion([1.0, 0.0, 0.0, 0.0]) #This is equivalent, maybe better?

    def support_func(self, direction):
        return supports.sphere(self, direction)

    def get_normal(self, point):
        ''' Returns the normal of the sphere in the given point '''
        assert isinstance(point, vectors.Vector), 'Input must be a vector'
        return (point - self._pos).normalize()

    def get_radius(self):
        return self._radius

    def draw(self):
        draw.sphere(self)
        
        
        
class Cube(Shape):

    def __init__(self, pos = vectors.Vector(), side = 1,
                 mass = 1, color = [0.8, 0.8, 0.8]):
        super(Cube, self).__init__()
        assert isinstance(pos, vectors.Vector), 'Pos must be a vector'
        assert isinstance(mass, numbers.Number), 'Mass must be a number'
        assert mass >= 0, 'Mass must be at least 0'
        assert isinstance(side, numbers.Number), 'Side must be a number'
        assert side > 0, 'Side must be greater than 0'
        assert isinstance(color, list), 'Color must be a list'
        # NOTE: If we use alpha values this should be 4
        assert len(color) == 3, 'Color must be of length 3'
        if __debug__:
            for item in color:
                assert isinstance(item, numbers.Number), \
                       'Every component of color must be a number'
                assert 0 <= item <= 1, \
                       'Every component of color must be a number between 0 and 1'

        self._pos = pos
        self._side = side
        self._mass = mass
        self._color = color

    def support_func(self, direction):
        #return supports.cube(self, direction)
        return supports.polyhedron(self, direction)

    def get_side(self):
        return self._side

    def get_points(self):
        h = self._side/2.0
        return [vectors.Vector([h, -h, -h]),  vectors.Vector([h, h, -h]),
                vectors.Vector([-h, h, -h]),  vectors.Vector([-h, -h, -h]),
                vectors.Vector([h, -h, h]),   vectors.Vector([h, h, h]),
                vectors.Vector([-h, -h, h]),  vectors.Vector([-h, h, h])]

    def get_normal(self, point):
        ''' Returns the normal of the cube in th given point. Assumes the point
            lies inside of the cube. '''
        assert isinstance(point, vectors.Vector), 'Input must be a vector'

        dist = point - self._pos
        halfside = self._side/2.0

        xdot = dist.dot(vectors.Vector([1.0, 0.0, 0.0]))
        ydot = dist.dot(vectors.Vector([0.0, 1.0, 0.0]))
        zdot = dist.dot(vectors.Vector([0.0, 0.0, 1.0]))

        xdist = halfside - abs(xdot)
        ydist = halfside - abs(ydot)
        zdist = halfside - abs(zdot)

        distlist = [xdist, ydist, zdist]

        # Calculates which pair of faces is closest to the point
        index = distlist.index(min(distlist))

        if index == 0:
            if xdot > 0:
                return vectors.Vector([1.0, 0.0, 0.0])
            else:
                return vectors.Vector([-1.0, 0.0, 0.0])
        elif index == 1:
            if ydot > 0:
                return vectors.Vector([0.0, 1.0, 0.0])
            else:
                return vectors.Vector([0.0, -1.0, 0.0])
        else:
            if zdot > 0:
                return vectors.Vector([0.0, 0.0, 1.0])
            else:
                return vectors.Vector([0.0, 0.0, -1.0])

    def draw(self):
        draw.cube(self)


class Surface(Shape):

    def __init__(self, pos = vectors.Vector(),
                 points = [vectors.Vector([-5.0, 0.0, -5.0]), vectors.Vector([5.0, 0.0, -5.0]),
                           vectors.Vector([5.0, 0.0, 5.0]), vectors.Vector([-5.0, 0.0, 5.0])],
                 color = [1.0, 0.0, 1.0]):
        super(Surface, self).__init__()
        assert isinstance(pos, vectors.Vector), 'Pos must be a vector'
        assert isinstance(color, list), 'Color must be a list'
        # NOTE: If we use alpha values this should be 4
        assert len(color) == 3, 'Color must be of length 3'
        if __debug__:
            for item in color:
                assert isinstance(item, numbers.Number), \
                       'Every component of color must be a number'
                assert 0 <= item <= 1, \
                       'Every component of color must be a number between 0 and 1'
        assert isinstance(points, list), 'Points must be a list'
        assert len(points) == 4, 'Points must be of length 4'
        if __debug__:
            for point in points:
                assert isinstance(point, vectors.Vector), \
                       'Every component of points must be a vector'

        self._pos = pos
        self._points = points
        self._color = color
        self._normal = (points[0] - points[1]).cross(points[3] - points[1]).normalize()

    def support_func(self, direction):
        return supports.polyhedron(self, direction)

    def get_points(self):
        return self._points

    def get_normal(self, point):
        return self._normal

    def draw(self):
        draw.plane(self)
