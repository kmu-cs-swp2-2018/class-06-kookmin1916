# not use

from PyQt5.QtCore import Qt
import Game
import Game.game
# from Game import game


class Keyboard:
    def __init__(self):
        pass

    @staticmethod
    def keyboard_press_event(event):
        if event.key() == Qt.Key_Right:
            game.player.move(1, 0)
            game.draw.view.position = game.player.position
        if event.key() == Qt.Key_Left:
            game.player.move(1, 0)
            game.draw.view.position = game.player.position
        if event.key() == Qt.Key_Up:
            game.player.move(1, 0)
            game.draw.view.position = game.player.position
        if event.key() == Qt.Key_Down:
            game.player.move(1, 0)
            game.draw.view.position = game.player.position
