# Start time: 17:32
# End time: 19:55

import aocd

data = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

data = """..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
.........."""

data = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

data = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

data = aocd.get_data(year=2023, day=10)


def print_map(symbols):
    """To help with visual debugging."""
    print()
    min_x = min(x for x, _ in symbols)
    min_y = min(y for _, y in symbols)
    max_x = max(x for x, _ in symbols)
    max_y = max(y for _, y in symbols)
    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            if (x, y) in symbols:
                row += symbols[(x, y)]
            else:
                row += "."
        print(row)


PIPE_DX_DY = {  # {"symbol": [(dx_1, dy_1), (dx_2, dy_2)]}
    "|": [(0, -1), (0, 1)],
    "-": [(-1, 0), (1, 0)],
    "L": [(0, -1), (1, 0)],
    "J": [(0, -1), (-1, 0)],
    "7": [(-1, 0), (0, 1)],
    "F": [(0, 1), (1, 0)],
}

# Build dicts of symbols and pipe connections
sx, sy = start_xy = (-1, -1)
symbols = {}  # {(x, y): "symbol"}
pipes = {}  # {(x, y): {(adj_x_1, adj_y_1), (adj_x_2, adj_y_2)}
for y, row in enumerate(data.splitlines()):
    for x, symbol in enumerate(row):
        symbols[(x, y)] = symbol
        if symbol == ".":
            continue
        if symbol == "S":
            sx, sy = start_xy = (x, y)
            continue

        (dx1, dy1), (dx2, dy2) = PIPE_DX_DY[symbol]
        x1, y1, x2, y2 = x + dx1, y + dy1, x + dx2, y + dy2
        pipes[(x, y)] = {(x1, y1), (x2, y2)}

# Add start pipe connections
start_options = (
    [(sx, sy - 1), "|7F", (sx, sy + 1), "|LJ", "-"],
    [(sx - 1, sy), "-LF", (sx + 1, sy), "-J7", "|"],
    [(sx, sy - 1), "|7F", (sx + 1, sy), "-J7", "L"],
    [(sx + 1, sy), "-J7", (sx, sy + 1), "|JL", "F"],
    [(sx, sy + 1), "|JL", (sx - 1, sy), "-LF", "7"],
    [(sx - 1, sy), "-LF", (sx, sy - 1), "|7F", "J"],
)
for (x1, y1), symbols_1, (x2, y2), symbols_2, start_symbol in start_options:
    if (x1, y1) not in symbols or (x2, y2) not in symbols:
        continue
    if symbols[(x1, y1)] in symbols_1 and symbols[(x2, y2)] in symbols_2:
        pipes[start_xy] = {(x1, y1), (x2, y2)}
        symbols[start_xy] = start_symbol

# Calculate loop
loop = [start_xy, list(pipes[start_xy])[0]]
while loop[-1] != start_xy:
    next_xy = (pipes[loop[-1]] - {loop[-2]}).pop()
    loop.append(next_xy)

# Clean symbols
for xy, symbol in symbols.items():
    if xy not in loop:
        symbols[xy] = "."

exp_max_y = (len(data.splitlines()) * 2) - 1
exp_max_x = (len(data.splitlines()[0]) * 2) - 1

# Expand map
exp_symbols = {}  # {(x, y): "symbol"}
for (x, y), symbol in symbols.items():
    exp_symbols[(x * 2, y * 2)] = symbol
for y in range(exp_max_y + 1):
    for x in range(exp_max_x + 1):
        if (x, y) in exp_symbols:
            continue
        elif (x - 1, y) in exp_symbols and exp_symbols[(x - 1, y)] in "-FL":
            exp_symbols[(x, y)] = "-"
        elif (x, y - 1) in exp_symbols and exp_symbols[(x, y - 1)] in "|F7":
            exp_symbols[(x, y)] = "|"
        else:
            exp_symbols[(x, y)] = "."


# Add a border
for y in range(-1, exp_max_y + 1):
    exp_symbols[(-1, y)] = "."
    exp_symbols[(-1, exp_max_x)] = "."
for x in range(-1, exp_max_x + 1):
    exp_symbols[(x, -1)] = "."
    exp_symbols[(x, exp_max_y)] = "."


# Find all outside locations for expanded map
next_xy = {(-1, -1)}
while next_xy:
    x, y = next_xy.pop()
    exp_symbols[(x, y)] = "O"
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        poss_xy = (x + dx, y + dy)
        if poss_xy not in exp_symbols:
            continue
        if exp_symbols[poss_xy] == ".":
            next_xy.add(poss_xy)

# Contract map
symbols = {}  # {(x, y): "symbol"}
for y in range(0, exp_max_y + 1, 2):
    for x in range(0, exp_max_x + 1, 2):
        symbols[(x // 2, y // 2)] = exp_symbols[(x, y)]

# print_map(final_symbols)

print(len([xy for xy, symbol in symbols.items() if symbol == "."]))
