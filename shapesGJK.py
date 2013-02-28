# Shape class for the GJK test

from vector import *

class Shape:

    def __init__(self, points, position):
        self._pos = position
        self._points = points
        #self._boundaryRadius = 0.5**(2.0/3.0)   # Only applies to cubes with
                                                # side 1.0, should be defined for each shape.

    def get_pos(self):
        return self._pos

    def get_points(self):
        return self._points

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

    #def get_boundary(self):
        #return self._boundaryRadius
