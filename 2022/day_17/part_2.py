# Start time: 07:40
# End time: 21:29

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


def print_room(settled, shape, max_height, num_show_rows=None):
    y_stop = max(-1, max_height + 6 - num_show_rows) if num_show_rows else 0
    for y in range(max_height + 6, y_stop, -1):
        row = "|"
        for x in range(7):
            if [x, y] in shape:
                row += "@"
            elif (x, y) in settled:
                row += "#"
            else:
                row += "."
        print(row + "|")
    if y_stop == 0:
        print("+-------+\n")


def check_for_repeats(height_adds):
    for i in range(len(height_adds) // 10):
        if height_adds[-5 * i :] == height_adds[-10 * i : -5 * i]:
            return height_adds[-5 * i :]


max_height = 0
settled = set([(i, 0) for i in range(7)])

height_adds = []
shape_id = 0
step = 0

keep_going = True
while keep_going:

    shape = [[sx + 2, sy + max_height + 4] for sx, sy in shapes[shape_id]]

    shape_id = (shape_id + 1) % 5
    shape_step = 0

    while True:
        dx = -1 if data[step] == "<" else 1

        if step == 0:
            repeat = check_for_repeats(height_adds)
            if repeat:
                keep_going = False
                break

        step = (step + 1) % len(data)
        shape_step += 1

        for sx, sy in shape:
            # Stop at walls
            if sx + dx < 0 or sx + dx > 6:
                dx = 0
                break

            # Stop at settled pieces
            if (sx + dx, sy) in settled:
                dx = 0
                break

        for piece in shape:
            piece[0] += dx

        lower_shape = {(sx, sy - 1) for sx, sy in shape}

        # Check if lower shape hits settled
        if settled & lower_shape:
            settled |= {tuple(piece) for piece in shape}
            new_max_height = max([sy for _, sy in shape] + [max_height])

            height_adds.append((shape_id, new_max_height - max_height))

            max_height = new_max_height

            break

        for piece in shape:
            piece[1] -= 1

height_so_far = sum([height for _, height in height_adds])
shapes_so_far = len(height_adds)

height_in_repeat = sum([height for _, height in repeat])
shapes_in_repeat = len(repeat)

total_shapes = 1000000000000
shapes_left = total_shapes - shapes_so_far

more_repeats = shapes_left // shapes_in_repeat
height_so_far += height_in_repeat * more_repeats

more_shapes = shapes_left % shapes_in_repeat
total_height = height_so_far + sum([height for _, height in repeat[:more_shapes]])

print(total_height)
