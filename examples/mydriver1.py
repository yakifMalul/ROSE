"""
This driver does not do any action.
"""
from rose.common import obstacles, actions  # NOQA

driver_name = "Amit"
right_balance = 0
action_list = list()
cnt = 0


def calculate_right_balance(x1, x2):
    global right_balance
    if x1 > x2:
        return -1 + right_balance
    if x1 < x2:
        return 1 + right_balance
    return right_balance


def row(world, right_balance, y):
    res = list()
    x = world.car.x

    if right_balance > 0:
        res = [(x - 2, y - 1), (x - 1, y - 1), (x, y - 1)]
    elif right_balance == 0:
        res = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]
    elif right_balance < 0:
        res = [(x, y - 1), (x + 1, y - 1), (x - 2, y - 1)]

    return res


def pos_to_score(world, pos):
    temp = list()
    res = list()
    for item in pos:
        temp.append(world.get(item))
    for item in temp:
        if item == obstacles.PENGUIN:
            score = 10
        elif item == obstacles.CRACK:
            score = 5
        elif item == obstacles.WATER:
            score = 4
        elif item == obstacles.BARRIER:
            score = -10
        elif item == obstacles.BIKE:
            score = -10
        elif item == obstacles.TRASH:
            score = -10
        else:
            score = 0
        res.append(score)
    print(res)

    return res


def world_to_score_board(world, right_balance):
    score_board = list()
    y = world.car.y

    for i in range(3, 0, -1):
        score_board.append(pos_to_score(world, row(world, right_balance, y-i)))
    return score_board


def get_connected(right_balance, y):
    res = list()
    if right_balance == -1:
        res.append((0, y - 1))
        res.append((1, y - 1))
    elif right_balance == 0:
        res.append((0, y - 1))
        res.append((1, y - 1))
        res.append((2, y - 1))
    elif right_balance == 1:
        res.append((1, y - 1))
        res.append((2, y - 1))
    return res


def best_way(world, score_board, right_balance):
    x = world.car.x
    y = world.car.y

    ways = dict()
    score_def = 0
    score_def += score_board[y][x]
    for i in get_connected(right_balance, y):
        score_i = 0
        if i[0] == x:
            score_i = score_board[i[1]][i[0]]
        for j in get_connected(calculate_right_balance(x, i[0]), i[1]):
            score_j = 0
            if j[0] == i[0]:
                score_j = score_board[j[1]][j[0]]
            for k in get_connected(calculate_right_balance(x, j[0]), j[1]):
                score_k = 0
                if k[0] == j[0]:
                    score_k = score_board[k[1]][k[0]]
                total_score = score_def + score_i + score_j + score_k
                ways[total_score] = [(x, y), i, j, k]
    for i in ways.keys():
        print(str(i) + ": ", end="")
        print(ways[i])

    big = list(ways)[0]
    for key in ways.keys():
        if big < key:
            big = key

    return ways[big]


def way_to_actions(way):
    res = list()
    for i in range(len(way) - 1):
        x_0 = way[i][0]
        x_1 = way[i+1][0]

        if x_1 - x_0 > 0:
            # right
            res.append(actions.RIGHT)
        elif x_1 - x_0 < 0:
            # left
            res.append(actions.LEFT)
        else:
            # mid
            res.append(actions.LEFT)
    return res


def drive(world):
    global right_balance, action_list, cnt
    res = actions.NONE

    x = world.car.x
    y = world.car.y
    obstacle = world.get((x, y - 1))
    if world.get((x, y-1)) == obstacles.PENGUIN:
        res = actions.PICKUP
    elif obstacle == obstacles.WATER:
        res = actions.BRAKE
    elif obstacle == obstacles.CRACK:
        res = actions.JUMP
    else:
        if cnt >= 3:
            cnt = 0
        if cnt == 0:
            score_board = world_to_score_board(world, right_balance)
            action_list = way_to_actions(best_way(world, score_board, right_balance))
            res = action_list[0]
    #     elif 0 < cnt < 3:
    #         res = action_list[cnt]
    cnt += 1
    # if res == actions.RIGHT:
    #     right_balance += 1
    # elif res == actions.LEFT:
    #     right_balance -= 1
    return res
