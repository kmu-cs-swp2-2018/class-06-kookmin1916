from abc import abstractmethod
from PyQt5.QtGui import QImage
from enum import Enum

import Equipment


class ItemState(Enum):
    EXIST = 0
    REMOVED = 1


class Item:
    def __init__(self, image):
        self._image = QImage(image)
        self.__state = ItemState.EXIST.value

    @abstractmethod
    def use_item(self, player):
        pass

    @property
    def image(self):
        return self._image

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state


class ItemCrown(Item):
    def __init__(self):
        super().__init__('image/crown.png')

    def use_item(self, player):
        pass


class ItemIronArmor(Item):
    def __init__(self):
        super().__init__('image/armor/iron_armor.png')

    def use_item(self, player):
        player.set_armor(Equipment.IronArmor())


class ItemGoldArmor(Item):
    def __init__(self):
        super().__init__('image/armor/gold_armor.png')

    def use_item(self, player):
        player.set_armor(Equipment.GoldArmor())


class ItemBrokenSword(Item):
    def __init__(self):
        super().__init__('image/weapon/broken_sword.png')

    def use_item(self, player):
        player.set_weapon(Equipment.BrokenSword())


class ItemWoodenSword(Item):
    def __init__(self):
        super().__init__('image/weapon/wooden_sword.png')

    def use_item(self, player):
        player.set_weapon(Equipment.WoodenSword())


class ItemIronSword(Item):
    def __init__(self):
        super().__init__('image/weapon/iron_sword.png')

    def use_item(self, player):
        player.set_weapon(Equipment.IronSword())


class ItemEmeraldSickle(Item):
    def __init__(self):
        super().__init__('image/weapon/emerald_sickle.png')

    def use_item(self, player):
        player.set_weapon(Equipment.EmeraldSickle())


class ItemWaterSword(Item):
    def __init__(self):
        super().__init__('image/weapon/water_sword.png')

    def use_item(self, player):
        player.set_weapon(Equipment.WaterSword())
