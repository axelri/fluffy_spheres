from math import *
# NOTE: Probably easier with numPy instead of defining own functions

def generate_rotation_matrix(vector, angle):
    ''' Generates a rotation matrix according to OpenGL standards
        with a rotation of angle (in radians) and
        the vector as rotation axis '''
    v = vector.normalize()

    if v == None:
        v = [0, 0, 0] #Dummy variable, will return identity matrix whatever we put here
    else:
        v = v._value
    
    rotation_matrix = [v[0] * v[0] * (1.0 - cos(angle)) + cos(angle),
                       v[1] * v[0] * (1.0 - cos(angle)) + v[2] * sin(angle),
                       v[0] * v[2] * (1.0 - cos(angle)) - v[1] * sin(angle),
                       0.0,
                       v[0] * v[1] * (1.0 - cos(angle)) - v[2] * sin(angle),
                       v[1] * v[1] * (1.0 - cos(angle)) + cos(angle),
                       v[1] * v[2] * (1.0 - cos(angle)) + v[0] * sin(angle),
                       0.0,
                       v[0] * v[2] * (1.0 - cos(angle)) + v[1] * sin(angle),
                       v[1] * v[2] * (1.0 - cos(angle)) - v[0] * sin(angle),
                       v[2] * v[2] * (1.0 - cos(angle)) + cos(angle),
                       0.0,
                       0.0,
                       0.0,
                       0.0,
                       1.0]
    return rotation_matrix

def matrix_mult(a, b):
    ''' Multiplies the matrices a and b as (a * b).
        The matrices are given in OpenGL standard, that is,
        a 4x4 matrix written in column-major order, represented
        as a list. '''
    out = [0]*16  
    for i in range(4):
        for k in range(4):
            out[4*i + k] = a[k]*b[4*i] + a[k+4]*b[4*i+1] + a[k+8]*b[4*i+2] + a[k+12]*b[4*i+3]
    return out
            
def identity():
    ''' Returns an identity matrix in OpenGL standard. '''
    return [1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0]
