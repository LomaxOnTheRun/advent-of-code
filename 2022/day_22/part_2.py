# Start time: 12:19
# End time: 16:41

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

########
#      #
#   21 #
#   3  #
#  54  #
#  6   #
#      #
########

data = aocd.get_data(year=2022, day=22)

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
DIR_NAMES = ["RIGHT", "DOWN", "LEFT", "UP"]

lines = data.split("\n")

# Assumes faces are square
FACE_SIZE = min([len(line.strip()) for line in lines[:-2]])

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

# Create set of existing faces
FACES = set()
for x in range(4):
    for y in range(4):
        if (x * FACE_SIZE, y * FACE_SIZE) in ground_or_walls:
            FACES.add((x, y))
assert len(FACES) == 6


def pivot_left(coord_x, coord_y, pivot_x, pivot_y):
    new_x = pivot_x + (coord_y - pivot_y)
    new_y = pivot_y - (coord_x - pivot_x)
    return (new_x, new_y)


def pivot_right(coord_x, coord_y, pivot_x, pivot_y):
    new_x = pivot_x - (coord_y - pivot_y)
    new_y = pivot_y + (coord_x - pivot_x)
    return (new_x, new_y)


def flip(x, y, dir):
    if dir == LEFT:
        return (x - (2 * (x % FACE_SIZE)) - 1, y)
    if dir == RIGHT:
        return (x + (2 * (FACE_SIZE - (x % FACE_SIZE))) - 1, y)
    if dir == UP:
        return (x, y - (2 * (y % FACE_SIZE)) - 1)
    if dir == DOWN:
        return (x, y + (2 * (FACE_SIZE - (y % FACE_SIZE))) - 1)


