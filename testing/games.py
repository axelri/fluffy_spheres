import shapes

class Game():
    ''' A class containing all the objects in the game '''
    def __init__(self, player, objectList, sceneList):
        # TODO: Use the Player object from fluffy instead?
        assert isinstance(player, shapes.Shape), 'Input must be a Shape object'
        assert isinstance(objectList, list), 'Input must be a list'
        assert isinstance(sceneList, list), 'Input must be a list'
        if __debug__:
            for item in objectList:
                assert isinstance(item, shapes.Shape), \
                       'All items in objectList must be Shape objects'
            for item in sceneList:
                assert isinstance(item, shapes.Shape), \
                       'All items in sceneList must be Shape objects'
        self._player = player
        self._objectList = objectList
        self._sceneList = sceneList

    def get_objects(self):
        return self._player, self._objectList, self._sceneList
