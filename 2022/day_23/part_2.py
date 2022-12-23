# Start time: 09:57
# End time: 10:00

import aocd

data = """.....
..##.
..#..
.....
..##.
....."""

data = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""

data = aocd.get_data(year=2022, day=23)


def should_move(elf_x: int, elf_y: int, elves: dict) -> bool:
    for dx, dy in ALL_DIRS:
        if (elf_x + dx, elf_y + dy) in elves:
            return True
    return False


def pick_new_coord(elf_x, elf_y, elves, dir_order) -> tuple[int, int]:
    if not should_move(elf_x, elf_y, elves):
        return (elf_x, elf_y)

    for look_dir in dir_order:
        look_coords = []
        for dx, dy in DIRS[look_dir][LOOK]:
            look_coords.append((elf_x + dx, elf_y + dy))
        if all([coord not in elves for coord in look_coords]):
            move_dx, move_dy = DIRS[look_dir][MOVE]
            return (elf_x + move_dx, elf_y + move_dy)

    # ASSUMPTION: If all directions are full, don't move
    return (elf_x, elf_y)


def count_empty_tiles(elves: dict) -> None:
    x_coords = [x for x, _ in elves]
    min_x = min(x_coords)
    max_x = max(x_coords)
    y_coords = [y for _, y in elves]
    min_y = min(y_coords)
    max_y = max(y_coords)
    return ((max_x - min_x + 1) * (max_y - min_y + 1)) - len(elves)


def print_elves(elves: dict) -> None:
    x_coords = [x for x, _ in elves]
    min_x = min(x_coords)
    max_x = max(x_coords)
    y_coords = [y for _, y in elves]
    min_y = min(y_coords)
    max_y = max(y_coords)
    for y in range(max_y, min_y - 1, -1):
        row = ""
        for x in range(min_x, max_x + 1):
            if (x, y) in elves:
                row += "#"
            else:
                row += "."
        print(row)
    print()


N, S, W, E, NO_MOVE = "NSWE-"
LOOK = "LOOK"
MOVE = "MOVE"

DIRS = {
    N: {LOOK: [(-1, 1), (0, 1), (1, 1)], MOVE: (0, 1)},
    S: {LOOK: [(-1, -1), (0, -1), (1, -1)], MOVE: (0, -1)},
    W: {LOOK: [(-1, -1), (-1, 0), (-1, 1)], MOVE: (-1, 0)},
    E: {LOOK: [(1, -1), (1, 0), (1, 1)], MOVE: (1, 0)},
    NO_MOVE: {MOVE: (0, 0)},
}
ALL_DIRS = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if x or y]

initial_height = len(data.split())
elves = set()
for y, line in enumerate(data.split()):
    for x, char in enumerate(line):
        if char == "#":
            elves.add((x, initial_height - y - 1))

dir_order = [N, S, W, E]

num_rounds = 0
while True:
    num_rounds += 1

    proposed_new_coords = {}
    for elf in elves:
        proposed_new_coords[elf] = pick_new_coord(*elf, elves, dir_order)

    if set(proposed_new_coords.values()) == elves:
        break

    new_coords = set()
    collisions = set()
    for new_coord in proposed_new_coords.values():
        if new_coord in new_coords:
            collisions.add(new_coord)
        new_coords.add(new_coord)

    new_elves = set()
    for elf in elves:
        if proposed_new_coords[elf] in collisions:
            # Stay at same coord
            new_elves.add(elf)
        else:
            new_elves.add(proposed_new_coords[elf])
    elves = new_elves

    dir_order.append(dir_order.pop(0))

print(num_rounds)
