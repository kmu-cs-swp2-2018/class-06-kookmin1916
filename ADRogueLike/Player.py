from Character import Character
import Status
import Equipment
from Enemy import Enemy
import Structure
from DroppedItem import DroppedItem
from Object import Object, ObjectState


class Player(Character):
    def __init__(self, image, x_pos, y_pos, stat_hp, stat_str, stat_arm):
        super().__init__(image, x_pos, y_pos, stat_hp, stat_str, stat_arm)

        self.__max_exp = 20
        self.__exp = 0
        self.__level = 1
        # self.add_status(Status.Poison(5))
        # self.add_status(Status.Weakness(8))
        # self.add_status(Status.Paralyze(10))
        # self.add_status(Status.Vulnerable(10))
        # self.add_status(Status.EagleEye(5))

    def is_enemy(self, obj):
        if isinstance(obj, Enemy):
            return True
        return False

    def is_interactive_structure(self, obj):
        if isinstance(obj, Structure.Structure):
            return True
        return False

    def get_exp(self, exp):
        if exp < 0:
            raise
        self.__exp += exp
        while self.__exp >= self.__max_exp:
            self.__level += 1
            self.__exp -= self.__max_exp
            self.__max_exp += 10
            self.stat_hp += 6
            self.stat_str += 2
            self.stat_arm += 0.5
            self.heal(self.stat_hp)

    def move(self, dx, dy, game):
        ret = super().move(dx, dy, game)
        dropped_item = game.map.object_map[self.x_pos][self.y_pos]
        if type(dropped_item) == DroppedItem:
            if game.inventory.add_item(dropped_item.item):
                dropped_item.state = ObjectState.REMOVED

    @property
    def level(self):
        return self.__level

    @property
    def exp(self):
        return self.__exp

    @property
    def max_exp(self):
        return self.__max_exp
