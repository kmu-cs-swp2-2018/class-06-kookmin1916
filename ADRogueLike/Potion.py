from abc import abstractmethod
import random

from Item import Item, ItemState
import Status


class Potion(Item):
    def __init__(self, image):
        super().__init__(image)

    def use_item(self, player):
        self.effect(player)
        self.state = ItemState.REMOVED.value

    @abstractmethod
    def effect(self, player):
        pass


class HealingPotion(Potion):
    def effect(self, player):
        player.heal(int(player.stat_hp / 2))


class PotionOfStrength(Potion):
    def effect(self, player):
        player.add_status(Status.Strength(10))


class PotionOfToughness(Potion):
    def effect(self, player):
        player.add_status(Status.Toughness(10))


class PoisonPotion(Potion):
    def effect(self, player):
        player.add_status(Status.Poison(8))


class PotionOfWeakness(Potion):
    def effect(self, player):
        player.add_status(Status.Weakness(8))


class ParalyzePotion(Potion):
    def effect(self, player):
        player.add_status(Status.Paralyze(8))


class PotionOfDeath(Potion):
    def effect(self, player):
        player.get_damage(int(player.stat_hp * 0.25), 1.0)


class PotionOfEagleEye(Potion):
    def effect(self, player):
        player.add_status(Status.EagleEye(15))


def shuffle_potion_list():
    potion_list = [HealingPotion, PotionOfStrength, PotionOfToughness, PoisonPotion,
                   PotionOfEagleEye, ParalyzePotion, PotionOfDeath]
    potion_image_list = ["image/potion/%s_Potion.png" % color for color in
                         ["Blue", "Cyan", "Green", "Orange", "Purple", "Red", "Yellow"]]
    number_of_potion = 7

    random.shuffle(potion_list)
    result = [(potion_list[i], potion_image_list[i]) for i in range(number_of_potion)]
    return result


current_potion_list = shuffle_potion_list()


def random_potion():
    r = random.randint(0, len(current_potion_list) - 1)
    return current_potion_list[r][0](current_potion_list[r][1])
