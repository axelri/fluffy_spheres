from math import *
class Vector:
    ''' A vector class to simplify calculations on vectors '''
    
    def __init__(self, value = [0.0, 0.0, 0.0]):
        # Shorter calls for vectors we use a lot
        if value == 'e_x':
            self._value = [1.0, 0.0, 0.0]
        elif value == 'e_y':
            self._value = [0.0, 1.0, 0.0]
        elif value == 'e_z':
            self._value = [0.0, 0.0, 1.0]
        else:
            self._value = value

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def isZero(self):
        return self._value == [0.0, 0.0, 0.0]
    
    def dot(self, v2):
        ''' Calculates the dot product of the vector and v2 '''
        tot = 0
        for i in range(len(self._value)):
            tot += self._value[i] * v2._value[i]
        return tot

    def cross(self, V2):
        ''' Calculates the cross product of the vector and another vector V2.
            Note that it is calculated as (self x V2), since the cross product
            isn't commutative '''
        v1 = self._value
        v2 = V2._value
        out = [v1[1] * v2[2] - v1[2] * v2[1],
               v1[2] * v2[0] - v1[0] * v2[2],
               v1[0] * v2[1] - v1[1] * v2[0]]
        return Vector(out)

    def norm(self):
        ''' Calculates the norm of the vector '''
        return (self.dot(self))**0.5

    def normalize(self):
        ''' Normalizes the vector '''
        n = self.norm()
        v = self._value
        if n != 0:
            for i in range(len(v)):
                v[i] /= n
        else:
            return None
        return Vector(v)

    def __add__(self, v2):
        ''' Adds the vector to v2, overloads the "+"-operator.'''
        out = [0]*len(self._value)
        for i in range(len(self._value)):
            out[i] = self._value[i] + v2._value[i]
        return Vector(out)

    def __mul__(self, scalar):
        ''' Multiplies the vector with the scalar.
            Overloads the "*"-operator. '''
        out = [0]*len(self._value)
        for i in range(len(self._value)):
            out[i] = self._value[i] * scalar
        return Vector(out)

    def __sub__(self, v2):
        ''' Subtracts v2 from the vector, overloads the "-"-operator. '''
        return self.__add__(v2.__mul__(-1.0))

    def __neg__(self):
        ''' Negates the vector, overloads "-self" '''
        return self.__mul__(-1.0)

    def __eq__(self, vector):
        ''' Checks if two vectors have the same value, overloads "==" '''
        return self._value == vector._value

    def __ne__(self, vector):
        ''' Checks if two vectors do not have the same value, overloads "!=" '''
        return self._value != vector._value

    def proj_norm(self, v2):
        ''' Returns the norm of the projection of the vector 
            on the vector v2 '''
        if v2.norm() != 0:
            e2 = v2.normalize()
            return self.dot(e2)
        else:
            return 0

    def projection(self, v2):
        ''' Returns the projection of the vector on the vector v2 '''
        n = self.proj_norm(v2)
        e2 = v2.normalize()
        if e2 != None:
            out = e2 * n
            return out
        else:
            return Vector([0]*len(self._value)) # A zero vector

    def proj_syst(self, e1, e2, e3):
        ''' Returns the projection of the vector in the coordinate system
            defined by the vectors e1, e2 and e3 (e1, e2 and e3 must be
            orthogonal'''
        proj1 = self.projection(e1)
        proj2 = self.projection(e2)
        proj3 = self.projection(e3)
        out = proj1 + proj2 + proj3
        
        return out

    def proj_plane(self, e1, e2):
        ''' Returns the projection of the vector on the plane defined
            by the vectors e1 and e2 (e1 and e2 must be orthogonal) '''
        proj1 = self.projection(e1)
        proj2 = self.projection(e2)
        out = proj1 + proj2

        return out

    def distance_vector(self, point):
        ''' Returns a vector from self to point '''
        # Rather unnessecary, why not just use point - self?
        p = point.get_value()
        s = self._value
        return Vector([p[0] - s[0],
                       p[1] - s[1],
                       p[2] - s[2]])
    
    def triple_product_1(self, v2, v3):
        ''' Calculates the triple product self x (v2 x v3)
            in a faster and simpler way.'''

        term1 = v2 * self.dot(v3)
        term2 = v3 * -self.dot(v2)
        out = term1 + term2
        return out

    def triple_product_2(self, v2, v3):
        ''' Calculates the triple product (self x v2) x v3
            in a faster and simpler way.'''

        term1 = self * -v2.dot(v3)
        term2 = v2 * self.dot(v3)
        out = term1 + term2
        return out
