# Start time: 06:44
# End time: 07:13

import aocd

data = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

data = aocd.get_data(year=2023, day=11)


def print_sky_map(sky_map):
    max_x = max(x for x, _ in sky_map.values())
    max_y = max(y for _, y in sky_map.values())
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in sky_map.values():
                print("#", end="")
            else:
                print(".", end="")
        print()


# Initial sky map
sky_map = {}  # {gid: (x, y)}
for y, row in enumerate(data.splitlines()):
    for x, char in enumerate(row):
        if char == "#":
            sky_map[len(sky_map)] = (x, y)

# Expand sky
non_empty_cols = {x for x, _ in sky_map.values()}
non_empty_rows = {y for _, y in sky_map.values()}
empty_rows = set(range(max(non_empty_rows) + 1)) - non_empty_rows
empty_cols = set(range(max(non_empty_cols) + 1)) - non_empty_cols
for gid, (x, y) in sky_map.items():
    dx = len([col for col in empty_cols if col < x])
    dy = len([row for row in empty_rows if row < y])
    sky_map[gid] = (x + dx, y + dy)

total = 0
for gid_1 in range(len(sky_map)):
    x1, y1 = sky_map[gid_1]
    for gid_2 in range(gid_1, len(sky_map)):
        x2, y2 = sky_map[gid_2]
        total += abs(x1 - x2) + abs(y1 - y2)

print(total)
