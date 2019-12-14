from abc import abstractmethod

from Object import Object


class Structure(Object):
    @abstractmethod
    def touch_event(self, game, obj):
        pass


class Staircase(Structure):
    def __init__(self, x_pos, y_pos):
        super().__init__("image/staircase.png", x_pos, y_pos)

    def touch_event(self, game, obj):
        game.next_level()
