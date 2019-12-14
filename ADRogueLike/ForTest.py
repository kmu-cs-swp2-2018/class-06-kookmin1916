import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 400)

        self.main_layout = QGridLayout()
        self.label = QLabel()


        qp = QPainter()

        pixmap = QPixmap("image/map_wall.png")
        qp.begin(pixmap)
        character = QPixmap("image/player.png")
        qp.drawPixmap(pixmap.rect(), character)
        self.label.setPixmap(pixmap)


        qp.end()

        self.main_layout.addWidget(self.label, 0, 0)

        self.setLayout(self.main_layout)
        self.setWindowTitle("ADRogue")  # Project-Rogue
        self.show()

    """def paintEvent(self, event):
        print("A")
        qp = QPainter()

        pixmap = QPixmap("image/map_wall.png")
        qp.begin(pixmap)

        painter = QPainter(pixmap)
        character = QPixmap("image/player.png")
        # painter.drawPixmap(self.label.rect(), pixmap)
        painter.drawPixmap(self.label.rect(), character)
        self.label.setPixmap(pixmap)

        # self.paint_event(event)

        qp.end()"""

    """def paint_event(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("image/map_wall.png")
        character = QPixmap("image/player.png")
        painter.drawPixmap(self.rect(), pixmap)
        painter.drawPixmap(self.rect(), character)
        pass"""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())