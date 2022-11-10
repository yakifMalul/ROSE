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
def_y = -1
did_setup = False
num_of_steps = 5
found_penguin_dorow = False
found_penguin_dorow_1 = False
mode = 1
# 1- one lane
# 2- whole screen


def log(msg):
    """
    The function prints a certain message with time and date.
    @param msg: the message that the function prints
    """
    print(str(time.strftime("%Y-%m-%d %H:%M:%S")) + "\t" + msg)


def update_world(world, action):
    """
    The functions updates every move about where is all the obstacles are
    @param world: the track
    """
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


def setup(x, y):
    """
    The function checks if it is the first step if yes so it active some setup settings
    @param x: the current coll in which the player is in
    @param y: the current row in which the player is in
    """
    global is_right, steps, x1, x2, x3, ox1, ox2, ox3, def_y, mode, found_penguin_dorow, found_penguin_dorow_1
    if steps == 0:
        mode = 1
        found_penguin_dorow = False
        found_penguin_dorow_1 = False
        def_y = y
        x1 = x - 1
        x2 = x
        x3 = x + 1
        if 0 <= x2 <= 2:
            is_right = False
            ox1, ox2, ox3 = 3, 4, 5
        elif 3 <= x2 <= 5:
            is_right = True
            ox1, ox2, ox3 = 0, 1, 2


def row(y):
    """
    The function returns a certain row
    @param y: the number of row to get
    @return: list with the positions in the y row
    """
    global x1, x2, x3
    res = [(x1, y), (x2, y), (x3, y)]
    return res


def other_row(y):
    """
    The function returns a certain opponent row
    @param y: the number of row to get
    @return: list with the positions in the y row
    """
    global ox1, ox2, ox3
    res = [(ox1, y), (ox2, y), (ox3, y)]
    return res


def full_row(y):
    """
    The function returns a certain whole screen row
    @param y: the number of row to get
    @return: list with the positions in the y row
    """
    global x1, x2, x3, ox1, ox2, ox3, is_right
    if is_right:
        res = [(ox1, y), (ox2, y), (ox3, y), (x1, y), (x2, y), (x3, y)]
    else:
        res = [(x1, y), (x2, y), (x3, y), (ox1, y), (ox2, y), (ox3, y)]
    return res


def pos_to_obs(world, pos):
    """
    The function takes a position, checks whats appearing in that position and turns it into an obstacle
    @param world: the track
    @param pos: a position to check whats in it
    @return: a list with the obstacle
    """
    res = list()
    for item in pos:
        res.append(world.get(item))
    return res


def pos_to_score(world, pos):
    """
    The function takes a position, checks whats appearing in that position and turns it to a score
    @param world: the track
    @param pos: a position to check whats in it
    @return: a list with the scores
    """
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
    """
    The function makes a list that display the world with scores and not with obstacles
    @param world: the track
    @return: list of the track displayed by scores
    """
    global num_of_steps
    score_board = list()
    y = world.car.y

    for i in range(num_of_steps, -1, -1):
        score_board.append(pos_to_score(world, full_row(y-i)))
    return score_board


def get_connected(x, y):
    """
    The function checks and returns the possible position you can get to while on current position
    on one lane mode
    @param x, y: current x and y position
    @return: list of possible positions to go to
    """
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
    """
    The function checks and returns the possible position you can get to while on current position
    on full screen mode
    @param x, y: current x and y position
    @return: list of possible positions to go to
    """
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
        elif x == x2:
            res.append((3, y - 1))
            res.append((4, y - 1))
            res.append((5, y - 1))
        elif x == x3:
            res.append((4, y - 1))
            res.append((5, y - 1))
    else:
        if x == x1:
            res.append((0, y - 1))
            res.append((1, y - 1))
        elif x == x2:
            res.append((0, y - 1))
            res.append((1, y - 1))
            res.append((2, y - 1))
        elif x == x3:
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
    """
    The function checks every possible way for the player to go to
    and finds the way the player must go through in order to get the most score
    on one lane mode
    @param world: the track
    @param score_board: the board displayed by scores
    @return: list of the best way the player can go through
    """
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
                    # ways[total_score] = [(x, y), i, j, k, b]
                    if not is_right:
                        ways[total_score] = [(x, y), i, j, k, b]
                    else:
                        if total_score in list(ways):
                            pass
                        else:
                            ways[total_score] = [(x, y), i, j, k, b]

    big = list(ways)[0]
    for key in ways.keys():
        if big < key:
            big = key

    return ways[big]


