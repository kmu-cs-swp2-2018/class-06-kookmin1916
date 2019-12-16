import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from time import sleep
import threading

from Player import Player
from Inventory import Inventory
from Map import Map
from Draw import Draw
import Enemy
import Character
import Structure
from Object import ObjectState
import Status
from DroppedItem import DroppedItem
import Potion
import Item


class Game(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stage_level = 1
        self.ended = False
        self.animation_update_time = 0.13
        self.animation_update_time = 0.13

        self.map = Map()
        self.player = Player("image/player.png", x_pos=0, y_pos=0, stat_hp=25, stat_str=5, stat_arm=1)
        self.staircase = Structure.Staircase(0, 0)
        self.player.position, self.staircase.position, character_list, object_list\
            = self.map.generate_map(self.stage_level)
        self.character_list = [self.player] + character_list
        self.object_list = [self.staircase] + object_list

        self.draw = Draw()
        self.inventory = Inventory(self.draw.view)
        self.setWindowTitle("ADRogue")
        self.setStyleSheet("background-color: #B7A284")
        self.setCentralWidget(self.draw)

        self.map.set_object_map(self.object_list)
        self.map.set_character_map(self.character_list)

        self.draw.setFixedSize(QSize(1294, 810))
        self.update_animation_thread = threading.Thread(target=self.update_animation)

        self.update_animation_thread.start()

    def draw_all(self):
        self.draw.view.position = self.player.position
        self.draw.draw_map(self.map)
        for obj in self.object_list:
            self.draw.view.draw_object(obj)
        for character in self.character_list:
            self.draw.view.draw_object(character)
        self.draw.draw_inventory(self)
        self.draw.view.draw_equipment(self.player)

        """self.draw.hp_bar.clear()
        for character in self.character_list:
            self.draw.hp_bar.setText(self.draw.hp_bar.text() + type(character).__name__ + " : " + str(character.hp) + ", ")
        self.draw.hp_bar.setText(self.draw.hp_bar.text() + "player damage : " + str(self.player.damage) + ", ")
        self.draw.hp_bar.setText(self.draw.hp_bar.text() + "player arm : " + str(self.player.arm) + ", ")
        for s in self.player.status:
            self.draw.hp_bar.setText(self.draw.hp_bar.text() + type(s).__name__ + " : " + str(s.duration) + ", ")"""

    def next_level(self):
        self.stage_level += 1
        self.player.position, self.staircase.position, character_list, object_list\
            = self.map.generate_map(self.stage_level)
        self.character_list = [self.player] + character_list
        if self.stage_level == 3:
            self.object_list = []
            self.character_list += [Enemy.Pharaoh(self.staircase.position[0], self.staircase.position[1])]
        else:
            self.object_list = [self.staircase]
        self.object_list += object_list

    def process_eagle_eye(self):
        is_eagle_eye = False
        for s in self.player.status:
            if type(s) == Status.EagleEye:
                self.draw.view.multiplier = 17 / 11
                is_eagle_eye = True
                break
        if is_eagle_eye is False:
            self.draw.view.multiplier = 1.0

    def process_turn(self):
        print(self.player.position)

        for character in self.character_list:
            if isinstance(character, Enemy.Enemy):
                character.behavior(self)
                character.process_status()

        temp_obj_list = []
        for obj in self.object_list:
            if obj.state != ObjectState.REMOVED:
                temp_obj_list += [obj]
        self.object_list = temp_obj_list

        temp_character_list = []
        for character in self.character_list:
            if character.state != ObjectState.REMOVED:
                temp_character_list += [character]
            elif isinstance(character, Enemy.Enemy):
                exp, dropped_item = character.when_died()
                self.player.get_exp(exp)
                if dropped_item is not None:
                    self.object_list += [dropped_item]
        self.character_list = temp_character_list

        self.map.set_object_map(self.object_list)
        self.map.set_character_map(self.character_list)
        self.process_eagle_eye()

    def update_animation(self):
        while not self.ended:
            for obj in self.character_list:
                obj.increase_index()
            sleep(self.animation_update_time)

    def paintEvent(self, event):
        self.draw_all()

    def keyPressEvent(self, event):
        if self.player.state == ObjectState.REMOVED:
            return

        if event.key() == Qt.Key_Right:
            self.player.move(1, 0, self)
            self.player.process_status()
            self.process_turn()
        if event.key() == Qt.Key_Left:
            self.player.move(-1, 0, self)
            self.player.process_status()
            self.process_turn()
        if event.key() == Qt.Key_Up:
            self.player.move(0, -1, self)
            self.player.process_status()
            self.process_turn()
        if event.key() == Qt.Key_Down:
            self.player.move(0, 1, self)
            self.player.process_status()
            self.process_turn()
        if event.key() == Qt.Key_Space:
            self.player.process_status()
            self.process_turn()

    def mousePressEvent(self, event):
        self.inventory.use_item(event.x(), event.y(), self.player)
        print(event.x(), event.y())
        self.inventory.process_removed_item()
        self.process_eagle_eye()

    def closeEvent(self, event):
        self.ended = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())
