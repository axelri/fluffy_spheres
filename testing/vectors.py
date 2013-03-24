from math import *
import numbers

class Vector:
    ''' A vector class to simplify calculations on vectors '''
    
    def __init__(self, value = [0.0, 0.0, 0.0]):
        assert isinstance(value, list), \
                'Input must be a list'

        if __debug__:
            for number in value:
                assert isinstance(number, numbers.Number), \
                    'Every component must be a number.'

        self.value = value

    def dim(self):
        return len(self.value)

    def is_zero(self):
        return self.value == [0] * self.dim()

    def is_not_zero(self):
        return self.value != [0] * self.dim()

    def dot(self, v2):
        ''' Calculates the dot product of the vector and v2 '''
        assert isinstance(v2, Vector), 'Input must be a vector'
        assert self.dim() ==  v2.dim(), \
                'Vectors must be of the same dimension'

        tot = 0
        for i in range(len(self.value)):
            tot += self.value[i] * v2.value[i]
        return tot

    def cross(self, v):
        ''' Calculates the cross product of the vector and another vector V2.
            Note that it is calculated as (self x V2), since the cross product
            isn't commutative '''
        assert isinstance(v, Vector), 'Input must be a vector'
        assert self.dim() == 3 and v.dim() == 3, \
                'Cross product is only defined in 3 dimensions.'

        v1 = self.value
        v2 = v.value
        return Vector([v1[1] * v2[2] - v1[2] * v2[1],
                       v1[2] * v2[0] - v1[0] * v2[2],
                       v1[0] * v2[1] - v1[1] * v2[0]])

    def norm(self):
        ''' Calculates the norm of the vector '''
        return sqrt((self.dot(self)))

    def normalize(self):
        ''' Returns a normaliszed version of the the vector. 
        Returns None if the vector is the zero vector.'''
        if self.is_zero():
            return None

        n = self.norm()
        out = []
        for component in self.value:
            out.append(component / n)
        return Vector(out)

    def __eq__(self, v2):
        ''' Checks if two vectors have the same value, overloads "==" '''
        assert isinstance(v2, Vector), 'Input must be a vector'
        return self.value == v2.value

    def __ne__(self, v2):
        ''' Checks if two vectors do not have the same value, overloads "!=" '''
        assert isinstance(v2, Vector), 'Input must be a vector'
        return self.value != v2.value

    def __mul__(self, scalar):
        ''' Returns the vector multiplied with the given scalar '''
        assert isinstance(scalar, numbers.Number), \
            'Input must be a real number.' 

        out = []
        for component in self.value:
            out.append(component * scalar)
        return Vector(out)

    def __neg__(self):
        '''Returns the vector in negative direction.'''
        return self * -1

    def __add__(self, v2):
        ''' Returns the vector added with the given other vector.'''
        assert isinstance(v2, Vector), 'Input must be a vector.'
        assert self.dim() == v2.dim(), \
                'Vectors must be of the same dimension'

        out = []
        for comp1, comp2 in zip(self.value, v2.value):
            out.append(comp1 + comp2)
        return Vector(out)

    def __sub__(self, v2):
        assert isinstance(v2, Vector), 'Input must be a vector.'
        assert self.dim() == v2.dim(), \
                'Vectors must be of the same dimension'

        return self + (-v2)

    def projected(self, *base):
        ''' Returns the projection of the vector on the vector space 
        defined by the supplied vectors. Assumes orthogonal and linearly
        independant base vectors.'''
        if __debug__:
            for v in base:
                assert isinstance(v, Vector), 'Input must be a vector.'
                assert self.dim() == v.dim(), 'Vectors must be of the same dimension'
                assert v.is_not_zero, "Input can't be the the zero vector"

        proj = Vector([0] * self.dim())
        for v in base:
            base_proj = v * (float(self.dot(v))/float(v.dot(v)))
            proj += base_proj

        return proj
    
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

    def __str__(self):
        ''' Returns the string representation of the vector.'''
        return self.value.__str__()
