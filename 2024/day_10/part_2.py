# Start time: 19:27
# End time: 19:30

import aocd

data = """0123
1234
8765
9876"""

data = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

data = aocd.get_data(year=2024, day=10)

coords = {}
for max_y, row in enumerate(data.split()):
    for max_x, val in enumerate(row):
        coords[(max_x, max_y)] = int(val)


def get_trail_ends(x, y, current_val, num_routes):
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        next_xy = next_x, next_y = x + dx, y + dy
        if next_x < 0 or next_y < 0 or next_x > max_x or next_y > max_y:
            continue

        if coords[next_xy] != current_val + 1:
            continue

        if coords[next_xy] == 9:
            num_routes += 1
        else:
            num_routes = get_trail_ends(next_x, next_y, current_val + 1, num_routes)

    return num_routes


num_trailheads = 0
for (x, y), val in coords.items():
    if val == 0:
        num_trailheads += get_trail_ends(x, y, 0, 0)

print(num_trailheads)
