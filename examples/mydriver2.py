"""
This driver does not do any action.
"""
from rose.common import obstacles, actions  # NOQA

driver_name = "Yakir"


def drive(world):
    res = actions.NONE
    x = world.car.x
    y = world.car.y
    obstacle = world.get((x, y - 1))
    if world.get((x, y - 1)) == obstacles.PENGUIN:
        res = actions.PICKUP
    elif obstacle == obstacles.WATER:
        res = actions.BRAKE
    elif obstacle == obstacles.CRACK:
        res = actions.JUMP

    return res
