from abc import abstractmethod
import random

from Character import Character
import Player
from DroppedItem import DroppedItem
import Potion
from AStar import a_star
import Item


class Enemy(Character):
    def __init__(self, image, x_pos, y_pos, stat_hp, stat_str, stat_arm, exp, sight):
        super().__init__(image, x_pos, y_pos, stat_hp, stat_str, stat_arm)
        self.__exp = exp
        self.__sight = sight

    def behavior(self, game):
        result_direction = None
        if abs(self.x_pos - game.player.x_pos) <= self.__sight and abs(self.y_pos - game.player.y_pos) <= self.__sight:
            result_direction = a_star(game.map, self.x_pos, self.y_pos, game.player.x_pos, game.player.y_pos)
        if result_direction is None:
            direction = [[0, 1], [0, -1], [1, 0], [-1, 0]]
            selected = random.randint(0, len(direction) - 1)
            self.move(direction[selected][0], direction[selected][1], game)
        else:
            self.move(result_direction[0], result_direction[1], game)

    @abstractmethod
    def __drop_items(self):
        pass

    def is_enemy(self, obj):
        if isinstance(obj, Player.Player):
            return True
        return False

    def is_interactive_structure(self, obj):
        return False

    @abstractmethod
    def when_died(self):
        pass

    @property
    def exp(self):
        return self.__exp


class Slime(Enemy):
    def __init__(self, x_pos, y_pos):
        super().__init__(["image/enemy/slime/slime%d.png" % i for i in [0, 1, 2, 3, 2]]
                         , x_pos, y_pos, stat_hp=10, stat_str=3, stat_arm=1, exp=5, sight=4)

    def __drop_items(self):
        r = random.randint(1, 100)
        item = None

        if r <= 33:
            item = Potion.random_potion()
        elif r <= 38:
            item = Item.ItemWoodenSword()
        elif r <= 41:
            item = Item.ItemIronSword()
        elif r <= 42:
            item = Item.ItemEmeraldSickle()
        elif r <= 47:
            item = Item.ItemIronArmor()

        if item is None:
            return None
        return DroppedItem(item, self.x_pos, self.y_pos)

    def when_died(self):
        return self.exp, self.__drop_items()

        # TODO : Split to Small Slimes


class Goblin(Enemy):
    def __init__(self, x_pos, y_pos):
        super().__init__("image/enemy/goblin.png", x_pos, y_pos, stat_hp=15, stat_str=6, stat_arm=0, exp=8, sight=5)

    def __drop_items(self):
        r = random.randint(1, 100)
        item = None

        if r <= 33:
            item = Potion.random_potion()
        elif r <= 38:
            item = Item.ItemIronSword()
        elif r <= 41:
            item = Item.ItemEmeraldSickle()
        elif r <= 42:
            item = Item.ItemWaterSword()
        elif r <= 45:
            item = Item.ItemIronArmor()
        elif r <= 48:
            item = Item.ItemGoldArmor()

        if item is None:
            return None
        return DroppedItem(item, self.x_pos, self.y_pos)

    def when_died(self):
        return self.exp, self.__drop_items()


class Bird(Enemy):
    def __init__(self, x_pos, y_pos):
        super().__init__(["image/enemy/bird/bird%d.png" % i for i in [0, 1]]
                         , x_pos, y_pos, stat_hp=8, stat_str=4, stat_arm=0, exp=3, sight=8)

    def __drop_items(self):
        r = random.randint(1, 100)
        item = None

        if r <= 33:
            item = Potion.random_potion()
        elif r <= 38:
            item = Item.ItemBrokenSword()
        elif r <= 41:
            item = Item.ItemWoodenSword()
        elif r <= 42:
            item = Item.ItemIronSword()
        elif r <= 45:
            item = Item.ItemIronArmor()

        if item is None:
            return None
        return DroppedItem(item, self.x_pos, self.y_pos)

    def when_died(self):
        return self.exp, self.__drop_items()


class Mummy(Enemy):
    def __init__(self, x_pos, y_pos):
        super().__init__("image/enemy/mummy", x_pos, y_pos, stat_hp=20, stat_str=8, stat_arm=2, exp=13, sight=6)

    def __drop_items(self):
        r = random.randint(1, 100)
        item = None

        if r <= 33:
            item = Potion.random_potion()
        elif r <= 38:
            item = Item.ItemEmeraldSickle()
        elif r <= 41:
            item = Item.ItemWaterSword()
        elif r <= 46:
            item = Item.ItemGoldArmor()

        if item is None:
            return None
        return DroppedItem(item, self.x_pos, self.y_pos)

    def when_died(self):
        return self.exp, self.__drop_items()


class Pharaoh(Enemy):
    def __init__(self, x_pos, y_pos):
        super().__init__(["image/enemy/pharaoh/pharaoh%d.png" % i for i in range(1, 21)]
                         , x_pos, y_pos, stat_hp=100, stat_str=13, stat_arm=4, exp=100, sight=8)

    def __drop_items(self):
        r = random.randint(1, 100)
        item = None

        if r <= 100:
            item = Item.ItemCrown()

        if item is None:
            return None
        return DroppedItem(item, self.x_pos, self.y_pos)

    def when_died(self):
        return self.exp, self.__drop_items()