def get_next_right(x: int, y: int, facing: int) -> tuple[tuple[int, int], int]:
    dx, dy = DIRS[facing]
    next_coord = (x + dx, y + dy)
    face_x, face_y = (x // FACE_SIZE, y // FACE_SIZE)
    next_facing = facing

    # Wrap around to different face
    if next_coord not in ground_or_walls:
        if (face_x + 1, face_y - 1) in FACES:
            pivot = (x, (face_y * FACE_SIZE) - 1)
            next_coord = pivot_left(x, y, *pivot)
            # next_facing = (facing - 1) % 4
            next_facing = UP
        elif (face_x + 1, face_y + 1) in FACES:
            pivot = (x, (face_y + 1) * FACE_SIZE)
            next_coord = pivot_right(x, y, *pivot)
            next_facing = (facing + 1) % 4
        # elif (face_x - 1, face_y - 2) in FACES:
        #     flipped_x, flipped_y = flip(x, y, UP)
        #     next_coord = (flipped_x - FACE_SIZE, flipped_y - FACE_SIZE)
        #     next_facing = (facing + 2) % 4
        elif (face_x - 1, face_y + 2) in FACES:
            flipped_x, flipped_y = flip(x, y, DOWN)
            next_coord = (flipped_x - FACE_SIZE, flipped_y + FACE_SIZE)
            # next_facing = (facing + 2) % 4
            next_facing = LEFT
        elif (face_x + 1, face_y - 2) in FACES:
            flipped_x, flipped_y = flip(x, y, UP)
            next_coord = (flipped_x + FACE_SIZE, flipped_y - FACE_SIZE)
            # next_facing = (facing + 2) % 4
            next_facing = LEFT
        else:
            raise Exception(
                f"DON'T KNOW WHICH FACE TO GO TO: {(face_x, face_y)} {DIR_NAMES[facing]}"
            )

    # Stay still if next position is a wall
    if next_coord in walls:
        next_coord = (x, y)
        next_facing = facing

    return next_coord, next_facing


def get_next_left(x: int, y: int, facing: int) -> tuple[tuple[int, int], int]:
    dx, dy = DIRS[facing]
    next_coord = (x + dx, y + dy)
    face_x, face_y = (x // FACE_SIZE, y // FACE_SIZE)
    next_facing = facing

    # Wrap around to different face
    if next_coord not in ground_or_walls:
        if (face_x - 1, face_y + 1) in FACES:  # 3 -> 5
            pivot = (x, (face_y + 1) * FACE_SIZE)
            next_coord = pivot_left(x, y, *pivot)
            # next_facing = (facing - 1) % 4
            next_facing = DOWN
        elif (face_x + 1, face_y - 3) in FACES:  # 6 -> 3
            pivot = (x, face_y * FACE_SIZE)
            pivoted_x, pivoted_y = pivot_left(x, y, *pivot)
            next_coord = (pivoted_x + FACE_SIZE, pivoted_y - (3 * FACE_SIZE))
            next_facing = DOWN
        elif (face_x + 1, face_y - 2) in FACES:  # 5 -> 2
            flipped_x, flipped_y = flip(x, y, UP)
            next_coord = (flipped_x + FACE_SIZE, flipped_y - FACE_SIZE)
            # next_facing = (facing + 2) % 4
            next_facing = RIGHT
        elif (face_x - 1, face_y + 2) in FACES:
            flipped_x, flipped_y = flip(x, y, DOWN)
            next_coord = (flipped_x - FACE_SIZE, flipped_y + FACE_SIZE)
            next_facing = (facing + 2) % 4
        else:
            raise Exception(
                f"DON'T KNOW WHICH FACE TO GO TO: {(face_x, face_y)} {DIR_NAMES[facing]}"
            )

    # Stay still if next position is a wall
    if next_coord in walls:
        next_coord = (x, y)
        next_facing = facing

    return next_coord, next_facing


def get_next_down(x: int, y: int, facing: int) -> tuple[tuple[int, int], int]:
    dx, dy = DIRS[facing]
    next_coord = (x + dx, y + dy)
    face_x, face_y = (x // FACE_SIZE, y // FACE_SIZE)
    next_facing = facing

    # Wrap around to different face
    if next_coord not in ground_or_walls:
        if (face_x - 1, face_y + 1) in FACES:
            pivot = ((face_x * FACE_SIZE) - 1, y)
            next_coord = pivot_right(x, y, *pivot)
            next_facing = (facing + 1) % 4
        elif (face_x - 2, face_y - 1) in FACES:
            flipped_x, flipped_y = flip(x, y, LEFT)
            next_coord = (flipped_x - FACE_SIZE, flipped_y - FACE_SIZE)
            next_facing = (facing + 2) % 4
        elif (face_x + 2, face_y - 1) in FACES:
            flipped_x, flipped_y = flip(x, y, RIGHT)
            next_coord = (flipped_x + FACE_SIZE, flipped_y - FACE_SIZE)
            next_facing = (facing + 2) % 4
        elif (face_x + 2, face_y - 3) in FACES:
            next_coord = (x + (2 * FACE_SIZE), (y - (4 * FACE_SIZE)) + 1)
        else:
            raise Exception(
                f"DON'T KNOW WHICH FACE TO GO TO: {(face_x, face_y)} {DIR_NAMES[facing]}"
            )

    # Stay still if next position is a wall
    if next_coord in walls:
        next_coord = (x, y)
        next_facing = facing

    return next_coord, next_facing


def get_next_up(x: int, y: int, facing: int) -> tuple[tuple[int, int], int]:
    dx, dy = DIRS[facing]
    next_coord = (x + dx, y + dy)
    face_x, face_y = (x // FACE_SIZE, y // FACE_SIZE)
    next_facing = facing

    # Wrap around to different face
    if next_coord not in ground_or_walls:
        if (face_x - 1, face_y - 1) in FACES:
            pivot = ((face_x * FACE_SIZE) - 1, y)
            next_coord = pivot_left(x, y, *pivot)
            next_facing = (facing - 1) % 4
        elif (face_x + 1, face_y - 1) in FACES:
            pivot = ((face_x + 1) * FACE_SIZE, y)
            next_coord = pivot_right(x, y, *pivot)
            next_facing = (facing + 1) % 4
        elif (face_x - 2, face_y + 1) in FACES:
            flipped_x, flipped_y = flip(x, y, LEFT)
            next_coord = (flipped_x - FACE_SIZE, flipped_y + FACE_SIZE)
            next_facing = (facing + 2) % 4
        elif (face_x - 1, face_y + 3) in FACES:
            pivot = (face_x * FACE_SIZE, y)
            pivoted_x, pivoted_y = pivot_right(x, y, *pivot)
            next_coord = (pivoted_x - FACE_SIZE, pivoted_y + (3 * FACE_SIZE))
            next_facing = RIGHT
        elif (face_x - 2, face_y + 3) in FACES:
            next_coord = (x - (2 * FACE_SIZE), (y + (4 * FACE_SIZE)) - 1)
        else:
            raise Exception(
                f"DON'T KNOW WHICH FACE TO GO TO: {(face_x, face_y)} {DIR_NAMES[facing]}"
            )

    # Stay still if next position is a wall
    if next_coord in walls:
        next_coord = (x, y)
        next_facing = facing

    return next_coord, next_facing


def print_path(path):
    for y in range(FACE_SIZE * 4):
        row = ""
        for x in range(FACE_SIZE * 4):
            coord = (x, y)
            if coord in path:
                row += ">v<^"[path[coord]]
            elif coord in walls:
                row += "#"
            elif coord in ground:
                row += "."
            else:
                row += " "
        print(row)


def get_next_step(x, y):
    # Get new coords and new facing
    next_right = get_next_right(x, y, RIGHT)
    next_left = get_next_left(x, y, LEFT)
    next_down = get_next_down(x, y, DOWN)
    next_up = get_next_up(x, y, UP)
    return (next_right, next_down, next_left, next_up)


route = lines[-1].replace("R", "-R-").replace("L", "-L-").split("-")

coord = (min([x for x, y in ground if y == 0]), 0)
facing = RIGHT
path = {coord: facing}
for step in route:
    if step == "R":
        facing = (facing + 1) % 4
    elif step == "L":
        facing = (facing - 1) % 4
    else:
        for _ in range(int(step)):
            next_step = get_next_step(*coord)
            new_coord, new_facing = next_step[facing]
            path[coord] = new_facing
            if new_coord == coord and new_facing == facing:
                break
            coord = new_coord
            facing = new_facing

# print_path(path)

print((1000 * (coord[1] + 1)) + (4 * (coord[0] + 1)) + facing)
