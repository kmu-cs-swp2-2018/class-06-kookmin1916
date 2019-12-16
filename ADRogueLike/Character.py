from abc import abstractmethod

from Object import Object, ObjectState
from Tile import TileSolidState
from Status import StatusState
import Status
from Structure import Structure
from Equipment import Weapon, Armor
from DroppedItem import DroppedItem


class Character(Object):
    def __init__(self, image, x_pos, y_pos, stat_hp, stat_str, stat_arm, weapon=None, armor=None):
        super().__init__(image, x_pos, y_pos)

        self.__stat_hp = stat_hp
        self.__hp = stat_hp
        self.__stat_str = stat_str
        self.__stat_arm = stat_arm
        self.__weapon = weapon
        self.__armor = armor

        self.__is_movable = True
        self.__damage_multiplier = 1.0
        self.__arm_multiplier = 1.0
        self.__status = []
        print(type(self))

    def __del__(self):
        print(type(self).__name__, "is died")

    def add_status(self, status):
        for s in self.__status:
            if type(s) == type(status):
                if s.duration < status.duration:
                    s.duration = status.duration
                return False
        self.__status += [status]
        status.effect(self)
        return True

    def process_status(self):
        self.__damage_multiplier = 1.0
        self.__arm_multiplier = 1.0
        for s in self.__status:
            s.process_status(self)

        temp_status = []
        for s in self.__status:
            if s.state != StatusState.REMOVED:
                temp_status += [s]
        self.__status = temp_status

    def move(self, dx, dy, game):
        if not self.__is_movable:
            self.__is_movable = True
            return False

        current_map = game.map
        character_list = game.character_list
        object_list = game.object_list

        x_pos = self.x_pos + dx
        y_pos = self.y_pos + dy

        if TileSolidState[current_map[x_pos][y_pos]]:
            return False
        for obj in object_list + character_list:
            if (x_pos, y_pos) == obj.position:
                if type(obj) != DroppedItem:
                    if self.is_enemy(obj):
                        obj.get_damage(self.damage)
                    elif self.is_interactive_structure(obj):
                        obj.touch_event(game, self)
                    return False

        self.position = x_pos, y_pos
        return True

    def get_damage(self, damage, penetration=0.0):
        self.__hp -= max(int(damage - self.arm * (1.0 - penetration)), 1)
        if self.__hp <= 0:
            self.die()

    @abstractmethod
    def is_enemy(self, obj):
        pass

    @abstractmethod
    def is_interactive_structure(self, obj):
        pass

    def heal(self, amount):
        self.__hp = min(self.__hp + amount, self.__stat_hp)

    def die(self):
        self.state = ObjectState.REMOVED
        self._when_died()

    def _when_died(self):
        pass

    def multiply_damage(self, multiplier):
        self.__damage_multiplier *= multiplier

    def multiply_arm(self, multiplier):
        self.__arm_multiplier *= multiplier

    def set_weapon(self, weapon):
        last = self.__weapon
        self.__weapon = weapon
        return last

    def set_armor(self, armor):
        last = self.__armor
        self.__armor = armor
        return last

    @property
    def stat_hp(self):
        return self.__stat_hp

    @property
    def stat_str(self):
        return self.__stat_str

    @property
    def stat_arm(self):
        return self.__stat_arm

    @stat_hp.setter
    def stat_hp(self, stat_hp):
        if stat_hp <= 0:
            raise
        self.__stat_hp = stat_hp

    @stat_str.setter
    def stat_str(self, stat_str):
        if stat_str < 0:
            raise
        self.__stat_str = stat_str

    @stat_arm.setter
    def stat_arm(self, stat_arm):
        if stat_arm < 0:
            raise
        self.__stat_arm = stat_arm

    @property
    def hp(self):
        return self.__hp

    @property
    def damage(self):
        if self.__weapon is None:
            return self.__stat_str * self.__damage_multiplier
        return (self.__stat_str + self.__weapon.damage) * self.__damage_multiplier

    @property
    def arm(self):
        if self.__armor is None:
            return self.__stat_arm * self.__arm_multiplier
        return (self.__stat_arm + self.__armor.arm) * self.__arm_multiplier

    @property
    def status(self):
        return self.__status

    @property
    def weapon(self):
        return self.__weapon

    @property
    def armor(self):
        return self.__armor

    @property
    def is_movable(self):
        return self.__is_movable

    @is_movable.setter
    def is_movable(self, is_movable):
        if not isinstance(is_movable, bool):
            raise
        self.__is_movable = is_movable


if __name__ == "__main__":
    character = Character("image/player.png", 52, 52, 20, 5, 4)
