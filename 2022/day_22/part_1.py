# Start time: 10:13
# End time: 12:19

import aocd

data = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

data = aocd.get_data(year=2022, day=22)

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

lines = data.split("\n")

ground = set()
walls = set()
for y, line in enumerate(lines[:-2]):
    for x, char in enumerate(line):
        coord = (x, y)
        if char == ".":
            ground.add(coord)
        elif char == "#":
            walls.add(coord)

ground_or_walls = ground | walls

next_ground = {}
for x, y in ground:
    # Right
    next_right = (x + 1, y)
    if next_right not in ground_or_walls:
        next_x = min([x for x, next_y in ground_or_walls if next_y == y])
        next_right = (next_x, y)
    if next_right in walls:
        next_right = (x, y)

    # Left
    next_left = (x - 1, y)
    if next_left not in ground_or_walls:
        next_x = max([x for x, next_y in ground_or_walls if next_y == y])
        next_left = (next_x, y)
    if next_left in walls:
        next_left = (x, y)

    # Down
    next_down = (x, y + 1)
    if next_down not in ground_or_walls:
        next_y = min([y for next_x, y in ground_or_walls if next_x == x])
        next_down = (x, next_y)
    if next_down in walls:
        next_down = (x, y)

    # Up
    next_up = (x, y - 1)
    if next_up not in ground_or_walls:
        next_y = max([y for next_x, y in ground_or_walls if next_x == x])
        next_up = (x, next_y)
    if next_up in walls:
        next_up = (x, y)

    next_ground[(x, y)] = (next_right, next_down, next_left, next_up)

route = lines[-1].replace("R", "-R-").replace("L", "-L-").split("-")

coord = (min([x for x, y in ground if y == 0]), 0)
facing = RIGHT
for step in route:
    if step == "R":
        facing = (facing + 1) % 4
    elif step == "L":
        facing = (facing - 1) % 4
    else:
        for _ in range(int(step)):
            coord = next_ground[coord][facing]

print((1000 * (coord[1] + 1)) + (4 * (coord[0] + 1)) + facing)
