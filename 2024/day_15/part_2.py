# Start time: 13:57
# End time:

import aocd

data = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

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
                line += "X"
            elif (x, y) == robot:
                line += "@"
            else:
                line += "."
        print(line)


def get_warehouse_info(warehouse: str) -> tuple[set, set, dict, tuple]:
    walls, boxes, box_pairs, robot = set(), set(), {}, ()
    for y, row in enumerate(warehouse.split()):
        for x, char in enumerate(row):
            if char == "#":
                walls.add((2 * x, y))
                walls.add(((2 * x) + 1, y))
            elif char == "O":
                boxes.add((2 * x, y))
                boxes.add(((2 * x) + 1, y))
                box_pairs[(2 * x, y)] = ((2 * x) + 1, y)
                box_pairs[((2 * x) + 1, y)] = (2 * x, y)
            elif char == "@":
                robot = (2 * x, y)
    return walls, boxes, box_pairs, robot


def get_next_boxes_to_move(current_boxes, dx, dy, boxes, box_pairs, walls):
    next_boxes_to_move = set()
    for x, y in current_boxes:
        next_xy = (x + dx, y + dy)
        if next_xy in walls:
            return None
        if next_xy in boxes:
            next_boxes_to_move |= {next_xy, box_pairs[next_xy]}
    next_boxes_to_move -= current_boxes
    return next_boxes_to_move


def get_boxes_to_move(robot, dx, dy, boxes, box_pairs, walls):
    next_xy = next_x, next_y = robot[0] + dx, robot[1] + dy

    if (next_x, next_y) in walls:
        return None
    if (next_x, next_y) not in boxes:
        return set()

    boxes_to_move = set()
    next_boxes = {next_xy, box_pairs[next_xy]}
    while next_boxes != set():
        boxes_to_move |= next_boxes
        next_boxes = get_next_boxes_to_move(next_boxes, dx, dy, boxes, box_pairs, walls)
        if next_boxes is None:
            # Wall hit, no boxes can move
            return None

    return boxes_to_move


def move_boxes(boxes_to_move, boxes, box_pairs, dx, dy):
    new_box_pairs = {}
    boxes_to_remove = set()
    boxes_to_add = set()
    for xy in boxes_to_move:
        new_xy = (xy[0] + dx, xy[1] + dy)
        new_pair_xy = (box_pairs[xy][0] + dx, box_pairs[xy][1] + dy)
        new_box_pairs[new_xy] = new_pair_xy

        del box_pairs[xy]

        boxes_to_remove.add(xy)
        boxes_to_add.add(new_xy)

    boxes -= boxes_to_remove
    boxes |= boxes_to_add
    box_pairs |= new_box_pairs


warehouse, instructions = data.split("\n\n")
walls, boxes, box_pairs, robot = get_warehouse_info(warehouse)

DIRS = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}
for step in instructions.replace("\n", ""):
    # print(f"Move {step}:")
    dx, dy = DIRS[step]

    # print_map(walls, boxes, robot)

    boxes_to_move = get_boxes_to_move(robot, dx, dy, boxes, box_pairs, walls)
    if boxes_to_move is None:
        continue

    move_boxes(boxes_to_move, boxes, box_pairs, dx, dy)
    robot = (robot[0] + dx, robot[1] + dy)

# print_map(walls, boxes, robot)

total = 0
for (x1, y1), (x2, y2) in box_pairs.items():
    if x1 < x2:
        total += (100 * y1) + x1
print(total)
