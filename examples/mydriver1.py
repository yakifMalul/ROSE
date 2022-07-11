"""
This driver does not do any action.
"""
from rose.common import obstacles, actions  # NOQA

driver_name = "Amit"
right_balance = 0


def move():  # * - *
    global right_balance
    if right_balance < 1:
        right_balance += 1
        return actions.RIGHT
    elif right_balance > -1:
        right_balance -= 1
        return actions.LEFT


def pos_to_score(world, pos):
    temp = list()
    res = list()
    for item in pos:
        temp.append(world.get(item))
    score = 0
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


def find_best(row):
    index = 0
    max = row[index]
    for i in range(1, len(row)):
        if max < row[i]:
            max = row[i]
            index = i
    return index


def row(world):
    global right_balance
    x = world.car.x
    y = world.car.y
    next_row = list()

    if right_balance > 0:
        next_row = [(x - 2, y - 1), (x-1, y-1), (x, y-1)]
    elif right_balance == 0:
        next_row = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]
    elif right_balance < 0:
        next_row = [(x, y - 1), (x + 1, y - 1), (x - 2, y - 1)]

    next_row_scores = pos_to_score(world, next_row)
    best_index = find_best(next_row_scores)
    return actions.RIGHT
    # if next_row_scores[best_index] == 0 and next_row_scores[1] == 0:
    #     # go mid
    #     if right_balance > 0:
    #         # left
    #         return actions.LEFT
    #     elif right_balance < 0:
    #         # right
    #         return actions.RIGHT
    #     else:
    #         # stay
    #         return actions.NONE
    # else:
    #     # go best
    #     best_pos = next_row[best_index]
    #     if x - best_pos[0] > 0:
    #         # left
    #         return actions.LEFT
    #     elif x - best_pos[0] < 0:
    #         # right
    #         return actions.RIGHT
    #     else:
    #         # straight
    #         return actions.NONE






def drive(world):
    return actions.RIGHT
    return row(world)

    # x = world.car.x
    # y = world.car.y
    # obstacle = world.get((x, y - 1))
    # if world.get((x, y)) == obstacles.PENGUIN:
    #     return actions.PICKUP
    # elif obstacle == obstacles.WATER:
    #     return actions.BRAKE
    # elif obstacle == obstacles.TRASH:
    #     return move()
    # elif obstacle == obstacles.CRACK:
    #     return actions.JUMP
    # elif obstacle == obstacles.BIKE:
    #     return move()
    # elif obstacle == obstacles.BARRIER:
    #     return move()

    # return actions.NONE
