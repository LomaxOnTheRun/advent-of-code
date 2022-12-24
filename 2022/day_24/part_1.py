# Start time: 09:22
# End time: 14:11

import aocd

from perf_utils import timeit, print_logged_times

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

import time

setup_start_time = time.perf_counter()

Coord = tuple[int, int]

DIRS = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0), " ": (0, 0)}
COORD, DIR = "COORD", "DIR"

INITIAL_BLIZZARDS = []
for y, line in enumerate(data.split()[1:-1]):
    for x, char in enumerate(line[1:-1]):
        if char in "^>v<":
            INITIAL_BLIZZARDS.append(((x, y), char))

WIDTH = len(data.split()[0]) - 2
HEIGHT = len(data.split()) - 2

START_COORD = (0, -1)
END_COORD = (WIDTH - 1, HEIGHT)


def print_blizzards(blizzards, elves_coord):
    if elves_coord == START_COORD:
        print("#E" + "#" * WIDTH)
    else:
        print("#." + "#" * WIDTH)

    for y in range(HEIGHT):
        row = "#"
        for x in range(WIDTH):
            if (x, y) in blizzards:
                row += "B"
            elif (x, y) == elves_coord:
                row += "E"
            else:
                row += "."
        print(row + "#")

    if elves_coord == END_COORD:
        print("#" * WIDTH + "E#")
    else:
        print("#" * WIDTH + ".#")

    print()


def get_blizzards(minute: int) -> set[Coord]:
    blizzards = set()
    for (x0, y0), dir in INITIAL_BLIZZARDS:
        dx, dy = DIRS[dir]
        new_x = (x0 + (dx * minute)) % WIDTH
        new_y = (y0 + (dy * minute)) % HEIGHT
        blizzards.add((new_x, new_y))
    return blizzards


BLIZZARDS = {minute: get_blizzards(minute) for minute in range(500)}

NEXT_COORDS = {}

setup_end_time = time.perf_counter()


@timeit
def get_next_coord(coord: Coord, dir: Coord) -> Coord:
    if (coord, dir) in NEXT_COORDS:
        return NEXT_COORDS[(coord, dir)]
    next_x = coord[0] + DIRS[dir][0]
    next_y = coord[1] + DIRS[dir][1]
    NEXT_COORDS[(coord, dir)] = (next_x, next_y)
    return (next_x, next_y)


@timeit
def can_move_to_coord(next_blizzards: set[Coord], next_coord: Coord) -> bool:
    next_x, next_y = next_coord

    # Don't walk into walls...
    if next_x < 0 or next_x >= WIDTH or next_y < 0 or next_y >= HEIGHT:
        # ... except for start and end coords
        if next_coord not in (START_COORD, END_COORD):
            return False

    # Don't walk into blizzards
    if next_coord in next_blizzards:
        return False

    return True


@timeit
def get_score(minute: int, coord: Coord) -> int:
    """
    Low score is better.
    """
    # score = minute
    # score = 0
    score = minute // 2
    score += END_COORD[0] - coord[0]
    score += END_COORD[1] - coord[1]
    return score


@timeit
def get_next_coord_to_try(steps_to_try):
    _, current_minute, current_coord = heapq.heappop(steps_to_try)
    return current_minute, current_coord


@timeit
def get_next_info(steps_tried: set, current_minute: int, current_coord: Coord):
    next_minute = current_minute + 1
    next_blizzards = BLIZZARDS[next_minute]
    return next_minute, next_blizzards


@timeit
def add_step_to_try(steps_to_try, score, next_minute, next_coord):
    heapq.heappush(steps_to_try, (score, next_minute, next_coord))


@timeit
def add_steps_to_try(
    current_coord: Coord,
    dir: str,
    steps_tried: set,
    steps_to_try: list,
    next_minute: int,
) -> bool:
    next_coord = get_next_coord(current_coord, dir)

    # Check for win condition
    if next_coord == END_COORD:
        return True

    # Ignore if we've already tried this step
    if (next_minute, next_coord) in steps_tried:
        return

    # Otherwise add next possible steps
    if can_move_to_coord(next_blizzards, next_coord):
        score = get_score(next_minute, next_coord)
        add_step_to_try(steps_to_try, score, next_minute, next_coord)
        steps_tried.add((current_minute, current_coord))

    return False  # End found


start_time = time.perf_counter()

import heapq

steps_to_try = [(0, 0, START_COORD)]
steps_tried = set()

max_minute = 0
best_time = 1e9
i = 0
keep_going = True
while steps_to_try and keep_going:
    i += 1

    current_minute, current_coord = get_next_coord_to_try(steps_to_try)

    if current_minute > best_time:
        continue

    next_minute, next_blizzards = get_next_info(
        steps_tried, current_minute, current_coord
    )

    # This is good enough to get the answer for me
    if i == 1e8:
        break

    for dir in "v> <^":

        end_found = add_steps_to_try(
            current_coord, dir, steps_tried, steps_to_try, next_minute
        )

        if end_found and next_minute < best_time:
            best_time = next_minute

print(best_time)

end_time = time.perf_counter()

# print_logged_times()
# print(f"\nTotal setup time: {setup_end_time - setup_start_time:.2f}s")
# print(f"Total run time: {end_time - start_time:.2f}s")
