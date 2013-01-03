from pygame.locals import *

### World physics constants ###
GRAVITY = 10

#### Sphere constants ####
SPHERE_COLOR = [0.5, 1, 0]
SPHERE_RADIUS = 1
SPHERE_SPEED = 0.05
SPHERE_JUMP_SPEED = 300

#### Cube constants ####
CUBE_COLOR = [0.5, 0, 1]
CUBE_SIDE = 2
CUBE_SPEED = 0.05
CUBE_JUMP_TIME = 60
CUBE_JUMP_SPEED = 0.3
CUBE_JUMP_HEIGHT = 3.0

#### User input constants ####
DEFAULT_MOVE_LEFT_KEY = K_a
DEFAULT_MOVE_RIGHT_KEY = K_d
DEFAULT_MOVE_FORWARD_KEY = K_w
DEFAULT_MOVE_BACKWARD_KEY = K_s
DEFAULT_JUMP_KEY = K_SPACE

#### Graphic settings constants ####
WINDOW_FPS = 60
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
