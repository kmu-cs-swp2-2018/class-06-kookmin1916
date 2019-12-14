from numpy import array
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtGui import QPixmap, QPainter
from Tile import TileImageList


class View:
    def __init__(self):
        self.__TilePixList = array([QPixmap(image).scaled(96, 96) for image in TileImageList])

        self.__width = 7
        self.__height = 7
        self.__x_pos = 15
        self.__y_pos = 15

        self.__layout = QGridLayout()
        self.__layout.setSpacing(0)

        self.__view = array([[None] * self.__height] * self.__width)

        for x in range(self.__width):
            for y in range(self.__height):
                self.__view[x][y] = QLabel()
                self.__layout.addWidget(self.__view[x][y], y, x)

    def move(self, dx, dy):
        x_pos = self.__x_pos + dx
        y_pos = self.__y_pos + dy
        if x_pos < 0 or y_pos < 0:
            raise

        self.__x_pos = x_pos
        self.__y_pos = y_pos

    def draw_object(self, drawing_object):
        x_pos, y_pos = drawing_object.position
        if self.is_out_of_view(x_pos, y_pos):
            return False

        x_pos_in_view = x_pos - self.left_x_pos
        y_pos_in_view = y_pos - self.top_y_pos

        painter = QPainter()
        tile_pixmap = self.__view[x_pos_in_view][y_pos_in_view].pixmap()\
            .copy(self.__view[x_pos_in_view][y_pos_in_view].rect())
        painter.begin(tile_pixmap)
        painter.drawImage(tile_pixmap.rect(), drawing_object.image[drawing_object.image_index])
        painter.end()

        self.__view[x_pos_in_view][y_pos_in_view].setPixmap(tile_pixmap)

        return True

    def draw_equipment(self, player):
        x_pos_in_view = player.x_pos - self.left_x_pos
        y_pos_in_view = player.y_pos - self.top_y_pos

        tile_pixmap = self.__view[x_pos_in_view][y_pos_in_view].pixmap() \
            .copy(self.__view[x_pos_in_view][y_pos_in_view].rect())

        painter = QPainter()
        painter.begin(tile_pixmap)
        painter.drawImage(QRect(28, 32, 48, 48), player.weapon.image)
        painter.end()

        self.__view[x_pos_in_view][y_pos_in_view].setPixmap(tile_pixmap)

    def update_view(self, drawing_map):
        for x in range(self.__width):
            for y in range(self.__height):
                map_x = self.left_x_pos + x
                map_y = self.top_y_pos + y
                self.__view[x][y].setPixmap(self.__TilePixList[drawing_map[map_x][map_y]])

                tile_name = "image/separated_wall_tile"
                separated_tile_list = [tile_name + str(number) for number in range(1, 10)]

                connected_cnt = [0] * 9
                direction_list = [[[1, 0], [2, 5, 8]], [[0, 1], [0, 1, 2]], [[-1, 0], [0, 3, 6]], [[0, -1], [6, 7, 8]]]
                for direction, tile_number_list in direction_list:
                    if drawing_map[map_x - direction[0]][map_y - direction[1]] == drawing_map[map_x][map_y]:
                        for number in tile_number_list:
                            connected_cnt[number] += 1

    def is_out_of_view(self, x_pos, y_pos):
        if x_pos < self.left_x_pos\
                or x_pos > self.right_x_pos\
                or y_pos < self.top_y_pos\
                or y_pos > self.bottom_y_pos:
            return True
        return False

    def __getitem__(self, item):
        return self.__view[item]

    @property
    def layout(self):
        return self.__layout

    @property
    def left_x_pos(self):
        return self.__x_pos - self.__width // 2

    @property
    def top_y_pos(self):
        return self.__y_pos - self.__height // 2

    @property
    def right_x_pos(self):
        return self.__x_pos + self.__width // 2

    @property
    def bottom_y_pos(self):
        return self.__y_pos + self.__height // 2

    @property
    def width(self):
        return self.__width

    @property
    def position(self):
        return self.__x_pos, self.__y_pos

    @position.setter
    def position(self, position):
        self.__x_pos, self.__y_pos = position

    @width.setter
    def width(self, width):
        if width < 1:
            raise
        self.__width = width

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        if height < 1:
            raise
        self.__width = height
