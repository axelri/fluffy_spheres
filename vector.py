from math import *
class Vector:
    """ A vector class to simplify calculations on vectors """
    
    def __init__(self, value):
        self._value = value      # A list of the values of the vector

    def get_Value(self):
        return self._value

    def set_Value(self, value):
        self._value = value
    
    def dot(self, v2):
        """ Calculates the dot product of the vector and v2 """
        tot = 0
        for i in range(len(self._value)):
            tot += self._value[i] * v2._value[i]
        return tot

    def cross(self, V2):
        """ Calculates the cross product of the vector and another vector V2.
            Note that it is calculated as (self x V2), since the cross product
            isn't commutative """
        v1 = self._value
        v2 = V2._value
        out = [v1[1] * v2[2] - v1[2] * v2[1],
               v1[2] * v2[0] - v1[0] * v2[2],
               v1[0] * v2[1] - v1[1] * v2[0]]
        return Vector(out)

    def norm(self):
        """ Calculates the norm of the vector """
        return (self.dot(self))**0.5

    def normalize(self):
        """ Normalizes the vector """
        n = self.norm()
        v = self._value
        if n != 0:
            for i in range(len(v)):
                v[i] /= n
        else:
            return None
        return Vector(v)

    def v_mult(self, scalar):
        """ Multiplies the vector with the scalar """
        out = [0]*len(self._value)
        for i in range(len(self._value)):
            out[i] = self._value[i] * scalar
        return Vector(out)

    def v_add(self, v2):
        """ Adds the vector to v2 """
        out = [0]*len(self._value)
        for i in range(len(self._value)):
            out[i] = self._value[i] + v2._value[i]
        return Vector(out)

    def proj_norm(self, v2):
        """ Returns the norm of the projection of the vector on the vector v2 """
        if v2.norm() != 0:
            e2 = v2.normalize()
            return self.dot(e2)
        else:
            return 0

    def projection(self, v2):
        """ Returns the projection of the vector on the vector v2 """
        n = self.proj_norm(v2)
        e2 = v2.normalize()
        if e2 != None:
            out = e2.v_mult(n)
            return out
        else:
            return Vector([0]*len(self._value)) # A zero vector

    def proj_syst(self, e1, e2, e3):
        """ Returns the projection of the vector in the coordinate system
            defined by the vectors e1, e2 and e3 """
        proj1 = self.projection(e1)
        proj2 = self.projection(e2)
        proj3 = self.projection(e3)
        out = proj1.v_add(proj2.v_add(proj3)) # Adds all vectors
        
        return out
