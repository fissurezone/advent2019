from computer import run_until_next_input
from enum import Enum


class Orientation(Enum):
    UP = 0
    LEFT = 1
    RIGHT = 2
    DOWN = 3


def turn(orientation, direction):
    if orientation == Orientation.UP:
        if direction == 0:
            return Orientation.LEFT
        else:
            return Orientation.RIGHT
    if orientation == Orientation.LEFT:
        if direction == 0:
            return Orientation.DOWN
        else:
            return Orientation.UP
    if orientation == Orientation.RIGHT:
        return turn(Orientation.LEFT, 1 - direction)
    if orientation == Orientation.DOWN:
        return turn(Orientation.UP, 1 - direction)


def advance(coordinates, orientation):
    x, y = coordinates
    if orientation == Orientation.UP:
        return x, y+1
    elif orientation == Orientation.LEFT:
        return x-1, y
    elif orientation == Orientation.RIGHT:
        return x+1, y
    else:
        return x, y-1


def paint_panels(robot_code, initial_panel_colour=0):
    panel_colours = {(0, 0): initial_panel_colour}
    position = (0, 0)
    facing = Orientation.UP

    robot = run_until_next_input(robot_code)
    next(robot)
    while True:
        colour = panel_colours[position] if position in panel_colours else 0
        panel_colours[position] = robot.send(colour)
        facing = turn(facing, robot.send(colour))
        try:
            robot.send(colour)
        except StopIteration:
            break
        position = advance(position, facing)
    return panel_colours


if __name__ == '__main__':
    with open('input.txt') as f:
        code = [int(x) for x in f.readline().strip().split(',')]

    print('Part 1 : {}'.format(len(paint_panels(code[:]))))

    panels = paint_panels(code[:], 1)

    print('Part 2 :')
    left = min(panels.keys(), key=lambda tup: tup[0])[0]
    right = max(panels.keys(), key=lambda tup: tup[0])[0]
    top = max(panels.keys(), key=lambda tup: tup[1])[1]
    bottom = min(panels.keys(), key=lambda tup: tup[1])[1]
    for row in range(top, bottom - 1, -1):
        line = []
        for col in range(left, right + 1):
            pos = (col, row)
            if pos in panels:
                line.append('#' if panels[pos] == 1 else ' ')
            else:
                line.append(' ')
        print(''.join(line))
