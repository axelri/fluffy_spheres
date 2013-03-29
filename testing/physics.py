import vectors
import collisions
import shapes
import numbers
import games

GRAVITY = vectors.Vector([0.0, -10.0, 0.0])
dt = 0.0005

def collision_response(shape1, shape2, collisionInfo):
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

    invMass1 = 1.0/shape1.get_mass()
    invMass2 = 1.0/shape2.get_mass()

    relativeVel = shape1.get_velocity() - shape2.get_velocity()

    if relativeVel.dot(penetrationNormal) < 0:
        # They are moving apart, no need to apply an impulse
        return
    
    e = 0.0     # coefficient of elasticity

    v_ab = relativeVel
    n = penetrationNormal   

    impulse = -(1+e)*v_ab.dot(n)/((invMass1+invMass2)*n.dot(n))

    #print 'impulse before:', impulse
    # Hack to prevent sinking
    impulse -= penetrationDepth*1.0
    #print 'depth:', penetrationDepth
    #print 'impulse after:', impulse
    shape1.add_velocity(n*impulse*invMass1)
    shape2.add_velocity(n*impulse*invMass2*(-1.0))


def update_physics(game):
    ''' Updates all physics in the game; takes all the objects in
        the game, calculates collisions etc and moves them to their
        new locations.'''
    assert isinstance(game, games.Game), 'Input must be a game object'
    # TODO: Make it have an input called dt, which gives it the
    # timestep it should simulate

    player, objectList, sceneList = game.get_objects()
    #print ''
    for item in objectList:
        #print 'Checking collision with item:', item

        collided, collisionInfo = collisions.GJK(player, item)

        if collided:
            #print 'Player collided with item'
            collision_response(player, item, collisionInfo)

        for thing in sceneList:
            collided, collisionInfo = collisions.GJK(item, thing)

            if collided:
                #print 'Item collided with scene'
                collision_response(item, thing, collisionInfo)

    for item in sceneList:
        #print 'Checking collision with scene:', item

        collided, collisionInfo = collisions.GJK(player, item)

        if collided:
            #print 'Player collided with scene'
            collision_response(player, item, collisionInfo)
    
    # TODO: switch to semi-implicit Euler integration
    
    player.add_velocity(GRAVITY*dt)
    player.add_pos(player.get_velocity())

    for item in objectList:
        item.add_velocity(GRAVITY*dt)
        item.add_pos(item.get_velocity())
