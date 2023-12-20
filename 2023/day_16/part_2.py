# Start time: 10:02
# End time: 10:09

import aocd

data = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""

data = aocd.get_data(year=2023, day=16)

LEFT, RIGHT, UP, DOWN = "L", "R", "U", "D"
DX_DY = {"L": (-1, 0), "R": (1, 0), "U": (0, -1), "D": (0, 1)}

EXIT_DIRECTIONS = {
    "/": {LEFT: [DOWN], RIGHT: [UP], UP: [RIGHT], DOWN: [LEFT]},
    "\\": {LEFT: [UP], RIGHT: [DOWN], UP: [LEFT], DOWN: [RIGHT]},
    "-": {LEFT: [LEFT], RIGHT: [RIGHT], UP: [LEFT, RIGHT], DOWN: [LEFT, RIGHT]},
    "|": {LEFT: [UP, DOWN], RIGHT: [UP, DOWN], UP: [UP], DOWN: [DOWN]},
}

HEIGHT = len(data.split())
WIDTH = len(data.split()[0])


def print_map(surfaces, energised):
    width = len(data.split()[0])
    height = len(data.split())
    for y in range(height):
        for x in range(width):
            char = surfaces[(x, y)]
            if char == "." and (x, y) in energised:
                char = "#"
            print(char, end="")
        print()


def get_surfaces(data):
    surfaces = {}
    for y, line in enumerate(data.splitlines()):
        for x, surface in enumerate(line):
            surfaces[(x, y)] = surface
    return surfaces


def get_num_energised(surfaces, start_x, start_y, start_direction):
    energised = set()
    frontier = [(start_x, start_y, start_direction)]
    seen_frontiers = set()

    while frontier:
        # print(frontier)

        # Get next line to start
        x, y, direction = frontier.pop(0)
        seen_frontiers.add((x, y, direction))
        dx, dy = DX_DY[direction]

        if (x, y) in surfaces:
            energised.add((x, y))

        # print(x, y, direction)
        # print(dx, dy)

        # Stop when we hit the edge of the grid
        next_x, next_y = x + dx, y + dy
        while (next_x, next_y) in surfaces:
            # print(next_x)
            next_surface = surfaces[(next_x, next_y)]

            # Empty space
            if next_surface == ".":
                energised.add((next_x, next_y))
                next_x, next_y = next_x + dx, next_y + dy
                continue

            # Another surface
            next_exit_directions = EXIT_DIRECTIONS[next_surface]
            for exit_direction in next_exit_directions[direction]:
                next_frontier = (next_x, next_y, exit_direction)
                if next_frontier not in seen_frontiers:
                    frontier.append(next_frontier)
            break

    return len(energised)


surfaces = get_surfaces(data)
max_energised = 0
for y in range(HEIGHT):
    left_energised = get_num_energised(surfaces, -1, y, RIGHT)
    right_energised = get_num_energised(surfaces, WIDTH, y, LEFT)
    max_energised = max([max_energised, left_energised, right_energised])

for x in range(WIDTH):
    up_energised = get_num_energised(surfaces, x, -1, DOWN)
    down_energised = get_num_energised(surfaces, x, HEIGHT, UP)
    max_energised = max([max_energised, up_energised, down_energised])

# print_map(surfaces, energised)

print(max_energised)
