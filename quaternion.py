from vector import *

class Quaternion(Vector):
    ''' A quaternion class for rotation handling, inherits from Vector.
        the values are named [w, x, y, z]'''

    def __init__(self, value):
        assert isinstance(value, list), 'Input must be a list'
        assert len(value) == 4, 'The quaternion must be of length 4'
        super(Quaternion, self).__init__(value)


    def convert_to_matrix(self):
        ''' Converts the quaternion to a rotation matrix of OpenGL standard. '''

        xx = self._value[1]*self._value[1]
        xy = self._value[1]*self._value[2]
        xz = self._value[1]*self._value[3]
        xw = self._value[1]*self._value[0]

        yy = self._value[2]*self._value[2]
        yz = self._value[2]*self._value[3]
        yw = self._value[2]*self._value[0]

        zz = self._value[3]*self._value[3]
        zw = self._value[3]*self._value[0]

        matrix = [1 - 2*yy - 2*zz, 2*xy + 2*zw, 2*xz - 2*yw, 0,
                  2*xy - 2*zw, 1 - 2*xx - 2*zz, 2*yz - 2*xw, 0,
                  2*xz + 2*yw, 2*yz - 2*xw, 1 - 2*xx - 2*yy, 0,
                  0, 0, 0, 1]

        return matrix

    def q_mult(self, quaternion):
        ''' Multiplies self with the given quaternion '''
        quat1 = self._value
        quat2 = quaternion._value

        v0 = Vector(quat1[1:])
        v1 = Vector(quat2[1:])

        w = quat1[0]*quat2[0] - v0.dot(v1)

        v = v1*quat1[0] + v0*quat2[0] + v0.cross(v1)

        out = [w]+v
        return Quaternion(out)

        
