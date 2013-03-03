# Python implementation of the GJK algorithm in 3D

# TODO: Make a function that plots the Minkowski difference of two shapes;
# this would enable better graphical debugging.


from vector import *
from simplex import *

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
    # TODO: make a support function for each shape,
    # e.g. shape.support_func(direction), that returns point1 and
    # point2 that are used in this algorithm. Different types of
    # shapes can have better and more efficient algorithms than
    # the one used here. This algorithm works for an arbitrary
    # convex set of vertices, whereas e.g. a sphere would have
    # something like self.center + direction*radius.
    
    # Get points on the edge of the shapes in opposite directions
    point1List = []
    point2List = []
    shape1Points = shape1.get_points()
    shape2Points = shape2.get_points()
    for point in shape1Points:
        point1List.append(point.dot(direction))

    for point in shape2Points:
        point2List.append(point.dot(-direction))
    
    point1 = shape1Points[point1List.index(max(point1List))]
    point2 = shape2Points[point2List.index(max(point2List))]

    # Perform the Minkowski Difference
    outPoint = point1 - point2

    return outPoint, point1, point2



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
                False otherwise.
    '''

    # Create a Simplex object
    simplex = Simplex()

    # Choose an initial search direction
    direction = shape2.get_pos() - shape1.get_pos()
    
    # Get the first Minkowski Difference point
    simplex.add(support(shape1, shape2, direction))
    simplex.add(support(shape1, shape2, -direction))

##    a = simplex.get(1)
##    b = simplex.get(2)
##
##    if a.dot(b) > 0:
##        # Both points on the same side of the origin: no collision, return False
##        print 'False in first check'
##        print 'a:', a.get_value()
##        print 'b:', b.get_value()
##        return False
    # Get the next direction
    originInSimplex, direction = containsOrigin(simplex)
    if originInSimplex:
        # Collision, return True
        #print 'True in first check'
        collisionPoint = pointOfCollision(simplex)
        return True, collisionPoint
    
    # Start looping
    while True:
        #print 'New loop'
        # Add a new point to the simplex
        # TODO: Take care of if the simplex already contains the point.
        simplex.add(support(shape1, shape2, direction))

        # Make sure that the last point we added passed the origin
        if simplex.get(1).dot(direction) <= 0:
            # If the point added last was not past the origin in
            # the chosen direction then the Minkowski Sum cannot
            # possibly contain the origin since the last point
            # added is on the edge of the Minkowski Difference.
            #print 'False in loop'
            return False, None
        else:
            # Otherwise we need to determine if the origin is in
            # the current simplex
            originInSimplex, direction = containsOrigin(simplex)
            if originInSimplex:
                # If it is then we know there is a collision
                #print 'True in loop'
                collisionPoint = pointOfCollision(simplex)
                return True, collisionPoint




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
                return True, None
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
            simplex.remove(b)
            direction = ao
        else:
            # Get the perp to AB in the direction of the origin
            abPerp = ab.triple_product_2(ao, ab)
            # If the origin lies on the same line as ab,
            # check if it lies on ab, if so, consider it a hit.
            if abPerp.norm() < TOLERANCE:       # Might give false positives
                #print 'On the line, True'
                #print 'a:', a.get_value()
                #print 'b:', b.get_value()
                #print 'ao:', ao.get_value()
                #print 'ab:', ab.get_value()
                # The origin is on the line, collision confirmed
                return True, None
            
            # Otherwise set the direction to abPerp
            else:
                #print 'False in line'
                direction = abPerp
    
    return False, direction

def pointOfCollision(simplex):
    ''' Returns the point in the shapes that represents the point of collision.
        This is calculated as the mean value of the points in the shapes that
        are closest to eachother. This is a pretty rough approximation, but
        should be sufficient for our needs. '''

    a = simplex.get(1)
    ao = -a

    if len(simplex.get_points()) == 4:
        # Tetrahedron
        
        # Get b, c and d
        b = simplex.get(2)
        c = simplex.get(3)
        d = simplex.get(4)

        # Compute the edges.
        ab = b - a
        cb = b - c
        cd = c - d

        bcdNormal = cb.cross(cd)
        bcdNormal *= bcdNormal.dot(ab)

        if ao.dot(bcdNormal)/ab.dot(bcdNormal) < 0.5:
            # a is closest
            points = simplex.get_all(1)
            collisionPoint = (points[1]+points[2])*0.5
        else:
            # bcd is closest
            cdPerp = cb.triple_product_2(cd, cd)
            bo = -b

            if abs(bo.dot(cdPerp)/cb.dot(cdPerp)) < 0.5:
                # b is closest
                points = simplex.get_all(2)
                collisionPoint = (points[1]+points[2])*0.5
            else:
                # cd is closest
                co = -c
                if co.proj_norm(cd)/cd.norm() < 0.5:
                    # c is closest
                    points = simplex.get_all(3)
                    collisionPoint = (points[1]+points[2])*0.5
                else:
                    # d is closest
                    points = simplex.get_all(4)
                    collisionPoint = (points[1]+points[2])*0.5

    elif len(simplex.get_points()) == 3:
        # Triangle

        b = simplex.get(2)
        c = simplex.get(3)

        ba = a - b
        bc = c - b

        bcPerp = ba.triple_product_2(bc, bc)

        if abs(ao.dot(bcPerp)/ba.dot(bcPerp)) < 0.5:
            # a is closest
            points = simplex.get_all(1)
            collisionPoint = (points[1]+points[2])*0.5
        else:
            # bc is closest
            bo = -b
            if bo.proj_norm(bc)/bc.norm() < 0.5:
                # b is closest
                points = simplex.get_all(2)
                collisionPoint = (points[1]+points[2])*0.5
            else:
                # c is closest
                points = simplex.get_all(3)
                collisionPoint = (points[1]+points[2])*0.5

    else:
        # Line

        b = simplex.get(2)
        if ao.proj_norm(ab)/ab.norm() < 0.5:
            # a is closest
            points = simplex.get_all(1)
            collisionPoint = (points[1]+points[2])*0.5
        else:
            # b is closest
            points = simplex.get_all(2)
            collisionPoint = (points[1]+points[2])*0.5

        

    return collisionPoint
