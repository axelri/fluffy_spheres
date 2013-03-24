# Shape class for the GJK test

from vector import *

class Shape:

    def __init__(self, points, position, support_func, color, mass = 1):

        # Linear motion
        self._pos = position
        self._velocity = Vector()
        self._acceleration = Vector()
        self._mass = mass
        self._force = Vector()

        # Angular motion
        self._orientation = None
        self._angVelocity = None
        self._angAcceleration = None
        self._invInertia = None
        self._torque = None


        self._points = points
        self.sup_func = support_func
        self._radius = 1.0 # Just used to test support func for spheres
        self._color = color
        
    def support_func(self, direction):
        return self.sup_func(self, direction)

    def get_velocity(self):
        return self._velocity

    def set_velocity(self, velocity):
        self._velocity = velocity

    def add_velocity(self, velocity):
        self._velocity += velocity

    def get_mass(self):
        return self._mass

    def get_pos(self):
        return self._pos

    def get_points(self):
        return self._points

    def get_radius(self):
        return self._radius

    def set_pos(self, pos):
        self._pos = pos

    def set_points(self, points):
        self._points = points

    def update_pos(self, movement):
        self._pos += movement

    def update_points(self, movement):
        outPoints = [0]*len(self._points)
        for i in range(len(self._points)):
            out = self._points[i] + movement
            outPoints[i] = out
        self._points = outPoints

    def set_color(self, color):
        self._color = color

    def get_color(self):
        return self._color
