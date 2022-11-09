# """
# This driver does not do any action.
# """
# from rose.common import obstacles, actions  # NOQA
#
# driver_name = "Yakif"
# action_list = list()
# cnt = 0
# x1, x2, x3 = 0, 0, 0
# got_x_values = False
# num_of_steps = 5
#
#
# def get_x_values(x):
#     global got_x_values, x1, x2, x3
#     if not got_x_values:
#         x1 = x - 1
#         x2 = x
#         x3 = x + 1
#         got_x_values = True
#
#
# def row(y):
#     global x1, x2, x3
#     res = [(x1, y), (x2, y), (x3, y)]
#     return res
#
#
# def pos_to_score(world, pos):
#     temp = list()
#     res = list()
#     for item in pos:
#         temp.append(world.get(item))
#     for item in temp:
#         if item == obstacles.PENGUIN:
#             score = 10
#         elif item == obstacles.CRACK:
#             score = 5
#         elif item == obstacles.WATER:
#             score = 4
#         elif item == obstacles.BARRIER:
#             score = -10
#         elif item == obstacles.BIKE:
#             score = -10
#         elif item == obstacles.TRASH:
#             score = -10
#         else:
#             score = 0
#         res.append(score)
#     print(temp)
#     print(res)
#
#     return res
#
#
# def world_to_score_board(world):
#     global num_of_steps
#     score_board = list()
#     y = world.car.y
#
#     for i in range(num_of_steps, -1, -1):
#         score_board.append(pos_to_score(world, row(y-i)))
#     return score_board
#
#
# def get_connected(x, y):
#     global x1, x2, x3
#     res = list()
#     if x == x1 or x == 0:
#         res.append((0, y - 1))
#         res.append((1, y - 1))
#     elif x == x2 or x == 1:
#         res.append((0, y - 1))
#         res.append((1, y - 1))
#         res.append((2, y - 1))
#     elif x == x3 or x == 2:
#         res.append((1, y - 1))
#         res.append((2, y - 1))
#     return res
#
#
# def best_way(world, score_board):
#     y = len(score_board) - 1
#     x = world.car.x
#
#     if x == x3:
#         x = 2
#     elif x == x2:
#         x = 1
#     elif x == x1:
#         x = 0
#
#     ways = dict()
#     score_def = score_board[y][x]
#     for i in get_connected(x, y):
#         score_i = 0
#         if i[0] == x:
#             score_i = score_board[i[1]][i[0]]
#         elif score_board[i[1]][i[0]] != 10 and score_board[i[1]][i[0]] != 0:
#             score_i = -10
#         for j in get_connected(i[0], i[1]):
#             score_j = 0
#             if j[0] == i[0]:
#                 score_j = score_board[j[1]][j[0]]
#             elif score_board[j[1]][j[0]] != 10 and score_board[j[1]][j[0]] != 0:
#                 score_j = -10
#             for k in get_connected(j[0], j[1]):
#                 score_k = 0
#                 if k[0] == j[0]:
#                     score_k = score_board[k[1]][k[0]]
#                 elif score_board[k[1]][k[0]] != 10 and score_board[k[1]][k[0]] != 0:
#                     score_k = -10
#                 for l in get_connected(k[0], k[1]):
#                     score_l = 0
#                     if l[0] == k[0]:
#                         score_l = score_board[l[1]][l[0]]
#                     elif score_board[l[1]][l[0]] != 10 and score_board[l[1]][l[0]] != 0:
#                         score_l = -10
#                     total_score = score_def + score_i + score_j + score_k + score_l
#                     ways[total_score] = [(x, y), i, j, k, l]
#     for i in ways.keys():
#         print(str(i) + ": ", end="")
#         print(ways[i])
#
#     big = list(ways)[0]
#     for key in ways.keys():
#         if big < key:
#             big = key
#
#     return ways[big]
#
#
# def way_to_actions(way):
#     res = list()
#     for i in range(len(way) - 1):
#         x_0 = way[i][0]
#         x_1 = way[i+1][0]
#
#         if x_1 - x_0 > 0:
#             # right
#             res.append(actions.RIGHT)
#         elif x_1 - x_0 < 0:
#             # left
#             res.append(actions.LEFT)
#         else:
#             # mid
#             res.append(actions.NONE)
#     return res
#
#
# def drive(world):
#     global action_list, cnt, num_of_steps
#     res = actions.NONE
#     x = world.car.x
#     y = world.car.y
#     get_x_values(x)
#
#     if cnt >= num_of_steps - 1:
#         cnt = 0
#     if cnt == 0:
#         score_board = world_to_score_board(world)
#         action_list = way_to_actions(best_way(world, score_board))
#         # action_list.insert(0, actions.NONE)
#         print(action_list)
#         res = action_list[0]
#     elif 0 < cnt < num_of_steps - 1:
#         res = action_list[cnt]
#
#     if res == actions.NONE:
#         obstacle = world.get((x, y - 1))
#         if obstacle == obstacles.PENGUIN:
#             res = actions.PICKUP
#         elif obstacle == obstacles.WATER:
#             res = actions.BRAKE
#         elif obstacle == obstacles.CRACK:
#             res = actions.JUMP
#
#     cnt += 1
#     print(res)
#     return res



