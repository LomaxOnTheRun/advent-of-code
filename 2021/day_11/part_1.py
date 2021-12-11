# Start time: 7:37am
# End time: 8:06am

import aocd

data = """11111
19991
19191
19991
11111"""

data = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

data = aocd.get_data(year=2021, day=11)

data = data.split("\n")

grid = {(y, x): int(data[y][x]) for y in range(len(data)) for x in range(len(data[0]))}
adjacent = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
in_grid = lambda y, x: 0 <= y < len(data) and 0 <= x < len(data[0])
neighbours = {
    (y, x): {(y + dy, x + dx) for dy, dx in adjacent if in_grid(y + dy, x + dx)}
    for y, x in grid
}


def light(old_grid, new_grid, pos):
    for nb in neighbours[pos]:
        new_grid[nb] = new_grid.get(nb, old_grid[nb]) + 1
        if new_grid[nb] == 10:
            light(old_grid, new_grid, nb)


def step(old_grid):
    new_grid = {}
    for pos in old_grid:
        new_grid[pos] = new_grid.get(pos, old_grid[pos]) + 1
        if new_grid[pos] == 10:
            light(old_grid, new_grid, pos)

    flashes = 0
    for pos in new_grid:
        if new_grid[pos] > 9:
            new_grid[pos] = 0
            flashes += 1

    return new_grid, flashes


def print_grid(grid):
    print("-" * 30)
    for y in range(len(data)):
        print(str([grid[(y, x)] for x in range(len(data[0]))]))


flashes = 0
for _ in range(100):
    grid, new_flashes = step(grid)
    flashes += new_flashes
    if _ == 99:
        print(flashes)
