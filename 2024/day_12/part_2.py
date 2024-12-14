import aocd

data = """AAAA
BBCD
BBCC
EEEC"""

data = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""

data = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""

data = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""

data = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

data = aocd.get_data(year=2024, day=12)

coords = {}
for y, row in enumerate(data.split()):
    for x, val in enumerate(row):
        coords[(x, y)] = val

height = len(data.split())
width = len(data.split()[0])

plots = {}
parents = {xy: xy for xy in coords}


def add_to_plot(xy_to_merge, main_xy, plots, parents):
    parent_to_merge = parents[xy_to_merge]
    main_parent = parents[main_xy]
    if parent_to_merge == main_parent:
        return
    for plot_xy_to_merge in plots.pop(parent_to_merge):
        parents[plot_xy_to_merge] = main_parent
        plots[main_parent].append(plot_xy_to_merge)


for y in range(height):
    for x in range(width):
        val = coords[(x, y)]
        plots[(x, y)] = [(x, y)]
        if coords.get((x - 1, y)) == val:
            add_to_plot((x, y), (x - 1, y), plots, parents)
        if coords.get((x, y - 1)) == val:
            add_to_plot((x, y), (x, y - 1), plots, parents)


def get_num_sides(plot: list[tuple[int, int]]) -> int:
    xs = [x for x, _ in plot]
    ys = [y for _, y in plot]
    min_x, max_x, min_y, max_y = min(xs), max(xs), min(ys), max(ys)

    lines = 0
    # Top lines
    for row_y in range(min_y, max_y + 1):
        row = [x for x, y in plot if y == row_y and (x, y - 1) not in plot]
        row = [x for x in row if x - 1 not in row]
        lines += len(row)
    # Bottom lines
    for row_y in range(min_y, max_y + 1):
        row = [x for x, y in plot if y == row_y and (x, y + 1) not in plot]
        row = [x for x in row if x - 1 not in row]
        lines += len(row)
    # Left lines
    for col_x in range(min_x, max_x + 1):
        col = [y for x, y in plot if x == col_x and (x - 1, y) not in plot]
        col = [y for y in col if y - 1 not in col]
        lines += len(col)
    # Right lines
    for col_x in range(min_x, max_x + 1):
        col = [y for x, y in plot if x == col_x and (x + 1, y) not in plot]
        col = [y for y in col if y - 1 not in col]
        lines += len(col)

    return lines


total = 0
for xy, plot in plots.items():
    total += len(plot) * get_num_sides(plot)
print(total)
