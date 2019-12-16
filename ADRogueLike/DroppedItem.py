from Object import Object
import Item
from PyQt5.QtGui import QImage


class DroppedItem(Object):
    def __init__(self, item, x_pos, y_pos):
        super().__init__(item.image, x_pos, y_pos)
        self.__item = item

    @property
    def item(self):
        return self.__item
