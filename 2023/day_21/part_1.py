# Start time: 08:45
# End time: 09:17

import aocd

data = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

data = aocd.get_data(year=2023, day=21)

xy_type = tuple[int, int]
grid_type = dict[xy_type, str]


def create_grid(data: str) -> grid_type:
    grid = {}
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            grid[(x, y)] = char
    return grid


def take_step(grid: grid_type, frontier: set[xy_type]) -> set[xy_type]:
    new_frontier = set()
    for x, y in frontier:
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_xy = (x + dx, y + dy)
            if new_xy not in grid:
                continue
            if grid[new_xy] == "#":
                continue
            new_frontier.add(new_xy)
    return new_frontier


def get_start_xy(grid: grid_type) -> xy_type:
    for xy, char in grid.items():
        if char == "S":
            return xy
    return -1, -1


grid = create_grid(data)
frontier = {get_start_xy(grid)}
all_plots = {get_start_xy(grid)}
for i in range(64):
    new_frontier = take_step(grid, frontier)
    new_frontier -= all_plots
    if i % 2:
        all_plots |= new_frontier
    frontier = new_frontier

print(len(all_plots))
