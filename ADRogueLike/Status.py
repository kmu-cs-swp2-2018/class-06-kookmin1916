import random
from enum import Enum
from abc import abstractmethod


class StatusList(Enum):
    POISON = 0
    SLEEP = 1
    STUN = 2
    PARALYZE = 3
    FREEZE = 4
    WEAKNESS = 5
    VULNERABLE = 6
    BLEEDING = 7


class StatusState(Enum):
    EXIST = 0
    REMOVED = 1


class Status:
    def __init__(self, duration):
        self.__duration = duration
        self.__state = StatusState.EXIST

    def process_status(self, character):
        self.effect(character)
        self.__duration -= 1
        if self.__duration <= 0:
            self.__state = StatusState.REMOVED

    @abstractmethod
    def effect(self, character):
        pass

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, duration):
        self.__duration = duration

    @property
    def state(self):
        return self.__state


class Poison(Status):
    def effect(self, character):
        character.get_damage(damage=1, penetration=1.0)


class Weakness(Status):
    def effect(self, character):
        character.multiply_damage(0.75)


class Vulnerable(Status):
    def effect(self, character):
        character.multiply_arm(0.5)


class Paralyze(Status):
    def effect(self, character):
        if random.randint(0, 2) == 0:
            character.is_movable = False
