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

plots = {}  # {(x, y): [(x, y), (x, y)]}
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


def get_perimeter(plot):
    perimeter = len(plot) * 4
    for x, y in plot:
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if (x + dx, y + dy) in plot:
                perimeter -= 1
    return perimeter


total = 0
for xy, plot in plots.items():
    total += len(plot) * get_perimeter(plot)
print(total)
