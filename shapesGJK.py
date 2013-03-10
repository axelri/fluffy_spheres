# Shape class for the GJK test

from vector import *

class Shape:

    def __init__(self, points, position, support_func):
        self._pos = position
        self._points = points
        self.sup_func = support_func
        self._radius = 1.0 # Just used to test support func for spheres
        self._mass = 1
        
    def support_func(self, direction):
        return self.sup_func(self, direction)

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
