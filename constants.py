from pygame.locals import *

### World physics constants ###
GRAVITY = 10.0
SLOW_DOWN = 1000.0

### Other world constants ###
# TODO: Make this part of a surface object for example?
GROUND_LEVEL = 0.0

#### Sphere constants ####
SPHERE_COLOR = [0.5, 1.0, 0.0]
SPHERE_RADIUS = 1.0
SPHERE_SPEED = 0.05
SPHERE_JUMP_SPEED = 300.0

#### Cube constants ####
CUBE_COLOR = [0.5, 0, 1]
CUBE_SIDE = 2.0
CUBE_SPEED = 0.025
CUBE_JUMP_SPEED = 300.0

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