"""
This driver does not do any action.
"""
from rose.common import obstacles, actions  # NOQA
import time

driver_name = "Yakif"
world_by_score = list()
world_by_obs = list()
world_actions = list()
action_list = list()
cnt = 0
steps = 0
is_right = False
x1, x2, x3 = 0, 0, 0
ox1, ox2, ox3 = 0, 0, 0  # o stand for other
got_x_values = False
num_of_steps = 5
found_penguin = False


def log(msg):
    print(str(time.strftime("%Y-%m-%d %H:%M:%S")) + "\t" + msg)


def update_world(world, action):
    global world_by_obs, world_by_score, steps, world_actions

    world_by_obs.append(pos_to_obs(world, row(world.car.y)))
    world_by_score.append(pos_to_score(world, row(world.car.y)))
    world_actions.append(action)
    if steps == 0:
        for i in range(len(world_by_score)):
            log(str(i) + ":\t" + str(world_by_score[i]) + "\t\t" + str(world_by_obs[i]) + "\t\t" + str(world_actions[i]) + "\n")
        world_by_score = list()
        world_by_obs = list()
        world_actions = list()


def get_x_values(x):
    global is_right, got_x_values, x1, x2, x3, ox1, ox2, ox3
    if not got_x_values:
        x1 = x - 1
        x2 = x
        x3 = x + 1
        got_x_values = True
        if 0 <= x2 <= 2:
            is_right = False
            ox1, ox2, ox3 = 3, 4, 5
        elif 3 <= x2 <= 5:
            is_right = True
            ox1, ox2, ox3 = 0, 1, 2


def row(y):
    global x1, x2, x3
    res = [(x1, y), (x2, y), (x3, y)]
    return res


def other_row(y):
    global ox1, ox2, ox3
    res = [(ox1, y), (ox2, y), (ox3, y)]
    return res


def full_row(y):
    global x1, x2, x3, ox1, ox2, ox3, is_right
    if is_right:
        res = [(ox1, y), (ox2, y), (ox3, y), (x1, y), (x2, y), (x3, y)]
    else:
        res = [(x1, y), (x2, y), (x3, y), (ox1, y), (ox2, y), (ox3, y)]
    return res


def pos_to_obs(world, pos):
    res = list()
    for item in pos:
        res.append(world.get(item))
    return res


def pos_to_score(world, pos):
    res = list()
    temp = pos_to_obs(world, pos)
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

    return res


def world_to_score_board(world):
    global num_of_steps
    score_board = list()
    y = world.car.y

    for i in range(num_of_steps, -1, -1):
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


