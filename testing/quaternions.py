import vectors
import numbers
from math import cos, sin

class Quaternion:
    ''' A quaternion class for rotation handling.
        The values are named [w, x, y, z] or [w, v], where v is [x, y, z]. '''
    def __init__(self, value = [1.0, 0.0, 0.0, 0.0]):
        assert isinstance(value, list), 'Input must be a list'
        assert len(value) == 4, 'The quaternion must be of length 4'
        if __debug__:
            for number in value:
                assert isinstance(number, numbers.Number), \
                    'Every component must be a number.'
        
        self.value = value

    def norm(self):
        v = self.value
        return sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2] + v[3]*v[3])

    def normalize(self):
        out = [0]*4
        n = norm(self)
        for i in range(len(self.value)):
            out[i] = self.value[i]/n

        return out

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
        assert isinstance(quaternion, Quaternion)
        quat1 = self.value
        quat2 = quaternion.value

        v0 = vectors.Vector(quat1[1:])
        v1 = vectors.Vector(quat2[1:])

        w = quat1[0]*quat2[0] - v0.dot(v1)

        v = v1*quat1[0] + v0*quat2[0] + v0.cross(v1)

        out = [w]+v.value
        return Quaternion(out)

    def conjugate(self):
        value = self.value
        w = value[0]
        x = value[1]
        y = value[2]
        z = value[3]
        return Quaternion([w, -x, -y, -z])


def matrix_to_quat(m):
    ''' Converts a rotational matrix to a quaternion. Assumes the
        matrix describes a rotation only, and therefore is special orthogonal. '''
    tr = m[0][0] + m[1][1] + m[2][2]

    if tr > 0:
        S = sqrt(tr + 1.0) * 2
        qw = 0.25 * S
        qx = (m[2][1] - m[1][2]) / S
        qy = (m[0][2] - m[2][0]) / S
        qz = (m[1][0] - m[0][1]) / S
    elif m[0][0] > m[1][1] and m[0][0] > m[2][2]:
        S = sqrt(1.0 + m[0][0] - m[1][1] - m[2][2]) * 2
        qw = (m[2][1] - m[1][2]) / S
        qx = 0.25 * S
        qy = (m[0][1] + m[1][0]) / S
        qz = (m[0][2] + m[2][0]) / S
    elif m[1][1] > m[2][2]:
        S = sqrt(1.0 + m[1][1] - m[0][0] - m[2][2]) * 2
        qw = (m[0][2] - m[2][0]) / S
        qx = (m[0][1] + m[1][0]) / S
        qy = 0.25 * S
        qz = (m[1][2] + m[2][1]) / S
    else:
        S = sqrt(1.0 + m[2][2] - m[0][0] - m[1][1]) * 2
        qw = (m[1][0] - m[0][1]) / S
        qx = (m[0][2] + m[2][0]) / S
        qy = (m[1][2] + m[2][1]) / S
        qz = 0.25 * S

    return Quaternion([qw, qx, qy, qz])

def axis_angle_to_quat(axis, angle):
    ''' Converts an axis and an angle to a quaternion. '''
    
    assert isinstance(axis, vectors.Vector), 'The rotation axis must be a vector'
    assert axis.is_zero() == False, "The rotation axis can't be the zero vector"
    assert axis.dim() == 3, 'The rotation axis must be a vector of length 3'
    assert isinstance(angle, numbers.Number), 'Angle must be a number'
    axis = axis.normalize().value
    w = cos(angle/2)
    x = axis[0]*sin(angle/2)
    y = axis[1]*sin(angle/2)
    z = axis[2]*sin(angle/2)

    return Quaternion([w, x, y, z])
