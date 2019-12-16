import queue
from numpy import array
from Map import Map
from Tile import TileSolidState, TilesEnum
from enum import Enum


class DirectionsEnum(Enum):
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3


def check_index_out(map_size, x, y):
    if x < 0 or x >= map_size:
        return False
    if y < 0 or y >= map_size:
        return False
    return True


def a_star(current_map, player_x, player_y, finish_x, finish_y):
    direction = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    map_size = current_map.width
    weight_map = array([[[-1, 1000]] * map_size] * map_size)  # [0] H [1] G

    distance = abs(player_x - finish_x) + abs(player_y - finish_y)

    weight_map[player_x][player_y] = [distance, 0]

    Q = queue.Queue()
    Q.put((player_x, player_y))

    while Q.qsize() > 0:
        qsize = Q.qsize()
        all_way = []
        best_way = 1234567890
        for i in range(qsize):
            pos = Q.get()
            walk_count = weight_map[pos[0]][pos[1]][1]
            for j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                x = pos[0] + j[0]
                y = pos[1] + j[1]

                if check_index_out(map_size, x, y):
                    if walk_count + 1 < weight_map[x][y][1] and not TileSolidState[current_map[x][y]]:
                        dis = abs(x - finish_x) + abs(y - finish_y)
                        weight_map[x][y] = [dis, walk_count + 1]
                        all_way += [(x, y)]
                        if best_way > dis:
                            best_way = dis
        for i in all_way:
            if weight_map[i[0]][i[1]][0] == best_way:
                Q.put((i[0], i[1]))

    move = []
    back_x = finish_x
    back_y = finish_y

    cnt = 0
    while (back_x != player_x or back_y != player_y) and cnt < 1000:
        for i in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x = back_x + i[0]
            y = back_y + i[1]
            if check_index_out(map_size, x, y):
                if weight_map[x][y][1] == weight_map[back_x][back_y][1] - 1:
                    back_x = x
                    back_y = y
                    if i[0] == 0 and i[1] == 1:
                        move += [DirectionsEnum.DOWN]

                    if i[0] == 0 and i[1] == -1:
                        move += [DirectionsEnum.UP]

                    if i[0] == 1 and i[1] == 0:
                        move += [DirectionsEnum.LEFT]

                    if i[0] == -1 and i[1] == 0:
                        move += [DirectionsEnum.RIGHT]
                    break
        cnt += 1
    if len(move) == 0:
        return None
    return direction[move[len(move) - 1].value]


if __name__ == "__main__":
    test_map = Map()
    test_map.map = array([[TilesEnum.TILE.value] * 10] * 10)
    for i in range(0, 9):
        test_map[i][5] = TilesEnum.WALL.value
    print(a_star(test_map, 0, 0, 9, 9) == [1, 0])
