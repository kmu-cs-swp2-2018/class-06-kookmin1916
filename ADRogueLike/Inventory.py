from numpy import array

import Item
from Item import ItemState


class Inventory:
    def __init__(self):
        self.__width = 5
        self.__height = 5
        self.__cell_width = 68.57
        self.__cell_height = 68.57
        self.__cell_space = 6.857
        self.__x_pos = 20
        self.__y_pos = 288
        self.__inventory = array([[Item.SampleItem() for i in range(self.__width)] for j in range(self.__height)])

    def add_item(self, item):
        for x in range(self.__width):
            for y in range(self.__height):
                if self.__inventory[x][y] is not None:
                    self.__inventory[x][y] = item
                    return True
        return False

    def use_item(self, x_pos, y_pos, player):
        for x in range(self.width):
            for y in range(self.height):
                left_x = self.x_pos + x * (self.cell_width + self.cell_space) + 680
                top_y = self.y_pos + y * (self.cell_height + self.cell_space) + 12
                if left_x < x_pos < left_x + self.cell_width\
                        and top_y < y_pos < top_y + self.cell_height:
                    if self.__inventory[x][y] is None:
                        return False
                    self.__inventory[x][y].use_item(player)
                    return True
        return False

    def process_removed_item(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.__inventory[x][y] is not None and self.__inventory[x][y].state == ItemState.REMOVED.value:
                    self.__inventory[x][y] = None

    def __getitem__(self, item):
        return self.__inventory[item]

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def cell_width(self):
        return self.__cell_width

    @property
    def cell_height(self):
        return self.__cell_height

    @property
    def cell_space(self):
        return self.__cell_space

    @property
    def x_pos(self):
        return self.__x_pos

    @property
    def y_pos(self):
        return self.__y_pos
