# 42 lines

import aocd

data = aocd.get_data(year=2022, day=12)

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

frontier = []
heights = {}
previous = {}
lowest_coords = []
for y, line in enumerate(data.split()):
    for x, char in enumerate(line):
        coord = (y, x)
        if char == "S":
            true_start_coord = (y, x)
            heights[coord] = ord("a")
        elif char == "E":
            end_coord = (y, x)
            frontier.append(coord)
            heights[coord] = ord("z")
        else:
            heights[coord] = ord(char)

        if char in ["S", "a"]:
            lowest_coords.append((y, x))

while frontier:
    old_coord = frontier.pop(0)
    for dir in DIRS:
        new_coord = (old_coord[0] + dir[0], old_coord[1] + dir[1])
        if new_coord in heights:
            if new_coord not in previous:
                if heights[old_coord] - heights[new_coord] < 2:
                    frontier.append(new_coord)
                    previous[new_coord] = old_coord

path_lengths = {}
for start_coord in lowest_coords:
    path = [start_coord]
    while path[-1] != end_coord:
        if path[-1] not in previous:
            break
        previous_coord = previous[path[-1]]
        path.append(previous_coord)
    if len(path) > 1:
        path_lengths[start_coord] = len(path) - 1

# Part 1
print(path_lengths[true_start_coord])

# Part 2
print(min(path_lengths.values()))
