import sys
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from time import sleep
import threading

from Player import Player
from Inventory import Inventory
from Map import Map
from Mouse import Mouse
from Draw import Draw
import Enemy
import Character
import Structure
from Object import ObjectState


class Game(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ended = False
        self.animation_update_time = 0.13

        self.map = Map()
        self.player = Player("image/player.png", x_pos=15, y_pos=15, stat_hp=20, stat_str=5, stat_arm=1)
        staircase = Structure.Staircase(5, 15)
        self.object_list = [self.player, Enemy.Slime(13, 13), staircase]
        self.inventory = Inventory()
        self.draw = Draw()
        self.setWindowTitle("ADRogue")
        self.setStyleSheet("background-color: #B7A284")
        self.setCentralWidget(self.draw)

        self.update_animation_thread = threading.Thread(target=self.update_animation)

        self.update_animation_thread.start()

    def draw_all(self):
        self.draw.view.position = self.player.position
        self.draw.draw_map(self.map)
        for obj in self.object_list:
            self.draw.view.draw_object(obj)
        self.draw.draw_inventory(self.inventory, self.player)
        self.draw.view.draw_equipment(self.player)

        self.draw.hp_bar.clear()
        for obj in self.object_list:
            if isinstance(obj, Character.Character):
                self.draw.hp_bar.setText(self.draw.hp_bar.text() + type(obj).__name__ + " : " + str(obj.hp) + ", ")
        self.draw.hp_bar.setText(self.draw.hp_bar.text() + "player damage : " + str(self.player.damage) + ", ")
        self.draw.hp_bar.setText(self.draw.hp_bar.text() + "player arm : " + str(self.player.arm) + ", ")
        for s in self.player.status:
            self.draw.hp_bar.setText(self.draw.hp_bar.text() + type(s).__name__ + " : " + str(s.duration) + ", ")

    def next_level(self):
        self.map.generate_map()
        self.player.position = 15, 15

    def process_turn(self):
        print(self.player.position)
        for obj in self.object_list:
            if isinstance(obj, Character.Character):
                obj.process_status()
            if isinstance(obj, Enemy.Enemy):
                obj.behavior(self)

        temp_obj_list = []
        for obj in self.object_list:
            if obj.state != ObjectState.REMOVED:
                temp_obj_list += [obj]
        self.object_list = temp_obj_list

    def update_animation(self):
        while not self.ended:
            for obj in self.object_list:
                obj.increase_index()
            sleep(self.animation_update_time)

    def paintEvent(self, event):
        self.draw_all()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.player.move(1, 0, self)
            self.process_turn()
        if event.key() == Qt.Key_Left:
            self.player.move(-1, 0, self)
            self.process_turn()
        if event.key() == Qt.Key_Up:
            self.player.move(0, -1, self)
            self.process_turn()
        if event.key() == Qt.Key_Down:
            self.player.move(0, 1, self)
            self.process_turn()

    def mousePressEvent(self, event):
        self.inventory.use_item(event.x(), event.y(), self.player)
        print(event.x(), event.y())
        self.inventory.process_removed_item()

    def closeEvent(self, event):
        self.ended = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())
