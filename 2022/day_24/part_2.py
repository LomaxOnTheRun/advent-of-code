# Start time: 14:11
# End time: 15:06

import aocd, heapq


data = """#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#"""

data = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""

data = aocd.get_data(year=2022, day=24)


Coord = tuple[int, int]


DIRS = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0), " ": (0, 0)}
WIDTH = len(data.split()[0]) - 2
HEIGHT = len(data.split()) - 2

START_COORD = (0, -1)
END_COORD = (WIDTH - 1, HEIGHT)

INITIAL_BLIZZARDS = []
for y, line in enumerate(data.split()[1:-1]):
    for x, char in enumerate(line[1:-1]):
        if char in "^>v<":
            INITIAL_BLIZZARDS.append(((x, y), char))


def get_blizzards(
    minute: int, initial_blizzards: list[tuple[Coord, str]]
) -> set[Coord]:
    blizzards = set()
    for (x0, y0), dir in initial_blizzards:
        dx, dy = DIRS[dir]
        new_x = (x0 + (dx * minute)) % WIDTH
        new_y = (y0 + (dy * minute)) % HEIGHT
        blizzards.add((new_x, new_y))
    return blizzards


def get_new_initial_blizzards(
    minute: int, initial_blizzards: list[tuple[Coord, str]]
) -> list[tuple[Coord, str]]:
    blizzards = []
    for (x0, y0), dir in initial_blizzards:
        dx, dy = DIRS[dir]
        new_x = (x0 + (dx * minute)) % WIDTH
        new_y = (y0 + (dy * minute)) % HEIGHT
        blizzards.append(((new_x, new_y), dir))
    return blizzards


def get_next_coord(coord: Coord, dir: Coord) -> Coord:
    next_x = coord[0] + DIRS[dir][0]
    next_y = coord[1] + DIRS[dir][1]
    return (next_x, next_y)


def can_move_to_coord(
    next_blizzards: set[Coord], next_coord: Coord, start_coord: Coord, end_coord: Coord
) -> bool:
    next_x, next_y = next_coord

    # Don't walk into walls...
    if next_x < 0 or next_x >= WIDTH or next_y < 0 or next_y >= HEIGHT:
        # ... except for start and end coords
        if next_coord not in (start_coord, end_coord):
            return False

    # Don't walk into blizzards
    if next_coord in next_blizzards:
        return False

    return True


def get_distance_to_end(coord: Coord, end_coord: Coord) -> int:
    return (end_coord[0] - coord[0]) + (end_coord[1] - coord[1])


def get_score(minute: int, coord: Coord, end_coord: Coord) -> int:
    """
    Low score is better.
    """
    return get_distance_to_end(coord, end_coord) + minute // 2


def get_next_coord_to_try(steps_to_try: list) -> tuple[int, Coord]:
    _, current_minute, current_coord = heapq.heappop(steps_to_try)
    return current_minute, current_coord


def get_next_blizzards(
    next_minute: int, blizzards: dict[int, set[Coord]]
) -> set[Coord]:
    return blizzards[next_minute]


def add_step_to_try(
    steps_to_try: list, score: int, next_minute: int, next_coord: Coord
) -> None:
    heapq.heappush(steps_to_try, (score, next_minute, next_coord))


def add_steps_to_try(
    next_coord: Coord,
    steps_tried: set,
    steps_to_try: list,
    next_minute: int,
    start_coord: Coord,
    end_coord: Coord,
    next_blizzards: set[Coord],
) -> bool:

    # Check for win condition
    if next_coord == end_coord:
        return True

    # Ignore if we've already tried this step
    if (next_minute, next_coord) in steps_tried:
        return

    # Otherwise add next possible steps
    if can_move_to_coord(next_blizzards, next_coord, start_coord, end_coord):
        score = get_score(next_minute, next_coord, end_coord)
        add_step_to_try(steps_to_try, score, next_minute, next_coord)
        steps_tried.add((next_minute, next_coord))

    return False  # End found


def go_through_blizzards(
    start_coord: Coord,
    end_coord: Coord,
    blizzards: dict[int, set[Coord]],
    dirs_to_try: str,
) -> int:
    steps_to_try = [(0, 0, start_coord)]
    steps_tried = set()

    best_time = 1e10
    while steps_to_try:
        current_minute, current_coord = get_next_coord_to_try(steps_to_try)

        remaining_distance = get_distance_to_end(current_coord, end_coord)
        if current_minute + remaining_distance > best_time:
            continue

        next_minute = current_minute + 1
        next_blizzards = get_next_blizzards(next_minute, blizzards)

        for dir in dirs_to_try:
            next_coord = get_next_coord(current_coord, dir)
            end_found = add_steps_to_try(
                next_coord,
                steps_tried,
                steps_to_try,
                next_minute,
                start_coord,
                end_coord,
                next_blizzards,
            )

            if end_found and next_minute < best_time:
                best_time = next_minute

    return best_time


best_times = []

# Going to the exit
initial_blizzards = INITIAL_BLIZZARDS
blizzards = {minute: get_blizzards(minute, initial_blizzards) for minute in range(1000)}
best_time = go_through_blizzards(START_COORD, END_COORD, blizzards, "v> <^")
best_times.append(best_time)

# Going back to the start
initial_blizzards = get_new_initial_blizzards(best_times[-1], initial_blizzards)
blizzards = {minute: get_blizzards(minute, initial_blizzards) for minute in range(1000)}
best_time = go_through_blizzards(END_COORD, START_COORD, blizzards, "^< >v")
best_times.append(best_time)

# And then back to end
initial_blizzards = get_new_initial_blizzards(best_times[-1], initial_blizzards)
blizzards = {minute: get_blizzards(minute, initial_blizzards) for minute in range(1000)}
best_time = go_through_blizzards(START_COORD, END_COORD, blizzards, "v> <^")
best_times.append(best_time)

print(sum(best_times))
