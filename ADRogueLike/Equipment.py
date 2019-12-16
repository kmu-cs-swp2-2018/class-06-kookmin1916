from PyQt5.QtGui import QImage


class Equipment:
    def __init__(self, image):
        self.__image = QImage(image)

    @property
    def image(self):
        return self.__image


class Weapon(Equipment):
    def __init__(self, image, damage):
        super().__init__(image)
        self.__damage = damage

    @property
    def damage(self):
        return self.__damage


class BrokenSword(Weapon):
    def __init__(self):
        super().__init__("image/weapon/broken_sword.png", 2)


class WoodenSword(Weapon):
    def __init__(self):
        super().__init__("image/weapon/wooden_sword.png", 3)


class IronSword(Weapon):
    def __init__(self):
        super().__init__("image/weapon/iron_sword.png", 4)


class EmeraldSickle(Weapon):
    def __init__(self):
        super().__init__("image/weapon/emerald_sickle.png", 6)


class WaterSword(Weapon):
    def __init__(self):
        super().__init__("image/weapon/water_sword.png", 8)


class Armor(Equipment):
    def __init__(self, image, arm):
        super().__init__(image)
        self.__arm = arm

    @property
    def arm(self):
        return self.__arm


class IronArmor(Armor):
    def __init__(self):
        super().__init__("image/armor/iron_armor.png", 2)


class GoldArmor(Armor):
    def __init__(self):
        super().__init__("image/armor/gold_armor.png", 3)
