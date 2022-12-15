# Start time: 07:17
# End time: 07:32

import aocd

data = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

data = aocd.get_data(year=2022, day=14)

walls = set()
for corners_str in data.split("\n"):
    corners = [eval(f"({coord})") for coord in corners_str.split(" -> ")]
    for i in range(len(corners) - 1):
        old, new = corners[i : i + 2]
        if old[0] == new[0]:
            for y in range(min(old[1], new[1]), max(old[1], new[1]) + 1):
                walls.add((old[0], y))
        else:
            for x in range(min(old[0], new[0]), max(old[0], new[0]) + 1):
                walls.add((x, old[1]))

settled_sand = set()
max_depth = max([depth for _, depth in walls])

while (500, 0) not in settled_sand:
    sand_x, sand_y = 500, 0
    taken_space = walls | settled_sand
    while True:
        if sand_y == max_depth + 1:
            settled_sand.add((sand_x, sand_y))
            break

        if (sand_x, sand_y + 1) not in taken_space:
            sand_y += 1
        elif (sand_x - 1, sand_y + 1) not in taken_space:
            sand_x -= 1
            sand_y += 1
        elif (sand_x + 1, sand_y + 1) not in taken_space:
            sand_x += 1
            sand_y += 1
        else:
            settled_sand.add((sand_x, sand_y))
            break

print(len(settled_sand))
