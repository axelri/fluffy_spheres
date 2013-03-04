from vector import *

def support(shape1, shape2, direction):
    ''' Calculates a point in Minkowski space that is on the edge of
        the Minkowski Difference of the two shapes.

        Input:
            *   shape1Points and shape2Points are lists of the points in
                shape1 and shape2, represented as Vector objects.
            *   direction is a Vector object indicating in which direction
                to look for a new point (doesn't have to be normalized).
        Output:
            *   outPoint is a point on the edge of the Minkowski Difference
                of the two shapes.
    '''
    
    # Get points on the edge of the shapes in opposite directions
    
    point1 = shape1.support_func(direction)
    point2 = shape2.support_func(-direction)

    # Perform the Minkowski Difference
    outPoint = point1 - point2

    return outPoint, point1, point2

def polyhedron(self, direction):
    ''' Support function for convex polyhedra '''
    pointList = []
    shapePoints = self.get_points()
    for point in shapePoints:
        pointList.append(point.dot(direction))
    outPoint = shapePoints[pointList.index(max(pointList))]
    return outPoint

def sphere(self, direction):
    ''' Support function for spheres '''
    return self.get_pos() + direction.normalize()*self.get_radius()
