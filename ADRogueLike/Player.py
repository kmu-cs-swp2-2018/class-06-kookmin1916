from Character import Character
from Map import Map
import Status
import Equipment
from Enemy import Enemy
import Structure

class Player(Character):
    def __init__(self, image, x_pos, y_pos, stat_hp, stat_str, stat_arm):
        super().__init__(image, x_pos, y_pos, stat_hp, stat_str, stat_arm)

        self.add_status(Status.Poison(5))
        self.add_status(Status.Weakness(8))
        self.add_status(Status.Paralyze(10))
        self.add_status(Status.Vulnerable(10))
        self.set_weapon(Equipment.WoodenSword())

    def is_enemy(self, obj):
        if isinstance(obj, Enemy):
            return True
        return False

    def is_interactive_structure(self, obj):
        if isinstance(obj, Structure.Structure):
            return True
        return False

    def move(self, dx, dy, game):
        ret = super().move(dx, dy, game)

