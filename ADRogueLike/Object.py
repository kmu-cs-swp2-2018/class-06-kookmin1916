from enum import Enum
from numpy import array

from PyQt5.QtGui import QImage


class ObjectState(Enum):
    EXIST = 0
    REMOVED = 1


class Object:
    def __init__(self, image, x_pos, y_pos):
        if isinstance(image, str):
            self.__image = array([QImage(image)])
        else:
            self.__image = array([QImage(i) for i in image])
        self.__image_index = 0
        self.__x_pos = x_pos
        self.__y_pos = y_pos
        self.__state = ObjectState.EXIST

    def increase_index(self):
        self.__image_index = (self.__image_index + 1) % len(self.__image)

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        self.__image = image

    @property
    def position(self):
        return self.__x_pos, self.__y_pos

    @position.setter
    def position(self, position):
        self.__x_pos, self.__y_pos = position

    @property
    def x_pos(self):
        return self.__x_pos

    @x_pos.setter
    def x_pos(self, x_pos):
        self.__x_pos = x_pos

    @property
    def y_pos(self):
        return self.__y_pos

    @y_pos.setter
    def y_pos(self, y_pos):
        self.__y_pos = y_pos

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state

    @property
    def image_index(self):
        return self.__image_index

    @property
    def image_number(self):
        return len(self.__image)
