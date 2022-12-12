# Start time: 06:45
# End time: 07:23

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
            start_coord = (y, x)
            frontier.append(coord)
            heights[coord] = ord("a")
        elif char == "E":
            end_coord = (y, x)
            heights[coord] = ord("z")
        else:
            heights[coord] = ord(char)

dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

# print(heights)
# print(frontier)

while True:
    # for _ in range(10):
    # print(f"Epoch {_}")
    # Update frontier
    old_coord = frontier.pop(0)
    for dir in dirs:
        new_coord = (old_coord[0] + dir[0], old_coord[1] + dir[1])
        # print(new_coord)
        if new_coord in heights:
            # print(new_coord)
            if new_coord not in previous:
                # print(new_coord)
                if heights[new_coord] - heights[old_coord] < 2:
                    frontier.append(new_coord)
                    previous[new_coord] = old_coord

    # print(frontier)

    if end_coord in frontier:
        break

# print(previous)

path = [end_coord]
while path[-1] != start_coord:
    previous_coord = previous[path[-1]]
    path.append(previous_coord)

print(len(path) - 1)
