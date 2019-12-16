import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QGuiApplication, QColor, QFont
from PyQt5.QtGui import QPixmap, QPainter
from numpy import array

from Map import Map
from Tile import TilesEnum, TileImageList
from Character import Character
from Inventory import Inventory
from View import View
from Object import ObjectState


class Draw(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__view = View()
        self.__inventory_label = QLabel()
        self.__inventory_label.setPixmap(QPixmap("image/Inventory.png").scaled(
            self.__view.width * self.__view.tile_size * 120 / 196 * (7 / self.__view.width),
            self.__view.height * self.__view.tile_size * (7 / self.__view.height)))  # 120 196
        # self.hp_bar = QLabel()  # this code for test

        self.__main_layout = QGridLayout()
        self.__main_layout.setSpacing(0)
        self.__main_layout.addLayout(self.__view.layout, 0, 0)
        self.__main_layout.addWidget(self.__inventory_label, 0, 1)
        # self.__main_layout.addWidget(self.hp_bar, 1, 0)  # this code for test

        self.setStyleSheet("background-color: #B7A284;")
        # container.setStyleSheet("background-color:black;")
        self.setLayout(self.__main_layout)

    def draw_map(self, drawing_map):
        self.__view.update_view(drawing_map)

    def draw_inventory(self, game):
        inventory = game.inventory
        player = game.player

        painter = QPainter()
        inventory_pixmap = QPixmap("image/Inventory.png").scaled(
            self.__view.width * self.__view.tile_size * 120 / 196,
            self.__view.height * self.__view.tile_size)

        painter.begin(inventory_pixmap)
        for x in range(inventory.width):
            for y in range(inventory.height):
                if inventory[x][y] is None:
                    continue
                object_pixmap = QPixmap(inventory[x][y].image)
                painter.drawPixmap(QRect((inventory.x_pos + x * (inventory.cell_width + inventory.cell_space))
                                         , (inventory.y_pos + y * (inventory.cell_height + inventory.cell_space))
                                         , inventory.cell_width, inventory.cell_height), object_pixmap)

        multiplier = (self.__view.height * self.__view.tile_size) / (7 * 96)
        if player.weapon is not None and player.state == ObjectState.EXIST:
            painter.drawImage(QRect(317 * multiplier, 26 * multiplier, 78 * multiplier, 78 * multiplier),
                              player.weapon.image)

        if player.armor is not None and player.state == ObjectState.EXIST:
            painter.drawImage(QRect((317 - 4) * multiplier, (111 + 4) * multiplier, 78 * multiplier, 78 * multiplier),
                              player.armor.image)

        string_list = [
            "HP : %d/%d" % (player.hp, player.stat_hp),
            "STR : %d(%d)" % (player.stat_str, player.damage),
            "ARM : %d(%d)" % (player.stat_arm, player.arm),
            "EXP : %d/%d" % (player.exp, player.max_exp),
            "LEVEL : %d" % player.level,
            "STAGE LEVEL : %d" % game.stage_level
        ]
        painter.setPen(QColor(0, 0, 0))
        painter.setFont(QFont('URW Chancery L', 15 * multiplier))
        space = 20
        for i in range(len(string_list)):
            painter.drawText(QRect(35 * multiplier, (40 + space * i) * multiplier, 200 * multiplier, 100 * multiplier),
                             Qt.AlignLeft, string_list[i])

        status_size = 32
        painter.setFont(QFont('URW Chancery L', 15 * multiplier))
        for i in range(len(player.status)):
            if player.status[i].image is not None:
                j = int(i / 6)
                painter.drawImage(QRect((30 + status_size * i) * multiplier, (210 + status_size * j) * multiplier,
                                  status_size * multiplier, status_size * multiplier), player.status[i].image)
                painter.drawText(QRect((30 + status_size * i) * multiplier, (205 + status_size * j) * multiplier,
                                       status_size * multiplier, status_size * multiplier), Qt.AlignRight,
                                 str(player.status[i].duration))

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
