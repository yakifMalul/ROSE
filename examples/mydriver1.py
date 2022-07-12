"""
This driver does not do any action.
"""
from rose.common import obstacles, actions  # NOQA

driver_name = "Amit"
action_list = list()
cnt = 0
x1, x2, x3 = 0, 0, 0
got_x_values = False
num_of_steps = 5


def get_x_values(x):
    global got_x_values, x1, x2, x3
    if not got_x_values:
        x1 = x - 1
        x2 = x
        x3 = x + 1
        got_x_values = True


def row(y):
    global x1, x2, x3
    res = [(x1, y - 1), (x2, y - 1), (x3, y - 1)]
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


def world_to_score_board(world):
    global num_of_steps
    score_board = list()
    y = world.car.y

    for i in range(num_of_steps, 0, -1):
        score_board.append(pos_to_score(world, row(y-i)))
    return score_board


def get_connected(x, y):
    global x1, x2, x3
    res = list()
    if x == x1 or x == 0:
        res.append((0, y - 1))
        res.append((1, y - 1))
    elif x == x2 or x == 1:
        res.append((0, y - 1))
        res.append((1, y - 1))
        res.append((2, y - 1))
    elif x == x3 or x == 2:
        res.append((1, y - 1))
        res.append((2, y - 1))
    return res


def best_way(world, score_board):
    y = len(score_board) - 1
    x = world.car.x

    if x == x3:
        x = 2
    elif x == x2:
        x = 1
    elif x == x1:
        x = 0

    ways = {0: [(1, 3), (1, 2), (1, 0), (1, 0)]}
    score_def = score_board[y][x]
    for i in get_connected(x, y):
        score_i = 0
        if i[0] == x:
            score_i = score_board[i[1]][i[0]]
        for j in get_connected(i[0], i[1]):
            score_j = 0
            if j[0] == i[0]:
                score_j = score_board[j[1]][j[0]]
            for k in get_connected(j[0], j[1]):
                score_k = 0
                if k[0] == j[0]:
                    score_k = score_board[k[1]][k[0]]
                for l in get_connected(k[0], k[1]):
                    score_l = 0
                    if l[0] == k[0]:
                        score_l = score_board[l[1]][l[0]]
                    total_score = score_def + score_i + score_j + score_k + score_l
                    ways[total_score] = [(x, y), i, j, k, l]
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
            res.append(actions.NONE)
    return res


def drive(world):
    global action_list, cnt, num_of_steps
    res = actions.NONE
    x = world.car.x
    y = world.car.y
    get_x_values(x)
    obstacle = world.get((x, y - 1))
    if world.get((x, y-1)) == obstacles.PENGUIN:
        res = actions.PICKUP
    elif obstacle == obstacles.WATER:
        res = actions.BRAKE
    elif obstacle == obstacles.CRACK:
        res = actions.JUMP
    else:
        if cnt >= num_of_steps - 1:
            cnt = 0
        if cnt == 0:
            score_board = world_to_score_board(world)
            action_list = way_to_actions(best_way(world, score_board))
            res = action_list[0]
        elif 0 < cnt < num_of_steps - 1:
            print(cnt)
            res = action_list[cnt - 1]
    cnt += 1

    return res
