class Player(object):
    ''' Defines a generic player with a set of playing keys,
    a name and the shape associated with the player'''
    def __init__(self, name, shape, moveLeft, moveRight,
                moveForward, moveBackward, jump):
        self._name = name
        self._shape = shape
        self._moveLeft = moveLeft
        self._moveRight = moveRight
        self._moveForward = moveForward
        self._moveBackward = moveBackward
        self._jump = jump

    def get_name(self):
        return self._name

    def get_shape(self):
        return self._shape

    def set_shape(self, shape):
        self._shape = shape

    def get_move_keys(self):
        return [self._moveLeft, self._moveRight,
                self._moveForward, self._moveBackward]

    def get_move_left_key(self):
        return self._moveLeft

    def set_move_left_key(self, moveLeft):
        self._moveLeft = moveLeft

    def get_move_right_key(self):
        return self._moveRight

    def set_move_right_key(self, moveRight):
        self._moveRight = moveRight

    def get_move_forward_key(self):
        return self._moveForward

    def set_move_forward_key(self, moveForward):
        self._moveForward = moveForward

    def get_move_backward_key(self):
        return self._moveBackward

    def set_move_backward_key(self):
        self._moveBackward = moveBackward

    def get_jump_key(self):
        return self._jump

    def set_jump_key(self, jump):
        self._jump = jump
