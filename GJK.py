# Python implementation of the GJK algorithm in 3D

# TODO: Make a function that plots the Minkowski difference of two shapes;
# this would enable better graphical debugging.


from vector import *
from simplex import *
from support import support
import gauss
import numbers

# Necessary? Only needed for the assert in the beginning...
from shapesGJK import Shape

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
    assert isinstance(shape1, Shape), 'Input must be a Shape object'
    assert isinstance(shape2, Shape), 'Input must be a Shape object'
    # Create a Simplex object
    simplex = Simplex()

    # Choose an initial search direction
    direction = shape1.get_pos() - shape2.get_pos()
    
    # Get the first Minkowski Difference point
    simplex.add(support(shape1, shape2, direction))
    
    direction *= -1.0

    originInSimplex = None
    # Start looping
    while True:
        #print 'New loop'
        # Add a new point to the simplex
        # TODO: Take care of if the simplex already contains the point.
        simplex.add(support(shape1, shape2, direction))

        # Make sure that the last point we added passed the origin
        if simplex.get(1).dot(direction) <= 0 and originInSimplex != '':
            # If the point added last was not past the origin in
            # the chosen direction then the Minkowski Difference cannot
            # possibly contain the origin since the last point
            # added is on the edge of the Minkowski Difference.
            #print 'False in loop'
            #return False, None, None, None
            return False, (None, None, None)
        else:
            # Otherwise we need to determine if the origin is in
            # the current simplex
            originInSimplex, direction = containsOrigin(simplex)
            if originInSimplex:
                # If it is then we know there is a collision
                #print 'True in loop'
                #collisionPoint, point1, point2 = pointOfCollision(simplex)
                #return True, collisionPoint, point1, point2
                assert len(simplex.get_points()) == 4, \
                       'Terminated without full simplex'
                collisionPoint = pointOfCollision_2(simplex)

                ######
                # A very rough approximation of the penetration depth
                # and vector that only applies if shape1 is a sphere...
                # Must be edited to be more accurate (and work for other shapes)
                # TODO: Better penetration normal

                penetrationNormal = (collisionPoint - shape1.get_pos()).normalize()
                penetrationDepth = (penetrationNormal*shape1.get_radius() \
                                   - (collisionPoint - shape1.get_pos())).norm()

                
                assert isinstance(collisionPoint, Vector), \
                       'Invalid type for collisionPoint'
                assert isinstance(penetrationNormal, Vector), \
                       'Invalid type for penetrationNormal'
                assert isinstance(penetrationDepth, numbers.Number)
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
    assert isinstance(simplex, Simplex), 'Input must be a Simplex object'
    TOLERANCE = 0.00001     # If the origin is this close to a side
                            # or line in the simplex, we call it a hit

    # Get the last point added to the simplex
    a = simplex.get(1)
    
    # Compute AO (same thing as -A)
    ao = - a

    if len(simplex.get_points()) == 4:
        #print 'Tetrahedron'
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
            #print 'In R1, False'
            # The origin is in R1
            # Remove point d
            simplex.remove(4)
            # Set new direction to abcNormal
            direction = abcNormal
        elif abdNormal.dot(ao) > 0:
            #print 'In R2, False'
            # The origin is in R2
            # Remove point c
            simplex.remove(3)
            # Set new direction to abdNormal
            direction = abdNormal
        elif acdNormal.dot(ao) > 0:
            #print 'In R3, False'
            # The origin is in R3
            # Remove point b
            simplex.remove(2)
            # Set new direction to acdNormal
            direction = acdNormal
        else:
            # The origin is in R5, collision is confirmed
            #print 'True in tetrahedron'
            return True, None

    elif len(simplex.get_points()) == 3:
        #print 'Triangle'
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
            #print 'Origin in the plane'
            # Calculate the normals of ab and ac.
            abPerp = ac.triple_product_2(ab, ab)
            acPerp = ab.triple_product_2(ac, ac)

            # Check where the origin is
            if abPerp.dot(ao) > 0:
                #print 'In R1, False'
                # The origin is in R1
                # Remove c
                simplex.remove(3)
                # Set new direction to abPerp
                direction = abPerp
            elif acPerp.dot(ao) > 0:
                #print 'In R2, False'
                # The origin is in R2
                # Remove b
                simplex.remove(2)
                # Set new direction to acPerp
                direction = acPerp
            else:
                # The origin is in R3, collision confirmed
                #print 'True in triangle'
                #return True, None
                # The origin is in the simplex, return a normal to
                # be able to build the full tetrahedron and an empty
                # string to force it to continue
                # TODO: Ugly solution, fix?
                return '', ab.cross(ac)
        # Otherwise, set the new direction to normal
        else:
            #print 'Origin not in plane, False'
            direction = normal

    else:
        #print 'Line'
        # Then it's the line segment case
        b = simplex.get(2)

        # Compute AB
        ab = b - a

        if ab.dot(ao) < 0:
            #print 'False in line: direction ahead!'
            simplex.remove(2)
            direction = ao
        else:
            # Get the perp to AB in the direction of the origin
            abPerp = ab.triple_product_2(ao, ab)
            # If the origin lies on the same line as ab,
            # check if it lies on ab, if so, consider it a hit.
            if abPerp.norm() < TOLERANCE:
                #print 'On the line, True'
                # The origin is on the line, collision confirmed

                # The origin is in the simplex, return a normal to
                # be able to build the full tetrahedron and an empty
                # string to force it to continue
                # TODO: Ugly solution, fix?
                if ab.dot(Vector([1.0, 0.0, 0.0])) - ab.norm() < TOLERANCE:
                    return '', Vector([0.0, 1.0, 0.0])
                else:
                    return '', Vector([1.0, 0.0, 0.0])
            
            # Otherwise set the direction to abPerp
            else:
                #print 'False in line'
                direction = abPerp
    
    return False, direction

def pointOfCollision(simplex):
    ''' Returns the point in the shapes that represents the point of collision.
        This is calculated as the mean value of the points in the shapes that
        are closest to eachother. This is a pretty rough approximation, but
        could be sufficient for our needs. '''
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

    return collisionPoint

def pointOfCollision_2(simplex):
    ''' Another approach to calculating the collision point, using
        baryocentric coordinates. '''
    assert len(simplex.get_points()) == 4, 'Terminated without full simplex'
    #points in the minkowski simplex
    simpPoints = simplex.get_all_points(0)
    #points in the simplex of shape 1
    aPoints = simplex.get_all_points(1)
    #points in the simplex of shape 2
    bPoints = simplex.get_all_points(2)

    # create a matrix 
    matrix = [[1.0]*len(simpPoints)]
    vectors = []
    for vector in simpPoints:
        value = vector.value
        vectors.append(value)
    for i in range(len(vectors[0])):
        outvec = []
        for j in range(len(vectors)):
            outvec.append(vectors[j][i])
        matrix.append(outvec)
            

    barCoord = gauss.solve(matrix, [1.0, 0.0, 0.0, 0.0])
    if barCoord:
        collisionPoint = Vector()

        for i in range(len(aPoints)):
            collisionPoint += aPoints[i]*barCoord[i]
        assert isinstance(collisionPoint, Vector), 'Invalid type for collisionPoint'
        return collisionPoint
    else:
        return pointOfCollision(simplex)
    
