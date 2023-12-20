# Start time: 11:27
# End time: 18:01

import aocd

data = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

data = aocd.get_data(year=2023, day=14)

HEIGHT = len(data.split())
WIDTH = len(data.split()[0])
NORTH, WEST, SOUTH, EAST = "NORTH", "WEST", "SOUTH", "EAST"

squares = set()
circles = set()
for y, line in enumerate(data.split()):
    for x, char in enumerate(line):
        if char == "#":
            squares.add((x, y))
        if char == "O":
            circles.add((x, y))


def move_circles_north(squares, circles):
    new_circles = set()
    for col in range(WIDTH):
        col_squares = [-1, HEIGHT] + [y for x, y in squares if x == col]
        col_circles = [y for x, y in circles if x == col]
        num_col_circles = {y: 0 for y in col_squares}
        for circle_y in col_circles:
            next_square = max(y for y in col_squares if y < circle_y)
            num_col_circles[next_square] += 1

        for square_y, num_circles in num_col_circles.items():
            for new_y in range(square_y + 1, square_y + num_circles + 1):
                new_circles.add((col, new_y))

    return new_circles


def move_circles_south(squares, circles):
    new_circles = set()
    for col in range(WIDTH):
        col_squares = [-1, HEIGHT] + [y for x, y in squares if x == col]
        col_circles = [y for x, y in circles if x == col]
        num_col_circles = {y: 0 for y in col_squares}
        for circle_y in col_circles:
            next_square = min(y for y in col_squares if y > circle_y)
            num_col_circles[next_square] += 1

        for square_y, num_circles in num_col_circles.items():
            for new_y in range(square_y - 1, square_y - num_circles - 1, -1):
                new_circles.add((col, new_y))

    return new_circles


def move_circles_west(squares, circles):
    new_circles = set()
    for row in range(HEIGHT):
        row_squares = [-1, WIDTH] + [x for x, y in squares if y == row]
        row_circles = [x for x, y in circles if y == row]
        num_row_circles = {x: 0 for x in row_squares}
        for circle_x in row_circles:
            next_square = max(x for x in row_squares if x < circle_x)
            num_row_circles[next_square] += 1

        for square_x, num_circles in num_row_circles.items():
            for new_x in range(square_x + 1, square_x + num_circles + 1):
                new_circles.add((new_x, row))

    return new_circles


def move_circles_east(squares, circles):
    new_circles = set()
    for row in range(HEIGHT):
        row_squares = [-1, WIDTH] + [x for x, y in squares if y == row]
        row_circles = [x for x, y in circles if y == row]
        num_row_circles = {x: 0 for x in row_squares}
        for circle_x in row_circles:
            next_square = min(x for x in row_squares if x > circle_x)
            num_row_circles[next_square] += 1

        for square_x, num_circles in num_row_circles.items():
            for new_x in range(square_x - 1, square_x - num_circles - 1, -1):
                new_circles.add((new_x, row))

    return new_circles


def do_cycle(squares, circles):
    circles = move_circles_north(squares, circles)
    circles = move_circles_west(squares, circles)
    circles = move_circles_south(squares, circles)
    circles = move_circles_east(squares, circles)
    return circles


def calculate_weight(circles):
    weight = 0
    for _, y in circles:
        weight += HEIGHT - y
    return weight


def get_cycle_length(weights, weight):
    # print(weights)
    # Get index of last weight
    current_index = len(weights)
    last_index = len(weights) - 1 - weights[::-1].index(weight)
    di = current_index - last_index
    # print(weight, current_index, last_index, di)
    for i in range(5):
        # print(-((i + 1) * di), weights[-((i + 1) * di)], weight)
        if weights[-((i + 1) * di)] != weight:
            return -1
    return di


# Do a bunch of cycles
weights = []
initial_cycles = 200
for i in range(initial_cycles):
    # print(i)
    circles = do_cycle(squares, circles)
    weight = calculate_weight(circles)
    weights.append(weight)

# print(weights)

# Now look for a pattern
cycle = []
cycle_length, weights_offset = -1, -1
for i in range(1000):
    circles = do_cycle(squares, circles)
    weight = calculate_weight(circles)
    if weight in weights:
        cycle_length = get_cycle_length(weights, weight)
        # print(i, cycle_length)
        if cycle_length != -1:
            weights_offset = initial_cycles + i
            cycle = weights[-cycle_length:]
            break
    weights.append(weight)

# Calculate where in the cycle we hit 1e10
cycle_offset = ((1_000_000_000 - weights_offset) % cycle_length) - 1
print(cycle[cycle_offset])
