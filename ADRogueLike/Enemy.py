from abc import abstractmethod
import random

from Character import Character
import Player


class Enemy(Character):
    def __init__(self, image, x_pos, y_pos, stat_hp, stat_str, stat_arm):
        super().__init__(image, x_pos, y_pos, stat_hp, stat_str, stat_arm)

    @abstractmethod
    def behavior(self, game):
        pass

    @abstractmethod
    def __drop_items(self):
        pass

    def is_enemy(self, obj):
        if isinstance(obj, Player.Player):
            return True
        return False

    def is_interactive_structure(self, obj):
        return False

    def _when_died(self):
        self.__drop_items()


class Slime(Enemy):
    def __init__(self, x_pos, y_pos):
        super().__init__(["image/slime/slime0.png", "image/slime/slime1.png",
                          "image/slime/slime2.png", "image/slime/slime3.png",
                          "image/slime/slime2.png", "image/slime/slime1.png"]
                         , x_pos, y_pos, stat_hp=10, stat_str=3, stat_arm=1)

    def behavior(self, game):
        direction = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        selected = random.randint(0, len(direction) - 1)
        self.move(direction[selected][0], direction[selected][1], game)

    def __drop_items(self):
        pass

    def _when_died(self):
        super()._when_died()

        # TODO : Split to Small Slimes
