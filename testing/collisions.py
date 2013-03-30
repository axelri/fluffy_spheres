import vectors
import simplices
import supports
import gauss
import numbers
import shapes

def GJK(shape1, shape2):
    ''' Calculates whether shape1 has collided with shape2. It uses Minkowski
        Difference to find out if they have any point in common; if they do,
        they have collided.

        Input:
            *   shape1 and shape2 are Shape objects. Shape objects shold have
                a position, describing it's location, and a list of it's points,
                represented as Vector objects, describing the whereabouts of
                it's vertices.
        Output:
            *   The output is a Boolean: True if the shapes have collided and
                False otherwise. It also outputs an approximation of the
                contact point, represented as a Vector object.
    '''
    assert isinstance(shape1, shapes.Shape), 'Input must be a Shape object'
    assert isinstance(shape2, shapes.Shape), 'Input must be a Shape object'
    # Create a Simplex object
    simplex = simplices.Simplex()

    # Choose an initial search direction
    direction = shape1.get_pos() - shape2.get_pos()
    
    # Get the first Minkowski Difference point
    simplex.add(supports.support(shape1, shape2, direction))
    
    direction *= -1.0

    originInSimplex = None
    # Start looping
    while True:
        # Add a new point to the simplex
        # TODO: Take care of if the simplex already contains the point.
        simplex.add(supports.support(shape1, shape2, direction))

        # Make sure that the last point we added passed the origin
        if simplex.get(1).dot(direction) <= 0 and originInSimplex != '':
            # If the point added last was not past the origin in
            # the chosen direction then the Minkowski Difference cannot
            # possibly contain the origin since the last point
            # added is on the edge of the Minkowski Difference.
            return False, (None, None, None)
        else:
            # Otherwise we need to determine if the origin is in
            # the current simplex
            originInSimplex, direction = containsOrigin(simplex)
            if originInSimplex:
                # If it is then we know there is a collision
                assert len(simplex.get_points()) == 4, \
                       'Terminated without full simplex'
                collisionPoint = pointOfCollision_2(simplex)            

                penetrationNormal, penetrationDepth = normal_and_depth(shape1, shape2, collisionPoint)

                
                assert isinstance(collisionPoint, vectors.Vector), \
                       'collisionPoint must be a vector'
                assert isinstance(penetrationNormal, vectors.Vector), \
                       'penetrationNormal must be a vector'
                assert isinstance(penetrationDepth, numbers.Number), \
                       'penetrationDepth must be a number'
                assert penetrationDepth >= 0, 'penetrationDepth must be at least 0'
                return True, (collisionPoint, penetrationNormal, penetrationDepth)




