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

# data = aocd.get_data(year=2023, day=21)

xy_type = tuple[int, int]
grid_type = dict[xy_type, str]

HEIGHT = len(data.splitlines())
WIDTH = len(data.splitlines()[0])


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
            new_grid_xy = ((x + dx) % WIDTH, (y + dy) % HEIGHT)
            if grid[new_grid_xy] == "#":
                continue
            new_xy = (x + dx, y + dy)
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
frontier_sizes = []
diffs = []
diff_diffs = []
for i in range(5 * HEIGHT):
    new_frontier = take_step(grid, frontier)
    new_frontier -= all_plots
    if i % 2:  # TODO: Replace this for main data
        # if i % 2 == 0:
        all_plots |= new_frontier
        frontier_sizes.append(len(new_frontier))
        if len(frontier_sizes) > 1:
            diff = frontier_sizes[-1] - frontier_sizes[-2]
            diffs.append(diff)
    frontier = new_frontier

print("Warm up done")

for i in range(100):
    new_frontier = take_step(grid, new_frontier)
    new_frontier -= all_plots
    if i % 2:  # TODO: Replace this for main data
        # if i % 2 == 0:
        all_plots |= new_frontier
        frontier_sizes.append(len(new_frontier))
        if len(frontier_sizes) > HEIGHT + 1:
            diff = frontier_sizes[-1] - frontier_sizes[-2]
            prev_diff = frontier_sizes[-HEIGHT - 1] - frontier_sizes[-HEIGHT - 2]
            diff_diff = diff - prev_diff
            diff_diffs.append(diff_diff)
            print(diff_diff)
    frontier = new_frontier

print(diff_diffs[:5])

# if len(diff_diffs) > 10:
#     print(diff_diffs[:5])
#     print(diff_diffs[-6:-1])
#     if diff_diffs[:5] == diff_diffs[-6:-1]:
#         print("Breaking at step", i)
#         print(diff_diffs[:5])
#         print(diff_diffs[-6:-1])
#         break
