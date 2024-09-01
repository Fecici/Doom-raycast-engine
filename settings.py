import math
WWIDTH, WHEIGHT = 1600, 900
HALF_WWIDTH, HALF_WHEIGHT = WWIDTH // 2, WHEIGHT // 2
RES = (WWIDTH, WHEIGHT)
TILESIZE = 50
FPS = 999

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FLOOR_COLOR = (26, 6, 6)

# player
PLAYER_POS = 3, 2.5  # * tilesize
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.005
PLAYER_SIZE = 60
PLAYER_MAX_HEALTH = 100

NPC_SIZE = 60

MOUSE_SENSITIVITY = 0.0003
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WWIDTH - MOUSE_BORDER_LEFT

# raycast
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WWIDTH // 2  # this is enough
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = WWIDTH // TILESIZE + 10

SCREEN_DISTANCE = HALF_WWIDTH / math.tan(HALF_FOV)  # tan = o/a <=> a = o/tan
SCALE = WWIDTH // NUM_RAYS  # the elemental value of the rectangles. this is essentially the width, or "pixel" of each rectangle

# textures
TEXTURE_SIZE = 2 ** 8
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2
