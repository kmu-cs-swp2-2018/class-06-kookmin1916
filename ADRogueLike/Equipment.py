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


class WoodenSword(Weapon):
    def __init__(self):
        super().__init__("image/weapon/wooden_sword.png", 3)


class Armor(Equipment):
    def __init__(self):
        image = ""
        super().__init__(image)
        self.__arm = 0

    @property
    def arm(self):
        return self.__arm
