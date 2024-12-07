import aocd

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

DXY = [(0, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]
DIRS = ["UP", "RIGHT", "DOWN", "LEFT", "UP"]


def get_path(guard_pos, guard_dir, obstacles):
    path = {(guard_pos, guard_dir)}
    while True:
        new_guard_dir = guard_dir
        x = guard_pos[0] + guard_dir[0]
        y = guard_pos[1] + guard_dir[1]
        if (x, y) in obstacles:
            new_guard_dir = DXY[DXY.index(guard_dir) + 1]
            x = guard_pos[0] + new_guard_dir[0]
            y = guard_pos[1] + new_guard_dir[1]
        new_guard_pos = (x, y)

        if new_guard_pos not in ground:
            return path
        if (new_guard_pos, new_guard_dir) in path:
            return path

        guard_pos = new_guard_pos
        guard_dir = new_guard_dir
        path.add((new_guard_pos, guard_dir))


ground, obstacles = set(), set()
guard_pos, guard_dir = (), ()  # (x, y), (dx, dy)
for y, row in enumerate(data.splitlines()):
    for x, symbol in enumerate(row):
        if symbol == ".":
            ground.add((x, y))
        elif symbol == "#":
            obstacles.add((x, y))
        else:
            guard_pos = (x, y)
            guard_dir = DXY[0]
            ground.add((x, y))

original_path = get_path(guard_pos, guard_dir, obstacles)


def get_next_turning_point(guard_pos, guard_dir, obstacles):
    """
    Get the next turning point from the current position.
    """
    gx, gy = guard_pos
    if guard_dir == "UP":
        # print("UP")
        # print("Next obstacle:", [(x, y) for x, y in obstacles if x == gx and y < gy])
        gy = max([y for x, y in obstacles if x == gx and y < gy]) + 1
        # print("New gy:", gy)
    elif guard_dir == "RIGHT":
        # print("RIGHT")
        # print("Next obstacle:", [(x, y) for x, y in obstacles if y == gy and x > gx])
        gx = min([x for x, y in obstacles if y == gy and x > gx]) - 1
    elif guard_dir == "DOWN":
        # print("DOWN")
        # print("Next obstacle:", [(x, y) for x, y in obstacles if x == gx and y > gy])
        gy = min([y for x, y in obstacles if x == gx and y > gy]) - 1
    elif guard_dir == "LEFT":
        # print("LEFT")
        # print("Next obstacle:", [(x, y) for x, y in obstacles if y == gy and x < gx])
        gx = max([x for x, y in obstacles if y == gy and x < gx]) + 1
    else:
        raise Exception(f"Unknown direction: {guard_dir}")
    return gx, gy


def is_loop(guard_pos, guard_dir, obstacles):
    # print("Obstacles:", sorted(obstacles))
    # print()

    seen = list()
    x, y = guard_pos
    # print("Guard pos:", (x, y))
    step = 0
    while True:
        step += 1
        # print("Step:", step)
        try:
            # print("Trying...")
            x, y = get_next_turning_point((x, y), guard_dir, obstacles)
        except ValueError:
            return False

        # print("Guard pos:", (x, y))

        guard_dir = DIRS[DIRS.index(guard_dir) + 1]
        if ((x, y), guard_dir) in seen:
            return True
        seen.append(((x, y), guard_dir))
        # print("Seen positions:", seen)
        # print()


new_obstacles = sorted(set(pos for pos, _ in original_path))

total = 0
for new_obstacle in new_obstacles:
    if is_loop(guard_pos, "UP", obstacles | {new_obstacle}):
        total += 1

print(total)
