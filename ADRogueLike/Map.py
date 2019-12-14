from Tile import TilesEnum, TileImageList
from numpy import array


class Map:
    def __init__(self):
        self.__map = None
        self.__character_map = None
        self.__object_map = None
        self.__level = 1
        self.generate_map()

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
                if 2 < i < 27 and 2 < j < 27:
                    continue
                self.__map[i][j] = TilesEnum.WALL.value
        self.__character_map = array([[None] * len(self.__map)] * len(self.__map[0]))
        self.__object_map = array([[None] * len(self.__map)] * len(self.__map[0]))

    def generate_map(self):
        self.__sample_map_generate()  # this code for test
        # TODO :

    def set_character(self, character):
        self.__character_map[character.x_pos][character.y_pos] = character

    def set_object(self, map_object):
        self.__object_map[map_object.x_pos][map_object.y_pos] = map_object

    def __getitem__(self, item):
        return self.__map[item]

    @property
    def map(self):
        return self.__map

    @property
    def character_map(self):
        return self.__character_map

    @property
    def object_map(self):
        return self.__object_map

    @property
    def level(self):
        return self.__level


if __name__ == "__main__":
    M = Map()
    print(M.map)
    print(M.character_map)
    print(M.object_map)

