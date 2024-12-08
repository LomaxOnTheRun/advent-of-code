import aocd, collections, itertools

coords = collections.defaultdict(list)
for y_max, row in enumerate(aocd.get_data(year=2024, day=8).split()):
    for x_max, char in enumerate(row):
        coords[char] += [(x_max, y_max)] if char != "." else []

for part in (0, 1):
    antinodes = set()
    for nodes in coords.values():
        for (x1, y1), (x2, y2) in itertools.permutations(nodes, 2):
            for i in range(-2, -1 + (part * x_max)):
                antinodes |= {(x2 + (i * (x2 - x1)), y2 + (i * (y2 - y1)))}

    print(len({(x, y) for (x, y) in antinodes if 0 <= x <= x_max and 0 <= y <= y_max}))
