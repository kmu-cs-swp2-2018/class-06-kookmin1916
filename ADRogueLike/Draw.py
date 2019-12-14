import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtGui import QPixmap, QPainter
from numpy import array

from Map import Map
from Tile import TilesEnum, TileImageList
from Character import Character
from Inventory import Inventory
from View import View


class Draw(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__view = View()
        self.__inventory_label = QLabel()
        self.__inventory_label.setPixmap(QPixmap("image/Inventory.png").scaled(
            self.__view.height * 96 * 120 / 196, self.__view.height * 96))  # 120 196
        self.hp_bar = QLabel()  # this code for test

        self.__main_layout = QGridLayout()
        self.__main_layout.setSpacing(0)
        self.__main_layout.addLayout(self.__view.layout, 0, 0)
        self.__main_layout.addWidget(self.__inventory_label, 0, 1)
        self.__main_layout.addWidget(self.hp_bar, 1, 0)  # this code for test

        self.setStyleSheet("background-color: #B7A284;")
        # container.setStyleSheet("background-color:black;")
        self.setLayout(self.__main_layout)

    def draw_map(self, drawing_map):
        self.__view.update_view(drawing_map)  # this code for test

    def draw_inventory(self, inventory, player):
        painter = QPainter()
        inventory_pixmap = QPixmap("image/Inventory.png").scaled(
            self.__view.height * 96 * 120 / 196, self.__view.height * 96)

        painter.begin(inventory_pixmap)
        for x in range(inventory.width):
            for y in range(inventory.height):
                if inventory[x][y] is None:
                    continue
                object_pixmap = QPixmap(inventory[x][y].image)
                painter.drawPixmap(QRect(inventory.x_pos + x * (inventory.cell_width + inventory.cell_space),
                                         inventory.y_pos + y * (inventory.cell_height + inventory.cell_space),
                                         inventory.cell_width, inventory.cell_height), object_pixmap)

        if player.weapon is not None:
            painter.drawImage(QRect(313, 26, 78, 78), player.weapon.image)

        painter.end()
        self.__inventory_label.setPixmap(inventory_pixmap)

    def closeEvent(self, event):
        print("Draw Close!")

    @property
    def view(self):
        return self.__view

    @property
    def main_layout(self):
        return self.__main_layout


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Draw()
    form.show()
    sys.exit(app.exec_())

# getter/setter
# constant naming
# map in view
# map naming
