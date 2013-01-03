from math import *

class GameSpace(object):
    ''' A class modeling the current 3D space, and all objects in it.
    Makes sure that all the operations are legal ones.'''

    def __init__(self, objectList):
        self._objectList = objectList

    def is_valid_move(self, shape, directions):
        ''' Checks for collision using a very crude approximation.
        Can be fine-tuned later on.'''
        shapePos = shape.try_move(directions)
        for obj in self._objectList:
            if(shape != obj):
                objPos = obj.get_position()
                distance = self.calc_distance(shapePos, objPos)
                if distance < shape.get_border_distance() + \
                        obj.get_border_distance():
                    return False

        return True

    # NOTE: should probably be class method instead
    def calc_distance(self, pos1, pos2):
        ''' Calculates the distance between to coordinates in 3D space.'''
        
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        dz = pos1[2] - pos2[2]

        return sqrt(dx**2 + dy**2 + dz**2)