def best_full_way(world, score_board):
    """
    The function checks every possible way for the player to go to
    and finds the way the player must go through in order to get the most score
    on whole screen mode
    @param world: the track
    @param score_board: the board displayed by scores
    @return: list of the best way the player can go through
    """
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
    for i in get_full_connected(x, y):
        score_i = 0
        if i[0] == x:
            score_i = score_board[i[1]][i[0]]
        elif score_board[i[1]][i[0]] != 10 and score_board[i[1]][i[0]] != 0:
            score_i = -10
        for j in get_full_connected(i[0], i[1]):
            score_j = 0
            if j[0] == i[0]:
                score_j = score_board[j[1]][j[0]]
            elif score_board[j[1]][j[0]] != 10 and score_board[j[1]][j[0]] != 0:
                score_j = -10
            for k in get_full_connected(j[0], j[1]):
                score_k = 0
                if k[0] == j[0]:
                    score_k = score_board[k[1]][k[0]]
                elif score_board[k[1]][k[0]] != 10 and score_board[k[1]][k[0]] != 0:
                    score_k = -10
                for b in get_full_connected(k[0], k[1]):
                    score_b = 0
                    if b[0] == k[0]:
                        score_b = score_board[b[1]][b[0]]
                    elif score_board[b[1]][b[0]] != 10 and score_board[b[1]][b[0]] != 0:
                        score_b = -10
                    total_score = score_def + score_i + score_j + score_k + score_b
                    # ways[total_score] = [(x, y), i, j, k, b]
                    if not is_right:
                        ways[total_score] = [(x, y), i, j, k, b]
                    else:
                        if total_score in list(ways):
                            pass
                        else:
                            ways[total_score] = [(x, y), i, j, k, b]

    big = list(ways)[0]
    for key in ways.keys():
        if big < key:
            big = key

    return ways[big]


def way_to_actions(way):
    """
    The function crates a list of actions the player must do for the optimal way
    @param way: list with the optimal x's
    @return: list actions for optimal way
    """
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
    """
    The function detects if there is a penguin in the starting row
    and one row under it of the opponent
    @param world: the track
    """
    global def_y, found_penguin_dorow, found_penguin_dorow_1
    dorow = pos_to_obs(world, other_row(def_y))
    dorow_1 = pos_to_obs(world, other_row(def_y+1))
    if obstacles.PENGUIN in dorow:
        log("found peng")
        found_penguin_dorow = True
    else:
        found_penguin_dorow = False
    if obstacles.PENGUIN in dorow_1:
        log("found peng 1")
        found_penguin_dorow_1 = True
    else:
        found_penguin_dorow_1 = False


def penguin_disappear(world):
    """
        The function detects if a penguin from one move earlier disappeared - someone took it
        @param world: the track
        """
    global def_y, found_penguin_dorow, found_penguin_dorow_1, mode
    if world.car.y == def_y:
        if found_penguin_dorow:
            dorow = pos_to_obs(world, other_row(def_y+1))
            if obstacles.PENGUIN not in dorow:
                mode = 2
            else:
                pass
        elif found_penguin_dorow_1:
            dorow_1 = pos_to_obs(world, other_row(def_y + 2))
            if obstacles.PENGUIN not in dorow_1:
                mode = 2
            else:
                pass
    elif world.car.y == def_y + 1:
        if found_penguin_dorow_1:
            dorow_1 = pos_to_obs(world, other_row(def_y + 2))
            if obstacles.PENGUIN not in dorow_1:
                mode = 2
            else:
                pass


def drive_normal(world):
    """
    The function tells the player what to do as the next action
    on one lane mode
    @param world: the track
    @return: the action the player will do
    """
    global action_list, cnt, num_of_steps, steps
    res = actions.NONE
    x = world.car.x
    y = world.car.y
    penguin_disappear(world)
    penguin_detect(world)

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


def drive_full_screen(world):
    """
    The function tells the player what to do as the next action
    on whole screen mode
    @param world: the track
    @return: the action the player will do
    """
    global action_list, cnt, num_of_steps, steps
    res = actions.NONE
    x = world.car.x
    y = world.car.y
    penguin_disappear(world)
    penguin_detect(world)

    if steps < 55:
        score_board = world_to_score_board(world)
        action_list = way_to_actions(best_full_way(world, score_board))
        res = action_list[0]
    else:
        if cnt >= num_of_steps - 1:
            cnt = 0
        if cnt == 0:
            score_board = world_to_score_board(world)
            action_list = way_to_actions(best_full_way(world, score_board))
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


def drive(world):
    """
    The function tells the player what to do as the next action
    @param world: the track
    @return: the action the player will do
    """
    global mode
    setup(world.car.x, world.car.y)
    log("mode is " + str(mode))
    if mode == 1:
        return drive_normal(world)
    elif mode == 2:
        return drive_full_screen(world)

    return actions.NONE

