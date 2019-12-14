from abc import abstractmethod

from Item import Item


class Potion(Item):
    @abstractmethod
    def effect(self):
        pass
