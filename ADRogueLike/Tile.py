from enum import Enum
from numpy import array
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage


class TilesEnum(Enum):
    WALL = 0
    TILE = 1
    GROUND = 2


TileImageList = array([
    QImage("image/map_wall.png"),  # 0
    QImage("image/tile_demo.png"),  # 1
    QImage("image/ground.png")  # 2
])

TileSolidState = array([
    True,  # 0
    False,  # 1
    False  # 2
])