def containsOrigin(simplex):
    ''' Calculates wheter the simplex contains the origin or not.

        Input:
            *   The simplex is a set of two to four points,
                representing a line, triangle or tetrahedron.
        Output:
            *   The output is a tuple of a Boolean and a direction.
                The Boolean represents whether or not the origin is
                found in the simplex, and the direction indicates
                in which direction to search for the origin in the
                next iteration. 
    '''
    assert isinstance(simplex, simplices.Simplex), 'Input must be a Simplex object'
    TOLERANCE = 0.00001     # If the origin is this close to a side
                            # or line in the simplex, we call it a hit

    # Get the last point added to the simplex
    a = simplex.get(1)
    
    # Compute AO (same thing as -A)
    ao = - a

    if len(simplex.get_points()) == 4:
        # It's the tetrahedon case

        # Get b, c and d
        b = simplex.get(2)
        c = simplex.get(3)
        d = simplex.get(4)

        # Compute the edges.
        # We only have to calculate some of them;
        # some can be reused, some are not needed
        ab = b - a
        ac = c - a
        ad = d - a

        # Compute the normals
        # Since we can't be sure the winding of the triangles (?),
        # we do not yet know if these normals point "inwards" or "outwards"
        abcNormal = ab.cross(ac)
        abdNormal = ad.cross(ab)
        acdNormal = ac.cross(ad)

        # Make sure the normals are in the right direction
        abcNormal *= -abcNormal.dot(ad)
        abdNormal *= -abdNormal.dot(ac)
        acdNormal *= -acdNormal.dot(ab)

        # Check where the origin is
        if abcNormal.dot(ao) > 0:
            # The origin is in R1
            # Remove point d
            simplex.remove(4)
            # Set new direction to abcNormal
            direction = abcNormal
        elif abdNormal.dot(ao) > 0:
            # The origin is in R2
            # Remove point c
            simplex.remove(3)
            # Set new direction to abdNormal
            direction = abdNormal
        elif acdNormal.dot(ao) > 0:
            # The origin is in R3
            # Remove point b
            simplex.remove(2)
            # Set new direction to acdNormal
            direction = acdNormal
        else:
            # The origin is in R5, collision is confirmed
            return True, None

    elif len(simplex.get_points()) == 3:
        # Then it's the triangle case
        
        # Get b and c
        b = simplex.get(2)
        c = simplex.get(3)

        # Compute the edges
        ab = b - a
        ac = c - a

        # Get the normal to the surface in the direction of the origin
        normal = ab.cross(ac)
        normal *= normal.dot(ao)
        
        # If the origin lies in the same plane as abc, check if it lies
        # on abc, if so, consider it a hit.
        if normal.norm() < TOLERANCE:
            # Calculate the normals of ab and ac.
            abPerp = ac.triple_product_2(ab, ab)
            acPerp = ab.triple_product_2(ac, ac)

            # Check where the origin is
            if abPerp.dot(ao) > 0:
                # The origin is in R1
                # Remove c
                simplex.remove(3)
                # Set new direction to abPerp
                direction = abPerp
            elif acPerp.dot(ao) > 0:
                # The origin is in R2
                # Remove b
                simplex.remove(2)
                # Set new direction to acPerp
                direction = acPerp
            else:
                # The origin is in R3, collision confirmed
                # The origin is in the simplex, return a normal to
                # be able to build the full tetrahedron and an empty
                # string to force it to continue
                # TODO: Ugly solution, fix?
                return '', ab.cross(ac)
        # Otherwise, set the new direction to normal
        else:
            direction = normal

    else:
        # Then it's the line segment case
        b = simplex.get(2)

        # Compute AB
        ab = b - a

        if ab.dot(ao) < 0:
            simplex.remove(2)
            direction = ao
        else:
            # Get the perp to AB in the direction of the origin
            abPerp = ab.triple_product_2(ao, ab)
            # If the origin lies on the same line as ab,
            # check if it lies on ab, if so, consider it a hit.
            if abPerp.norm() < TOLERANCE:
                # The origin is on the line, collision confirmed

                # The origin is in the simplex, return a normal to
                # be able to build the full tetrahedron and an empty
                # string to force it to continue
                # TODO: Ugly solution, fix?
                if ab.dot(vectors.Vector([1.0, 0.0, 0.0])) - ab.norm() < TOLERANCE:
                    return '', vectors.Vector([0.0, 1.0, 0.0])
                else:
                    return '', vectors.Vector([1.0, 0.0, 0.0])
            
            # Otherwise set the direction to abPerp
            else:
                direction = abPerp
    assert isinstance(direction, vectors.Vector), 'Direction must be a vector'
    return False, direction

def pointOfCollision(simplex):
    ''' Returns the point in the shapes that represents the point of collision.
        This is calculated as the mean value of the points in the shapes that
        are closest to eachother. This is a pretty rough approximation, but
        could be sufficient for our needs. '''
    assert isinstance(simplex, simplices.Simplex), 'Input must be a Simplex'
    assert len(simplex.get_points()) == 4, 'Terminated without full simplex'

    # Get the points
    a = simplex.get(1)
    b = simplex.get(2)
    c = simplex.get(3)
    d = simplex.get(4)

    ao = -a

    # Compute the edges.
    ab = b - a
    cb = b - c
    cd = c - d

    bcdNormal = cb.cross(cd)
    bcdNormal *= bcdNormal.dot(ab)

    if ao.dot(bcdNormal)/ab.dot(bcdNormal) < 0.5:
        # a is closest
        points = simplex.get_all(1)
        #collisionPoint = (points[1]+points[2])*0.5
        
        # NOTE: When dealing with plane-sphere and plane-cube collisions,
        # the interpolation between the two points in the simplices
        # ((points[1]+points[2])*0.5) can give really poor results, why
        # it is better to just use the point that we get from the sphere
        # or cube, respectively. With this solution we must make sure to
        # call GJK with GJK(sphere/cube, plane) and not the other way around.
        # Is there a better solution?
        collisionPoint = points[1]
    else:
        # bcd is closest
        cdPerp = cb.triple_product_2(cd, cd)
        bo = -b

        if abs(bo.dot(cdPerp)/cb.dot(cdPerp)) < 0.5:
            # b is closest
            points = simplex.get_all(2)
            #collisionPoint = (points[1]+points[2])*0.5
            collisionPoint = points[1]
        else:
            # cd is closest
            co = -c
            if co.dot(cd)/cd.dot(cd) < 0.5:
                # c is closest
                points = simplex.get_all(3)
                #collisionPoint = (points[1]+points[2])*0.5
                collisionPoint = points[1]
            else:
                # d is closest
                points = simplex.get_all(4)
                #collisionPoint = (points[1]+points[2])*0.5
                collisionPoint = points[1]
    assert isinstance(collisionPoint, vectors.Vector), 'CollisionPoint must be a vector'
    return collisionPoint

