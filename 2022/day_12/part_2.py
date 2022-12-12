# Start time: 07:23
# End time: 07:44

import aocd

data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

data = aocd.get_data(year=2022, day=12)


frontier = []
heights = {}
previous = {}
for y, line in enumerate(data.split()):
    for x, char in enumerate(line):
        coord = (y, x)
        if char == "S":
            heights[coord] = ord("a")
        elif char == "E":
            end_coord = (y, x)
            frontier.append(coord)
            heights[coord] = ord("z")
        else:
            heights[coord] = ord(char)

dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

while frontier:
    old_coord = frontier.pop(0)
    for dir in dirs:
        new_coord = (old_coord[0] + dir[0], old_coord[1] + dir[1])
        if new_coord in heights:
            if new_coord not in previous:
                if heights[old_coord] - heights[new_coord] < 2:
                    frontier.append(new_coord)
                    previous[new_coord] = old_coord

start_coords = []
for y, line in enumerate(data.split()):
    for x, char in enumerate(line):
        if char in ["S", "a"]:
            start_coords.append((y, x))

path_lengths = []
for start_coord in start_coords:
    path = [start_coord]
    while path[-1] != end_coord:
        if path[-1] not in previous:
            break
        previous_coord = previous[path[-1]]
        path.append(previous_coord)
    if len(path) > 1:
        path_lengths.append(len(path) - 1)

print(min(path_lengths))