def get_full_connected(x, y):
    global x1, x2, x3, ox1, ox2, ox3, is_right
    res = list()
    if is_right:
        if x == ox1:
            res.append((0, y - 1))
            res.append((1, y - 1))
        elif x == ox2:
            res.append((0, y - 1))
            res.append((1, y - 1))
            res.append((2, y - 1))
        elif x == ox3:
            res.append((1, y - 1))
            res.append((2, y - 1))
            res.append((3, y - 1))
        elif x == x1:
            res.append((2, y - 1))
            res.append((3, y - 1))
            res.append((4, y - 1))
        elif x == x2 or x == 1:
            res.append((3, y - 1))
            res.append((4, y - 1))
            res.append((5, y - 1))
        elif x == x3 or x == 2:
            res.append((4, y - 1))
            res.append((5, y - 1))
    else:
        if x == x1:
            res.append((0, y - 1))
            res.append((1, y - 1))
        elif x == x2 or x == 1:
            res.append((0, y - 1))
            res.append((1, y - 1))
            res.append((2, y - 1))
        elif x == x3 or x == 2:
            res.append((1, y - 1))
            res.append((2, y - 1))
            res.append((3, y - 1))
        elif x == ox1:
            res.append((2, y - 1))
            res.append((3, y - 1))
            res.append((4, y - 1))
        elif x == ox2:
            res.append((3, y - 1))
            res.append((4, y - 1))
            res.append((5, y - 1))
        elif x == ox3:
            res.append((4, y - 1))
            res.append((5, y - 1))
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

    ways = dict()
    score_def = score_board[y][x]
    for i in get_connected(x, y):
        score_i = 0
        if i[0] == x:
            score_i = score_board[i[1]][i[0]]
        elif score_board[i[1]][i[0]] != 10 and score_board[i[1]][i[0]] != 0:
            score_i = -10
        for j in get_connected(i[0], i[1]):
            score_j = 0
            if j[0] == i[0]:
                score_j = score_board[j[1]][j[0]]
            elif score_board[j[1]][j[0]] != 10 and score_board[j[1]][j[0]] != 0:
                score_j = -10
            for k in get_connected(j[0], j[1]):
                score_k = 0
                if k[0] == j[0]:
                    score_k = score_board[k[1]][k[0]]
                elif score_board[k[1]][k[0]] != 10 and score_board[k[1]][k[0]] != 0:
                    score_k = -10
                for b in get_connected(k[0], k[1]):
                    score_b = 0
                    if b[0] == k[0]:
                        score_b = score_board[b[1]][b[0]]
                    elif score_board[b[1]][b[0]] != 10 and score_board[b[1]][b[0]] != 0:
                        score_b = -10
                    total_score = score_def + score_i + score_j + score_k + score_b
                    ways[total_score] = [(x, y), i, j, k, b]
                    # if is_right:
                    #     ways[total_score] = [(x, y), i, j, k, b]
                    # else:
                    #     if total_score in list(ways):
                    #         pass
                    #     else:
                    #         ways[total_score] = [(x, y), i, j, k, b]

    log("")
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


def penguin_detect(world):
    global found_penguin
    orow = pos_to_obs(other_row(world.car.y))
    if obstacles.PENGUIN in orow:
        found_penguin = True

# def penguin_disappear(world):
#     back_rows_pos = list()
#     back_rows_obs = list()
#     for i in range(world.car.y, 10):
#         back_rows_pos.append(row(i))
#
#     for item in back_rows_pos:
#         back_rows_obs.append(pos_to_obs(world, item))
#
#     for item in back_rows_obs:
#         print(item)


def drive(world):
    global action_list, cnt, num_of_steps, steps
    res = actions.NONE
    x = world.car.x
    y = world.car.y
    get_x_values(x)

    if steps < 55:
        score_board = world_to_score_board(world)
        action_list = way_to_actions(best_way(world, score_board))
        res = action_list[0]
    else:
        if cnt >= num_of_steps - 1:
            cnt = 0
        if cnt == 0:
            score_board = world_to_score_board(world)
            action_list = way_to_actions(best_way(world, score_board))
            print(action_list)
            res = action_list[0]
        elif 0 < cnt < num_of_steps - 1:
            res = action_list[cnt]

    if res == actions.NONE:
        obstacle = world.get((x, y - 1))
        if obstacle == obstacles.PENGUIN:
            res = actions.PICKUP
        elif obstacle == obstacles.WATER:
            res = actions.BRAKE
        elif obstacle == obstacles.CRACK:
            res = actions.JUMP

    cnt += 1
    steps = (steps + 1) % 60
    update_world(world, res)
    return res
