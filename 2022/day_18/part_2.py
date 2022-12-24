# Start time: 08:11
# End time: 08:19

import aocd

data = """1,1,1
2,1,1"""

data = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

data = aocd.get_data(year=2022, day=18)

drops = {eval(f"({line})") for line in data.split()}

DIRS = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]

all_x = [x for x, _, _ in drops]
all_y = [y for _, y, _ in drops]
all_z = [z for _, _, z in drops]

min_x = min(all_x)
max_x = max(all_x)
min_y = min(all_y)
max_y = max(all_y)
min_z = min(all_z)
max_z = max(all_z)

coord = (min_x - 1, min_y - 1, min_z - 1)

coords_to_check = [coord]
bubble = {coord}
bubble_sides = 0

while coords_to_check:
    coord = coords_to_check.pop(0)

    # Try to extend the bubble
    for dir in DIRS:
        adjacent = (coord[0] + dir[0], coord[1] + dir[1], coord[2] + dir[2])

        x, y, z = adjacent
        if x < min_x - 1 or x > max_x + 1:
            continue
        if y < min_y - 1 or y > max_y + 1:
            continue
        if z < min_z - 1 or z > max_z + 1:
            continue

        if adjacent in bubble:
            continue
        if adjacent in coords_to_check:
            continue

        if adjacent in drops:
            bubble_sides += 1
            continue

        coords_to_check.append(adjacent)
        bubble.add(adjacent)

print(bubble_sides)
