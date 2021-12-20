import aocd

data = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""

data = aocd.get_data(year=2021, day=20)


def print_grid(grid):
    min_y, max_y = min([y for y, _ in grid]), max([y for y, _ in grid])
    min_x, max_x = min([x for _, x in grid]), max([x for _, x in grid])
    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            row += grid[(y, x)]
        print(row)


def coord_to_algo_pos(grid, y, x):
    algo_bin_str = ""
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            algo_bin_str += grid.get((y + dy, x + dx), ".")
    return int(algo_bin_str.replace(".", "0").replace("#", "1"), 2)


def add_border(grid):
    min_y, max_y = min([y for y, _ in grid]), max([y for y, _ in grid])
    min_x, max_x = min([x for _, x in grid]), max([x for _, x in grid])
    for y in range(min_y - 1, max_y + 2):
        grid[(y, min_x - 1)] = "."
        grid[(y, max_x + 1)] = "."
    for x in range(min_x - 1, max_x + 2):
        grid[(min_y - 1, x)] = "."
        grid[(max_y + 1, x)] = "."
    return grid


def expand(grid, algo):
    new_grid = {}
    for pos in grid:
        new_grid[pos] = algo[coord_to_algo_pos(grid, *pos)]
    return new_grid


algo, image = data.split("\n\n")
image = image.split("\n")

max_y, max_x = len(image), len(image[0])
grid = {(y, x): image[y][x] for y in range(max_y) for x in range(max_x)}

num_expands = 50

for _ in range(2 * num_expands + 1):
    grid = add_border(grid)

for _ in range(num_expands):
    grid = expand(grid, algo)

in_grid = lambda xy, num_expands: -(num_expands + 1) < xy < max_y + num_expands
grid = {
    (y, x): grid[(y, x)]
    for y, x in grid
    if in_grid(y, num_expands) and in_grid(x, num_expands)
}

print(list(grid.values()).count("#"))
