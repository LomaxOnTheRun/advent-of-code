# Start time: 11:59
# End time: 12:24

import aocd, math

data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

data = aocd.get_data(year=2024, day=6)

DIRS = {"v": 0, ">": math.pi * 0.5, "^": math.pi, "<": math.pi * 1.5}

ground, obstacles = set(), set()
guard_pos, guard_dir = (), 0  # (x, y), 0-2pi
for y, row in enumerate(data.splitlines()):
    for x, symbol in enumerate(row):
        if symbol == ".":
            ground.add((x, y))
        elif symbol == "#":
            obstacles.add((x, y))
        else:
            guard_pos = (x, y)
            guard_dir = DIRS[symbol]
            ground.add((x, y))

path = set()
while guard_pos in ground:
    path.add(guard_pos)
    x = guard_pos[0] + int(math.sin(guard_dir))
    y = guard_pos[1] + int(math.cos(guard_dir))
    if (x, y) in obstacles:
        guard_dir = (guard_dir - (math.pi / 2)) % (math.pi * 2)
        x = guard_pos[0] + int(math.sin(guard_dir))
        y = guard_pos[1] + int(math.cos(guard_dir))
    guard_pos = (x, y)

print(len(path))