def pointOfCollision_2(simplex):
    ''' Another approach to calculating the collision point, using
        baryocentric coordinates. '''
    assert isinstance(simplex, simplices.Simplex), 'Input must be a Simplex object'
    assert len(simplex.get_points()) == 4, 'Terminated without full simplex'
    #points in the minkowski simplex
    simpPoints = simplex.get_all_points(0)
    #points in the simplex of shape 1
    aPoints = simplex.get_all_points(1)
    #points in the simplex of shape 2
    bPoints = simplex.get_all_points(2)

    # create a matrix 
    matrix = [[1.0]*len(simpPoints)]
    vecs = []
    for vector in simpPoints:
        value = vector.value
        vecs.append(value)
    for i in range(len(vecs[0])):
        outvec = []
        for j in range(len(vecs)):
            outvec.append(vecs[j][i])
        matrix.append(outvec)
            

    barCoord = gauss.solve(matrix, [1.0, 0.0, 0.0, 0.0])
    if barCoord:
        collisionPoint = vectors.Vector()

        for i in range(len(aPoints)):
            collisionPoint += aPoints[i]*barCoord[i]
        assert isinstance(collisionPoint, vectors.Vector), 'CollisionPoint must be a vector'
        return collisionPoint
    else:
        return pointOfCollision(simplex)
    
def normal_and_depth(shape1, shape2, collisionPoint):
    assert isinstance(shape1, shapes.Shape), 'Input must be a shape object'
    assert isinstance(shape2, shapes.Shape), 'Input must be a shape object'
    assert isinstance(collisionPoint, vectors.Vector), 'Input must be a vector'

    name1 = shape1.__class__.__name__
    name2 = shape2.__class__.__name__

    # NOTE: Very specific, and a little redundant, but should be sufficient for our needs
    # The bottom line is that the normals that we get from Surface objects are preferred,
    # number two are the ones from Cube objects and last the ones from Sphere objects.
    # (The ones from the sphere isn't very reliable, I've tested it in the physics engine
    # and got very poor results)

    if name1 == 'Surface':
        penetrationNormal, penetrationDepth = \
                           surface_normal_and_depth(shape1, shape2, collisionPoint)
    elif name2 == 'Surface':
        penetrationNormal, penetrationDepth = \
                           surface_normal_and_depth(shape2, shape1, collisionPoint)

    elif name1 == 'Cube':
        penetrationNormal, penetrationDepth = \
                           cube_normal_and_depth(shape1, shape2, collisionPoint)
    elif name2 == 'Cube':
        penetrationNormal, penetrationDepth = \
                           cube_normal_and_depth(shape2, shape1, collisionPoint)

    elif name1 == 'Sphere':
        penetrationNormal, penetrationDepth = \
                           sphere_normal_and_depth(shape1, shape2, collisionPoint)
    elif name2 == 'Sphere':
        penetrationNormal, penetrationDepth = \
                           sphere_normal_and_depth(shape2, shape1, collisionPoint)

    else:
        raise Exception('Unknown shape used in collision')

    assert isinstance(penetrationNormal, vectors.Vector), \
                   'penetrationNormal must be a vector'
    assert isinstance(penetrationDepth, numbers.Number), \
                   'penetrationDepth must be a number'
    assert penetrationDepth >= 0, 'penetrationDepth must be at least 0'
    return penetrationNormal, penetrationDepth
        
    
def surface_normal_and_depth(shape1, shape2, collisionPoint):
    assert isinstance(shape1, shapes.Surface), 'Shape1 must be a surface object'
    assert isinstance(shape2, shapes.Shape), 'Input must be a shape object'
    assert shape2.__class__.__name__ != 'Surface', \
           'Surfaces can not be checked for collision with other surfaces'
    name1 = shape1.__class__.__name__
    name2 = shape2.__class__.__name__
    
    pos = shape2.get_pos()
    points = shape1.get_points()
    a = points[0]
    b = points[1]
    c = points[2]
    if 0 <= (pos - b).dot(a-b) <= (a-b).dot(a-b) and \
       0 <= (pos - b).dot(c-b) <= (c-b).dot(c-b):
        # The other shape is above the surface
        penetrationNormal = shape1.get_normal(collisionPoint)
        if penetrationNormal.dot(pos) < 0:
            # It's pointing the wrong way
            penetrationNormal *= -1.0
        # TODO: Make generic "get distance to edge"-function for all entities
        
    else:
        # shape2 hit an edge of the surface; the normal doesn't matter
        # so we choosde the one from shape2
        penetrationNormal = shape2.get_normal(collisionPoint)

    # TODO: Make generic "get distance to edge"-function for all entities
    if name2 == 'Cube':
        side = shape2.get_side()
    elif name2 == 'Sphere':
        side = shape2.get_radius()*2.0
    else:                 
        raise Exception('Unknown shape used in collision')
    
    penetrationDepth = side/2.0 - (pos - collisionPoint).projected(penetrationNormal).norm()

    assert isinstance(penetrationNormal, vectors.Vector), \
           'penetrationNormal must be a vector'
    assert isinstance(penetrationDepth, numbers.Number), \
           'penetrationDepth must be a number'
    assert penetrationDepth >= 0, 'penetrationDepth must be at least 0'

    return penetrationNormal, penetrationDepth
            
