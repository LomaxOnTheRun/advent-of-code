# Start time: 11:06
# End time: 11:43

import aocd

data = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

data = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

data = aocd.get_data(year=2024, day=15)


def print_map(walls, boxes, robot) -> None:
    max_x = max(x for x, _ in walls)
    max_y = max(y for _, y in walls)
    print()
    for y in range(max_y + 1):
        line = ""
        for x in range(max_x + 1):
            if (x, y) in walls:
                line += "#"
            elif (x, y) in boxes:
                line += "O"
            elif (x, y) == robot:
                line += "@"
            else:
                line += "."
        print(line)


def get_warehouse_info(warehouse: str) -> tuple[set, set, tuple]:
    walls, boxes, robot = set(), set(), ()
    for y, row in enumerate(warehouse.split()):
        for x, char in enumerate(row):
            if char == "#":
                walls.add((x, y))
            elif char == "O":
                boxes.add((x, y))
            elif char == "@":
                robot = (x, y)
    return walls, boxes, robot


warehouse, instructions = data.split("\n\n")
walls, boxes, robot = get_warehouse_info(warehouse)

DIRS = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}
for step in instructions.replace("\n", ""):
    dx, dy = DIRS[step]

    # print_map(walls, boxes, robot)

    next_xy = (robot[0] + dx, robot[1] + dy)
    boxes_to_move = []
    while next_xy in boxes:
        boxes_to_move.append(next_xy)
        next_xy = (next_xy[0] + dx, next_xy[1] + dy)

    if next_xy in walls:
        # Blocked by wall, nothing moves
        continue

    for box_x, box_y in boxes_to_move:
        boxes.remove((box_x, box_y))
    for box_x, box_y in boxes_to_move:
        boxes.add((box_x + dx, box_y + dy))
    robot = (robot[0] + dx, robot[1] + dy)

total = 0
for box_x, box_y in boxes:
    total += (100 * box_y) + box_x
print(total)
