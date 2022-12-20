# Start time: 06:47
# End time: 07:40

import aocd

data = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

data = aocd.get_data(year=2022, day=17)

shapes_str = """
    ####

    .#.
    ###
    .#.

    ..#
    ..#
    ###

    #
    #
    #
    #

    ##
    ##
"""

shapes = (  # (x, y)
    ([0, 0], [1, 0], [2, 0], [3, 0]),
    ([1, 0], [0, 1], [1, 1], [2, 1], [1, 2]),
    ([0, 0], [1, 0], [2, 0], [2, 1], [2, 2]),
    ([0, 0], [0, 1], [0, 2], [0, 3]),
    ([0, 0], [0, 1], [1, 0], [1, 1]),
)


def print_room(settled, shape, max_height):
    for y in range(max_height + 6, -1, -1):
        row = "|"
        for x in range(7):
            if (x, y) in shape:
                row += "@"
            elif (x, y) in settled:
                row += "#"
            else:
                row += "."
        print(row + "|")
    print("+-------+\n")


max_height = -1
settled = set([(i, -1) for i in range(7)])
step = 0
for shape_id in range(2022):
    shape = {(sx + 2, sy + max_height + 4) for sx, sy in shapes[shape_id % len(shapes)]}

    while True:
        dx = -1 if data[step] == "<" else 1
        step = (step + 1) % len(data)
        for sx, sy in shape:
            if sx + dx < 0 or sx + dx > 6:
                dx = 0
            if (sx + dx, sy) in settled:
                dx = 0

        shape = {(sx + dx, sy) for sx, sy in shape}
        lower_shape = {(sx, sy - 1) for sx, sy in shape}
        if settled & lower_shape:
            settled |= shape
            max_height = max([sy for _, sy in settled])
            break
        shape = lower_shape

print(max_height + 1)