def cube_normal_and_depth(shape1, shape2, collisionPoint):
    assert isinstance(shape1, shapes.Cube), 'Shape1 must be a cube object'
    assert isinstance(shape2, shapes.Shape), 'Input must be a shape object'

    name1 = shape1.__class__.__name__
    name2 = shape2.__class__.__name__

    dist = shape1.get_pos() - shape2.get_pos()
    halfside = shape1.get_side()/2.0

    xdot = abs(dist.dot(vectors.Vector([1.0, 0.0, 0.0])))
    ydot = abs(dist.dot(vectors.Vector([0.0, 1.0, 0.0])))
    zdot = abs(dist.dot(vectors.Vector([0.0, 0.0, 1.0])))

    if xdot <= halfside and ydot <= halfside or \
       xdot <= halfside and zdot <= halfside or \
       ydot <= halfside and zdot <= halfside:
        # The other shape is in front of one of the faces of the cube
        penetrationNormal = shape1.get_normal(collisionPoint)
        #print 'Normal (on cube side):', penetrationNormal.value

        penetrationDepth = shape1.get_side()/2.0 - \
                           (shape1.get_pos() - collisionPoint).projected(penetrationNormal).norm()
        # Hack to avoid small negative penetration depths due to rounding errors
        if penetrationDepth < 0.0:
            if abs(penetrationDepth) < 0.00001:
                penetrationDepth = 0.0
            else:
                raise Exception('Negative penetration depth')
        #print 'Other info:'
        #print '\tSide/2:', shape1.get_side()/2.0
        #print '\tPosition:', shape1.get_pos().value
        #print '\tCollisionPoint:', collisionPoint.value
        #print '\tPenetrationDepth:', penetrationDepth
    else:
        # The other shape hit an edge of the cube; the normal doesn't matter
        # so we choose the one from shape2
        penetrationNormal = shape2.get_normal(collisionPoint)
        #print 'Normal (on cube edge):', penetrationNormal.value
        
        if name2 == 'Cube':
            side = shape2.get_side()
        elif name2 == 'Sphere':
            side = shape2.get_radius()*2
        else:                 
            raise Exception('Unknown shape used in collision')
        
        penetrationDepth = side/2.0 - (shape2.get_pos() - collisionPoint).projected(penetrationNormal).norm()

        # Hack to avoid small negative penetration depths due to rounding errors
        if penetrationDepth < 0.0:
            if abs(penetrationDepth) < 0.00001:
                penetrationDepth = 0.0
            else:
                raise Exception('Negative penetration depth')

        #print 'Other info:'
        #print '\tSide/2:', side/2.0
        #print '\tPosition:', shape2.get_pos().value
        #print '\tCollisionPoint:', collisionPoint.value
        #print '\tPenetrationDepth:', penetrationDepth

    assert isinstance(penetrationNormal, vectors.Vector), \
           'penetrationNormal must be a vector'
    assert isinstance(penetrationDepth, numbers.Number), \
           'penetrationDepth must be a number'
    assert penetrationDepth >= 0, 'penetrationDepth must be at least 0'

    return penetrationNormal, penetrationDepth
        

def sphere_normal_and_depth(shape1, shape2, collisionPoint):
    assert isinstance(shape1, shapes.Sphere), 'Shape1 must be a sphere object'
    assert isinstance(shape2, shapes.Shape), 'Input must be a shape object'

    penetrationNormal = shape1.get_normal(collisionPoint)
    penetrationDepth = (penetrationNormal*shape1.get_radius() \
                                   - (collisionPoint - shape1.get_pos())).norm()

    assert isinstance(penetrationNormal, vectors.Vector), \
           'penetrationNormal must be a vector'
    assert isinstance(penetrationDepth, numbers.Number), \
           'penetrationDepth must be a number'
    assert penetrationDepth >= 0, 'penetrationDepth must be at least 0'

    return penetrationNormal, penetrationDepth

