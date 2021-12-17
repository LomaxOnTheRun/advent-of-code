import aocd, dataclasses, typing as t

data = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

# data = """116
# 138
# 213"""

data = aocd.get_data(year=2021, day=15)

data = data.split("\n")

# Grid
grid = {(y, x): int(data[y][x]) for y in range(len(data)) for x in range(len(data[0]))}

poss = [pos for pos in grid]
for y, x in poss:
    for dy in range(5):
        for dx in range(5):
            new_y = y + (dy * len(data))
            new_x = x + (dx * len(data[0]))
            new_value = grid[(y, x)] + dy + dx
            if new_value > 9:
                new_value %= 9
            grid[(new_y, new_x)] = new_value

# Neighbours
in_grid = lambda y, x: 0 <= y < (5 * len(data)) and 0 <= x < (5 * len(data[0]))
adj = lambda y, x: [(y + dy, x + dx) for dy, dx in [(-1, 0), (0, 1), (1, 0), (0, -1)]]
nbs = {pos: {nb for nb in adj(*pos) if in_grid(*nb)} for pos in grid}

# Calculate total risk of path
path_risk = lambda path: sum([grid[pos] for pos in path[1:]])

START = (0, 0)
END = ((5 * len(data)) - 1, (5 * len(data[0])) - 1)

open_set = {START: 0}
previous = {}

# Cheapest path to node
g = {START: 0}
# Heuristic (Manhattan distance)
h = lambda pos: (END[0] - pos[0]) + (END[1] - pos[1])

risk = 0

while open_set:
    # Get open node with lowest cost
    min_cost = min(open_set.values())
    current = sorted(open_set, key=open_set.get)[0]

    # Done, calculate the risk of the path
    if current == END:
        while current != START:
            # print(grid[current])
            risk += grid[current]
            current = previous[current]
        break

    del open_set[current]
    for nb in nbs[current]:
        new_g = g[current] + grid[nb]
        if nb not in g or new_g < g[nb]:
            g[nb] = new_g
            previous[nb] = current
            total_cost = g[nb] + h(nb)
            if nb not in open_set or total_cost < open_set[nb]:
                open_set[nb] = total_cost

print(risk)
