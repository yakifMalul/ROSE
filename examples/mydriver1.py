"""
This driver does not do any action.
"""
from rose.common import obstacles, actions  # NOQA

driver_name = "Amit"


def drive(world):
    x = world.car.x
    y = world.car.y
    obstacle = world.get((x, y - 1))
    if world.get((x, y - 1)) == obstacles.PENGUIN:
        return actions.PICKUP
    elif obstacle == obstacles.WATER:
        return actions.BRAKE
    elif obstacle == obstacles.TRASH:
        return actions.LEFT
    elif obstacle == obstacles.CRACK:
        return actions.JUMP
    elif obstacle == obstacles.BIKE:
        return actions.RIGHT
    elif obstacle == obstacles.BARRIER:
        return actions.RIGHT

    return actions.NONE
