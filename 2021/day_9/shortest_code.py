import aocd, math

data = """2199943210
3987894921
9856789892
8767896789
9899965678""".split(
    "\n"
)

data = aocd.get_data(year=2021, day=9).split("\n")

grid = {(y, x): int(data[y][x]) for y in range(len(data)) for x in range(len(data[0]))}
adjacent = [(-1, 0), (1, 0), (0, -1), (0, 1)]
nbs = {(y, x): {(y + dy, x + dx) for dy, dx in adjacent} for y, x in grid}

lowest = {pos for pos in grid if all([grid[pos] < grid.get(nb, 9) for nb in nbs[pos]])}

# Part 1
print(sum([grid[pos] + 1 for pos in lowest]))

# Part 2
basins = [[pos] for pos in lowest]
for basin in basins:
    for pos in basin:
        basin += [nb for nb in nbs[pos] if nb not in basin and grid.get(nb, 9) < 9]


print(math.prod(sorted([len(basin) for basin in basins])[-3:]))

# *********************

# USING SETS

# basins = [set([point]) for point in lowest]

# # Only valid squares left
# valid_pos = {pos for pos in grid if grid[pos] < 9}
# nbs = {pos: {nb for nb in nbs[pos] if nb in valid_pos} for pos in valid_pos}

# while valid_pos:
#     basins = [basin.union(*[nbs[pos] for pos in basin]) for basin in basins]
#     valid_pos = valid_pos.difference(*basins)

# print(math.prod(sorted([len(basin) for basin in basins])[-3:]))

# *********************

# USING RECURSION (NOT COMPLETE)

# valid = lambda pos, basin: pos not in basin and pos in valid_pos

# def add_neighbours(basin, pos):
#     basin.append(pos) if valid(pos, basin) else None
#     for nb in [nb for nb in nbs.get(pos, []) if valid(nb, basin)]:
#         add_neighbours(basin, nb)

# for basin in basins:
#     add_neighbours(basin, basin[0])
