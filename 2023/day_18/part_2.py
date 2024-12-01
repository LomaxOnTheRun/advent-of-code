# Start time: 07:10
# End time:

import aocd

data = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

# data = aocd.get_data(year=2023, day=18)

DIR = {"0": "R", "1": "D", "2": "L", "3": "U"}
DXY = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}

hole = {(0, 0)}
x, y = 0, 0
for line in data.splitlines():
    print(line)
    hex_str = line.split(" ")[2]
    d = DIR[hex_str[7]]
    num_steps = int(hex_str[2:7], 16)

    for _ in range(int(num_steps)):
        dx, dy = DXY[d]
        x, y = x + dx, y + dy
        hole.add((x, y))

all_x = [x for x, _ in hole]
all_y = [y for _, y in hole]
min_x, max_x = min(all_x), max(all_x)
min_y, max_y = min(all_y), max(all_y)

frontier = {(min_x - 1, min_y - 1)}
outside_hole = set()
while frontier:
    x, y = frontier.pop()
    outside_hole.add((x, y))
    for dx, dy in DXY.values():
        new_xy = (x + dx, y + dy)
        if new_xy in hole:
            continue
        if new_xy in outside_hole:
            continue
        if x + dx < min_x - 1 or x + dx > max_x + 1:
            continue
        if y + dy < min_y - 1 or y + dy > max_y + 1:
            continue
        frontier.add(new_xy)


hole_size = 0
for y in range(min_y - 1, max_y + 1):
    for x in range(min_x - 1, max_x + 1):
        if (x, y) not in outside_hole:
            hole_size += 1

print(hole_size)
