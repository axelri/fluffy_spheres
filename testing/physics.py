import vectors
import collisions
import shapes
import numbers
import games

GRAVITY = vectors.Vector([0.0, -10.0, 0.0])
dt = 0.00015

def collision_response(shape1, shape2, collisionInfo):
    print 'Entered collision_response'
    assert isinstance(shape1, shapes.Shape), 'Input must be a Shape object'
    assert isinstance(shape2, shapes.Shape), 'Input must be a Shape object'
    assert isinstance(collisionInfo, tuple), 'Input must be a tuple'
    assert len(collisionInfo) == 3, 'CollisionInfo must be of length 3'

    collisionPoint, penetrationNormal, penetrationDepth = collisionInfo

    assert isinstance(collisionPoint, vectors.Vector), \
           'Input must be a vector'
    assert isinstance(penetrationNormal, vectors.Vector), \
           'Input must be a vector'
    assert isinstance(penetrationDepth, numbers.Number), \
           'Input must be a number'

    if penetrationNormal.dot(shape2.get_pos() - shape1.get_pos()) < 0:
        # It's pointing the wrong way
        penetrationNormal *= -1.0

    mass1 = shape1.get_mass()
    mass2 = shape2.get_mass()
    if mass1 > 1000:        # It is immobile
        invMass1 = 0
    else:
        invMass1 = 1 / mass1
    if mass2 > 1000:        # It is immobile
        invMass2 = 0
    else:
        invMass2 = 1 / mass2

    relativeVel = shape1.get_velocity() - shape2.get_velocity()

    if relativeVel.dot(penetrationNormal) < 0:
        # They are moving apart, no need to apply an impulse
        return
    
    e = 0.1     # coefficient of elasticity

    v_ab = relativeVel
    n = penetrationNormal   

    impulse = -(1+e)*v_ab.dot(n)/((invMass1+invMass2)*n.dot(n))

    print 'Impulse:', impulse

    

    # Hack to prevent sinking
    impulse -= penetrationDepth*1.5

    shape1.add_velocity(n*impulse*invMass1)
    shape2.add_velocity(n*impulse*invMass2*(-1.0))


def update_physics(game):
    ''' Updates all physics in the game; takes all the objects in
        the game, calculates collisions etc and moves them to their
        new locations.'''
    assert isinstance(game, games.Game), 'Input must be a game object'
    # TODO: make it have an input called dt, which gives it the
    # timestep it should simulate

    player, objectList, sceneList = game.get_objects()

    for item in objectList:

        collided, collisionInfo = collisions.GJK(player, item)

        if collided:
            collision_response(player, item, collisionInfo)

    for item in sceneList:

        collided, collisionInfo = collisions.GJK(player, item)

        if collided:
            point, normal, depth = collisionInfo
            print 'Collision information:'
            print '\tCollision point:', point.value
            print '\tCollision normal:', normal.value
            print '\tCollision depth:', depth
            print '\tPlayer position:', player.get_pos().value
            print ''
            collision_response(player, item, collisionInfo)


    # TODO: switch to semi-implicit Euler integration

    player.add_velocity(GRAVITY*dt)
    player.add_pos(player.get_velocity())

    for item in objectList:
        item.add_velocity(GRAVITY*dt)
        item.add_pos(item.get_velocity())
