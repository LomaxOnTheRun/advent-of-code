# Start time: 10:50
# End time: 11:27

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

squares = set()
circles = set()
for y, line in enumerate(data.split()):
    for x, char in enumerate(line):
        if char == "#":
            squares.add((x, y))
        if char == "O":
            circles.add((x, y))

total_weight = 0
for col in range(WIDTH):
    col_squares = [-1] + [y for x, y in squares if x == col]
    col_circles = [y for x, y in circles if x == col]
    num_col_circles = {y: 0 for y in col_squares}
    for circle_y in col_circles:
        next_square = max(y for y in col_squares if y < circle_y)
        num_col_circles[next_square] += 1

    new_col_circles = []
    for y, num_circles in num_col_circles.items():
        for i in range(y + 1, y + num_circles + 1):
            new_col_circles.append(i)
            total_weight += HEIGHT - i

print(total_weight)
