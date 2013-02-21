# Python implementation of the GJK algorithm in 3D

# TODO: Make a function that plots the Minkowski difference of two shapes;
# this would enable better graphical debugging.


from vector import *
from simplex import *

def support(shape1Points, shape2Points, direction):
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
    point1List = []
    point2List = []
    for point in shape1Points:
        point1List.append(point.dot(direction))

    for point in shape2Points:
        point2List.append(point.dot(direction.v_mult(-1.0)))
    
    point1 = shape1Points[point1List.index(max(point1List))]
    point2 = shape2Points[point2List.index(max(point2List))]

    # Perform the Minkowski Difference
    outPoint = point1.v_add(point2.v_mult(-1.0))

    return outPoint



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
    direction = shape2.get_pos().v_add(shape1.get_pos().v_mult(-1.0))
    
    # Get the first Minkowski Difference point
    simplex.add(support(shape1.get_points(), shape2.get_points(), direction))

    # Negate d for the next point
    direction = direction.v_mult(-1.0)
    
    # Start looping
    while True:
        # Add a new point to the simplex
        simplex.add(support(shape1.get_points(), shape2.get_points(), direction))

        # Make sure that the last point we added passed the origin
        if simplex.get(1).dot(direction) <= 0:
            # If the point added last was not past the origin in
            # the chosen direction then the Minkowski Sum cannot
            # possibly contain the origin since the last point
            # added is on the edge of the Minkowski Difference.
            return False
        else:
            # Otherwise we need to determine if the origin is in
            # the current simplex
            originInSimplex, direction = containsOrigin(simplex)
            if originInSimplex:
                # If it is then we know there is a collision
                return True




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
    ao = a.v_mult(-1.0)

    if len(simplex.get_points()) == 4:
        # It's the tetrahedon case

        # Get b, c and d
        b = simplex.get(2)
        c = simplex.get(3)
        d = simplex.get(4)

        # Compute the edges.
        # We only have to calculate some of them;
        # some can be reused, some are not needed
        ab = b.v_add(a.v_mult(-1.0))
        ac = c.v_add(a.v_mult(-1.0))
        ad = d.v_add(a.v_mult(-1.0))

        # Compute the normals
        # Since we can't be sure the winding of the triangles (?),
        # we do not yet know if these normals point "inwards" or "outwards"
        abcNormal = ab.cross(ac)
        abdNormal = ad.cross(ab)
        acdNormal = ac.cross(ad)

        # Make sure the normals are in the right direction
        abcNormal = abcNormal.v_mult(-abcNormal.dot(ad))
        abdNormal = abdNormal.v_mult(-abdNormal.dot(ac))
        acdNormal = acdNormal.v_mult(-acdNormal.dot(ab))

        # Check where the origin is
        if abcNormal.dot(ao) > 0:
            # The origin is in R1
            # Remove point d
            simplex.remove(d)
            # Set new direction to abcNormal
            direction = abcNormal
        elif abdNormal.dot(ao) > 0:
            # The origin is in R2
            # Remove point c
            simplex.remove(c)
            # Set new direction to abdNormal
            direction = abdNormal
        elif acdNormal.dot(ao) > 0:
            # The origin is in R3
            # Remove point b
            simplex.remove(b)
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
        ab = b.v_add(a.v_mult(-1.0))
        ac = c.v_add(a.v_mult(-1.0))

        # Get the normal to the surface in the direction of the origin
        normal1 = ab.cross(ac)
        normal = normal1.v_mult(normal1.dot(ao))
        
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
                simplex.remove(c)
                # Set new direction to abPerp
                direction = abPerp
            elif acPerp.dot(ao) > 0:
                # The origin is in R2
                # Remove b
                simplex.remove(b)
                # Set new direction to acPerp
                direction = acPerp
            else:
                # The origin is in R3, collision confirmed
                return True, None
        # Otherwise, set the new direction to normal
        else:
            direction = normal

    else:
        # Then it's the line segment case
        b = simplex.get(2)

        # Compute AB
        ab = b.v_add(a.v_mult(-1.0))

        # Get the perp to AB in the direction of the origin
        abPerp = ab.triple_product_2(ao, ab)
        # If the origin lies on the same line as ab,
        # check if it lies on ab, if so, consider it a hit.
        if abPerp.norm() < TOLERANCE:       # Might give false positives
            if ab.dot(ao) > 0:

                ###################
                # NOTE: That we even get here means that something's 
                # wrong with the calculation of a: it is on the wrong
                # side of the origin and should therefore already have
                # been discarded... 
                ###################
                
                # The origin is in R1
                # Remove b
                simplex.remove(b)
                # Set new direction to ao
                direction = ao
                # This line is added to prevent the program from
                # entering an endless loop and crash; it should really
                # return False...
                return True, None
            else:
                # The origin is on the line, collision confirmed
                return True, None
        
        # Otherwise set the direction to abPerp
        else:        
            direction = abPerp
        
    return False, direction
