from abc import abstractmethod
from PyQt5.QtGui import QImage
from enum import Enum


class ItemState(Enum):
    EXIST = 0
    REMOVED = 1


class Item:
    def __init__(self, image, x_pos, y_pos):
        self._image = QImage(image)
        self.__x_pos = x_pos
        self.__y_pos = y_pos
        self.__state = ItemState.EXIST.value

    @abstractmethod
    def use_item(self, player):
        pass

    @property
    def x_pos(self):
        return self.__x_pos

    @property
    def y_pos(self):
        return self.__y_pos

    @property
    def image(self):
        return self._image

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state


class SampleItem(Item):
    def __init__(self):
        super().__init__('image/Potion.png', 0, 0)

    def use_item(self, player):
        player.heal(5)
        self.state = ItemState.REMOVED.value
