import random

from Tile import TilesEnum, TileImageList, TileSolidState
from numpy import array
from CellularAutomata import cellular_automata
import Enemy
import Potion
from DroppedItem import DroppedItem


class Map:
    def __init__(self):
        self.__map = None
        self.__character_map = None
        self.__object_map = None
        self.__level = 1

    # this method for test
    def __sample_map_generate(self):
        self.__map = array([[TilesEnum.WALL.value] * 30] * 30)
        for i in range(30):
            self.__map[i][15] = TilesEnum.TILE.value
            self.__map[15][i] = TilesEnum.TILE.value
        for i in range(5):
            for j in range(5):
                self.__map[i + 13][j + 13] = TilesEnum.TILE.value

        for i in range(3):
            for j in range(3):
                self.__map[i + 14][j + 14] = TilesEnum.GROUND.value

        for i in range(30):
            for j in range(30):
                if 3 < i < 26 and 3 < j < 26:
                    continue
                self.__map[i][j] = TilesEnum.WALL.value

    def place_object(self, level):
        up, down = None, None
        for y in range(self.height):
            for x in range(self.width):
                if not TileSolidState[self.__map[x][y]]:
                    up = (x, y)
                    break

        for y in reversed(range(self.height)):
            for x in range(self.width):
                if not TileSolidState[self.__map[x][y]]:
                    down = (x, y)
                    break

        r = random.randint(0, 1)
        staircase, player = [up, down][r], [up, down][1 - r]

        count = 0
        monster_list = []

        while count < 15:
            x = random.randint(0, len(self.map) - 1)
            y = random.randint(0, len(self.map) - 1)
            if not TileSolidState[self.__map[x][y]] and self.__character_map[x][y] is None:
                if level == 1:
                    monster_list += [random.choice([Enemy.Slime(x, y), Enemy.Bird(x, y)])]
                elif level == 2:
                    monster_list += [random.choice([Enemy.Slime(x, y), Enemy.Goblin(x, y), Enemy.Bird(x, y)])]
                elif level == 3:
                    monster_list += [random.choice([Enemy.Goblin(x, y), Enemy.Mummy(x, y)])]
                else:
                    monster_list += [random.choice([Enemy.Slime(x, y), Enemy.Goblin(x, y), Enemy.Bird(x, y)])]
                self.__character_map[x][y] = monster_list[len(monster_list) - 1]
                count += 1

        count = 0
        object_list = []
        while count < 5:
            x = random.randint(0, len(self.map) - 1)
            y = random.randint(0, len(self.map) - 1)
            if not TileSolidState[self.__map[x][y]] and self.__object_map[x][y] is None:
                object_list += [DroppedItem(Potion.random_potion(), x, y)]
                self.__object_map[x][y] = object_list[len(object_list) - 1]
                count += 1
        return staircase, player, monster_list, object_list

    def generate_map(self, level):
        # self.__sample_map_generate()  # this code for test
        self.__map = cellular_automata(60)
        self.__character_map = array([[None] * len(self.__map)] * len(self.__map[0]))
        self.__object_map = array([[None] * len(self.__map)] * len(self.__map[0]))
        return self.place_object(level)

    def set_character(self, character):
        self.__character_map[character.x_pos][character.y_pos] = character

    def set_object(self, map_object):
        self.__object_map[map_object.x_pos][map_object.y_pos] = map_object

    def set_character_map(self, character_list):
        self.__character_map = array([[None] * len(self.__map)] * len(self.__map[0]))
        for character in character_list:
            self.__character_map[character.x_pos][character.y_pos] = character

    def set_object_map(self, object_list):
        self.__object_map = array([[None] * len(self.__map)] * len(self.__map[0]))
        for current_object in object_list:
            self.__object_map[current_object.x_pos][current_object.y_pos] = current_object

    def __getitem__(self, item):
        return self.__map[item]

    @property
    def map(self):
        return self.__map

    @map.setter
    def map(self, new_map):
        self.__map = new_map

    @property
    def character_map(self):
        return self.__character_map

    @property
    def object_map(self):
        return self.__object_map

    @property
    def level(self):
        return self.__level

    @property
    def width(self):
        return len(self.map)

    @property
    def height(self):
        return len(self.map[0])


if __name__ == "__main__":
    M = Map()
    print(M.map)
    print(M.character_map)
    print(M.object_map)

