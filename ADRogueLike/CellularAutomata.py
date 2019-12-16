import random
import copy
from numpy import array
import queue

from Tile import TilesEnum


def check_wall(current_map):
    map_size = len(current_map)
    next_map = array([[0] * map_size] * map_size)
    for x in range(len(current_map)):
        for y in range(len(current_map[x])):
            count = 0
            for i in [(0, 1), (1, 1), (-1, 1), (0, -1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 0)]:
                temp_x = x - i[0]
                temp_y = y - i[1]
                if temp_x < 0 or temp_y < 0 or temp_x >= map_size or temp_y >= map_size:
                    count += 1
                elif current_map[temp_x][temp_y] == 1:
                    count += 1
            if count >= 5:
                next_map[x][y] = 1
            else:
                next_map[x][y] = 0
    return next_map


def cellular_automata(map_size):
    current_map = array([[0] * map_size] * map_size)
    for i in range(len(current_map)):
        for j in range(len(current_map[i])):
            if random.randint(0, 18) > 9:
                current_map[i][j] = 1
    for k in range(4):
        current_map = check_wall(current_map)

    # Cellular Automata End

    check_map = copy.deepcopy(current_map)
    node_list = []
    node_queue = queue.Queue()
    big = 0
    for x in range(len(check_map)):
        for y in range(len(check_map[x])):
            if check_map[x][y] == 0:
                temp_big = 0
                node_queue.put([x, y])
                while node_queue.qsize() != 0:
                    pos = node_queue.get()
                    check_map[pos[0]][pos[1]] = 1
                    temp_big += 1
                    for i in [(0, 1), (1, 1), (-1, 1), (0, -1), (1, -1), (-1, -1), (1, 0), (-1, 0)]:
                        if pos[0] - i[0] < 0 or pos[0] - i[0] >= map_size:
                            continue
                        elif pos[1] - i[1] < 0 or pos[1] - i[1] >= map_size:
                            continue
                        elif check_map[pos[0] - i[0]][pos[1] - i[1]] == 1:
                            continue
                        check_map[pos[0] - i[0]][pos[1] - i[1]] = 1
                        node_queue.put([pos[0] - i[0], pos[1] - i[1]])
                if big < temp_big: big = temp_big
                node_list += [(x, y, temp_big)]
    temp_big = 0
    for i in node_list:
        if i[2] != big:
            node_queue = queue.Queue()
            node_queue.put([i[0], i[1]])
            while node_queue.qsize() != 0:
                pos = node_queue.get()
                current_map[pos[0]][pos[1]] = 1
                temp_big += 1
                for i in [(0, 1), (1, 1), (-1, 1), (0, -1), (1, -1), (-1, -1), (1, 0), (-1, 0)]:
                    if pos[0] - i[0] < 0 or pos[0] - i[0] >= map_size:
                        continue
                    elif pos[1] - i[1] < 0 or pos[1] - i[1] >= map_size:
                        continue
                    elif current_map[pos[0] - i[0]][pos[1] - i[1]] == 1:
                        continue
                    current_map[pos[0] - i[0]][pos[1] - i[1]] = 1
                    node_queue.put([pos[0] - i[0], pos[1] - i[1]])
    ret = array([[TilesEnum.WALL.value] * (map_size + 20)] * (map_size + 20))
    for i in range(map_size):
        for j in range(map_size):
            if current_map[i][j] == 0:
                ret[i + 10][j + 10] = TilesEnum.TILE.value
            else:
                ret[i + 10][j + 10] = TilesEnum.WALL.value

    return ret


if __name__ == "__main__":
    A = cellular_automata(50)
    for i in A:
        for j in i:
            print(j, end='')
        print()
