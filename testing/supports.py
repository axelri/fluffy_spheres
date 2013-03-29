import vectors

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

def polyhedron(shape, direction):
    ''' Support function for convex polyhedra '''
    # TODO: Edit to take orientation into account?
    pointList = []
    shapePoints = shape.get_points()
    for point in shapePoints:
        pointList.append(point.dot(direction))
    outPoint = shapePoints[pointList.index(max(pointList))]
    outPoint += shape.get_pos()
    return outPoint

def sphere(sphere, direction):
    ''' Support function for spheres '''
    return sphere.get_pos() + direction.normalize()*sphere.get_radius()

def cube(cube, direction):
    ''' Support function for axis-aligned cubes '''
    side = cube.get_side()
    out = cube.get_pos()

    if direction.dot(vectors.Vector([1.0, 0.0, 0.0])) < 0:
        out += vectors.Vector([side*0.5, 0.0, 0.0])
    else:
        out += vectors.Vector([side*-0.5, 0.0, 0.0])
    if direction.dot(vectors.Vector([0.0, 1.0, 0.0])) < 0:
        out += vectors.Vector([0.0, side*0.5, 0.0])
    else:
        out += vectors.Vector([0.0, side*-0.5, 0.0])
    if direction.dot(vectors.Vector([0.0, 0.0, 1.0])) < 0:
        out += vectors.Vector([0.0, 0.0, side*0.5])
    else:
        out += vectors.Vector([0.0, 0.0, side*-0.5])

    print 'Support point:', out.value
    return out
