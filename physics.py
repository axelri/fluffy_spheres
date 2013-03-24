from vector import *
from GJK import GJK

GRAVITY = Vector([0.0, -10.0, 0.0])
dt = 0.0015

def collision_response(shape1, shape2, collisionInfo):

    collisionPoint, penetrationNormal, penetrationDepth = collisionInfo


    mass1 = shape1.get_mass()
    mass2 = shape2.get_mass()
    if mass1 > 1000:
        invMass1 = 0
    else:
        invMass1 = 1 / mass1
    if mass2 > 1000:
        invMass2 = 0
    else:
        invMass2 = 1 / mass2

    relativeVel = shape1.get_velocity() - shape2.get_velocity()

    if relativeVel.dot(penetrationNormal) < 0:
        return
    
    e = 0.1     # coefficient of elasticity

    v_ab = relativeVel
    n = penetrationNormal   

    impulse = -(1+e)*v_ab.dot(n)/((invMass1+invMass2)*n.dot(n))

    

    # Hack to prevent sinking
    impulse -= penetrationDepth*1.5

    shape1.add_velocity(n*impulse*invMass1)
    shape2.add_velocity(n*impulse*invMass2*(-1.0))


def update_physics(game):
    ''' Updates all physics in the game; takes all the objects in
        the game, calculates collisions etc and moves them to their
        new locations.'''
    # TODO: make it have an input called dt, which gives it the
    # timestep it should simulate

    player, objectList, sceneList = game.get_objects()

    for item in objectList:

        collided, collisionInfo = GJK(player, item)

        if collided:
            collision_response(player, item, collisionInfo)

    for item in sceneList:

        collided, collisionInfo = GJK(player, item)

        if collided:
##            point, normal, depth = collisionInfo
##            print 'Collision information:'
##            print '\tCollision point:', point.value
##            print '\tCollision normal:', normal.value
##            print '\tCollision depth:', depth
##            print ''
            collision_response(player, item, collisionInfo)


    # TODO: switch to semi-implicit Euler integration

    player.add_velocity(GRAVITY*dt)
    player.update_pos(player.get_velocity())

    for item in objectList:
        item.add_velocity(GRAVITY*dt)
        item.update_pos(item.get_velocity())
        item.update_points(item.get_velocity())
