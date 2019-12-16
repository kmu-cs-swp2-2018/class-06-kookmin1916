from numpy import array
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtGui import QPixmap, QPainter
from Tile import TileImageList, TilesEnum


class View:
    def __init__(self):
        self.__tile_size = 72
        self.__width = 11
        self.__height = 11
        self.__x_pos = 15
        self.__y_pos = 15
        self.__multiplier = 1.0

        self.__TilePixList = array(
            [QPixmap(image).scaled(self.tile_size, self.tile_size) for image in TileImageList])
        self.__layout = QGridLayout()
        self.__layout.setSpacing(0)

        self.__view = array([[None] * self.height] * self.width)

        for x in range(self.width):
            for y in range(self.height):
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
        multiplier = self.tile_size / 96
        if player.weapon is not None:
            painter.drawImage(QRect(28 * multiplier, 32 * multiplier,
                                    48 * multiplier, 48 * multiplier), player.weapon.image)
        painter.end()

        self.__view[x_pos_in_view][y_pos_in_view].setPixmap(tile_pixmap)

    def update_view(self, drawing_map):
        for x in range(self.width):
            for y in range(self.height):
                map_x = self.left_x_pos + x
                map_y = self.top_y_pos + y

                if drawing_map[map_x][map_y] != TilesEnum.WALL.value:
                    self.__view[x][y].setPixmap(self.__TilePixList[drawing_map[map_x][map_y]])

                else:
                    tile_name = "image/separated_wall_tile/wall_tile"
                    separated_tile_list = [tile_name + str(number) + ".png" for number in range(1, 10)]

                    tile_pixmap = QPixmap(self.__TilePixList[TilesEnum.WALL.value])
                    separated_tile = [-1] * 9
                    direction_list = [[1, 0], [0, -1], [-1, 0], [0, 1]]
                    separated_tile[4] = 4
                    for number, direction in zip([5, 1, 3, 7], direction_list):
                        if drawing_map[map_x + direction[0]][map_y + direction[1]] == drawing_map[map_x][map_y]:
                            separated_tile[number] = 4
                        else:
                            separated_tile[number] = number

                    for number, tile_numbers, index in\
                            zip([2, 0, 6, 8], [[5, 1, 2], [1, 3, 0], [3, 7, 6], [7, 5, 8]], range(4)):
                        if drawing_map[map_x + direction_list[index][0]][map_y + direction_list[index][1]]\
                                == drawing_map[map_x][map_y]:
                            separated_tile[number] = tile_numbers[1]
                        if drawing_map[map_x + direction_list[(index + 1) % 4][0]]\
                                [map_y + direction_list[(index + 1) % 4][1]] == drawing_map[map_x][map_y]:
                            if separated_tile[number] == -1:
                                separated_tile[number] = tile_numbers[0]
                            else:
                                separated_tile[number] = 4
                        if separated_tile[number] == -1:
                            separated_tile[number] = tile_numbers[2]

                    painter = QPainter()
                    painter.begin(tile_pixmap)
                    for number in range(9):
                        tile_x = number % 3
                        tile_y = int(number / 3)
                        painter.drawPixmap(QRect(tile_x * self.tile_size / 3, tile_y * self.tile_size / 3,
                                                 self.tile_size / 3 + 0.99, self.tile_size / 3 + 0.99),
                                           QPixmap(separated_tile_list[separated_tile[number]]))
                    painter.end()
                    self.__view[x][y].setPixmap(tile_pixmap)

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
        return self.__x_pos - self.width // 2

    @property
    def top_y_pos(self):
        return self.__y_pos - self.height // 2

    @property
    def right_x_pos(self):
        return self.__x_pos + self.width // 2

    @property
    def bottom_y_pos(self):
        return self.__y_pos + self.height // 2

    @property
    def width(self):
        return int(self.__width * self.__multiplier)

    @property
    def height(self):
        return int(self.__height * self.__multiplier)

    @property
    def position(self):
        return self.__x_pos, self.__y_pos

    @property
    def tile_size(self):
        return self.__tile_size / self.__multiplier

    @property
    def multiplier(self):
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, multiplier):
        if multiplier == 0.0:
            raise
        if self.multiplier != multiplier:
            for x in range(self.width):
                for y in range(self.height):
                    self.__view[x][y].deleteLater()
            self.__multiplier = multiplier
            self.__view = array([[None] * self.height] * self.width)
            for x in range(self.width):
                for y in range(self.height):
                    self.__view[x][y] = QLabel()
                    self.__layout.addWidget(self.__view[x][y], y, x)
            self.__TilePixList = array(
                [QPixmap(image).scaled(self.tile_size + 0.99, self.tile_size + 0.99) for image in TileImageList])

    @position.setter
    def position(self, position):
        self.__x_pos, self.__y_pos = position

    @width.setter
    def width(self, width):
        if width < 1:
            raise
        self.__width = width

    @height.setter
    def height(self, height):
        if height < 1:
            raise
        self.__width = height
