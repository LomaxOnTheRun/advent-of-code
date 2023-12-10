# Start time: 11:26
# End time: 17:32

import aocd

data = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

data = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""

data = aocd.get_data(year=2023, day=10)

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
    [(sx, sy - 1), "|7F", (sx, sy + 1), "|LJ"],
    [(sx - 1, sy), "-LF", (sx + 1, sy), "-J7"],
    [(sx, sy - 1), "|7F", (sx + 1, sy), "-J7"],
    [(sx + 1, sy), "-J7", (sx, sy + 1), "|JL"],
    [(sx, sy + 1), "|JL", (sx - 1, sy), "-LF"],
    [(sx - 1, sy), "-LF", (sx, sy - 1), "|7F"],
)
for (x1, y1), symbols_1, (x2, y2), symbols_2 in start_options:
    if (x1, y1) not in symbols or (x2, y2) not in symbols:
        continue
    if symbols[(x1, y1)] in symbols_1 and symbols[(x2, y2)] in symbols_2:
        pipes[start_xy] = {(x1, y1), (x2, y2)}

# Calculate loop
loop = [start_xy, list(pipes[start_xy])[0]]
while loop[-1] != start_xy:
    next_xy = (pipes[loop[-1]] - {loop[-2]}).pop()
    loop.append(next_xy)

print(len(loop) // 2)
