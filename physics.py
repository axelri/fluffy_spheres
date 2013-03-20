from vector import *

def collision_response(shape1, shape2, collisionPoint, penetrationNormal, penetrationDepth):

    invMass1 = 1 / shape1.get_mass()
    invMass2 = 1 / shape2.get_mass()

    relativeVel = shape1.get_velocity() - shape2.get_velocity()

    if relativeVel.dot(penetrationNormal) < 0:
        return
    
    e = 1.0     # coefficient of elasticity

    v_ab = relativeVel
    n = penetrationNormal   

    impulse = -(1+e)*v_ab.dot(n)/((invMass1+invMass2)*n.dot(n))

    

    # Hack to prevent sinking
    #impulse += penetrationDepth*1.5

    shape1.add_velocity(n*impulse*invMass1)
    shape2.add_velocity(n*impulse*invMass2*(-1.0))
