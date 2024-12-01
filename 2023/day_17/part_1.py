# Start time: 10:46
# End time:

import aocd

data = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

# data = """11199
# 991999
# 991999
# 991999
# 99111"""
#
# data = """119
# 919
# 919
# 919
# 911"""
#
# data = """11
# 91
# 11
# 19
# 11"""
#
# data = """121
# 231
# 211"""

# data = """111991111
# 991111991
# 999999991
# 999999911
# 111991119
# 191111999
# 199999999
# 199999999
# 119999111
# 911111191"""

# data = """112111
# 211121"""

data = """
241343231
321545353
""".strip()

# data = """
# 241343
# 321545
# """.strip()

# data = aocd.get_data(year=2023, day=17)


def get_losses(data):
    losses = {}  # {(x, y): loss}
    for y, line in enumerate(data.splitlines()):
        for x, loss_str in enumerate(line):
            losses[(x, y)] = int(loss_str)
    return losses


def get_distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


def is_straight_line(neighbour, path_so_far):
    for prev in path_so_far[::-1]:
        dx = abs(neighbour[0] - prev[0])
        dy = abs(neighbour[1] - prev[1])
        if dx != 0 and dy != 0:
            return False
        if dx == 0 and dy > 3 or dy == 0 and dx > 3:
            return True
    return False


def get_line_neighbours(current_x, current_y, dx, dy, losses):
    line_neighbours = []
    x, y, loss = current_x, current_y, 0
    # for i in range(3):
    for i in range(1):
        x, y = x + dx, y + dy
        if (x, y) not in losses:
            continue
        if (x, y) == (current_x, current_y):
            continue
        loss += losses[(x, y)]
        line_neighbours.append(((x, y), loss))
    return line_neighbours


def get_neighbours(current, prev, losses):
    neighbours = []
    # neighbours += get_line_neighbours(current_x, current_y, -1, 0, losses)
    # neighbours += get_line_neighbours(current_x, current_y, 0, -1, losses)
    # neighbours += get_line_neighbours(current_x, current_y, 1, 0, losses)
    # neighbours += get_line_neighbours(current_x, current_y, 0, 1, losses)

    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        x, y = current[0] + dx, current[1] + dy
        if (x, y) not in losses:
            continue
        if (x, y) == prev:
            continue
        neighbours.append(((x, y), losses[(x, y)]))

    return neighbours


def print_map(path, losses):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (x, y) in path:
                print(".", end="")
            else:
                print(losses[(x, y)], end="")
        print()


def get_lowest_path(losses, start_xy, end_xy):
    # Keep track of lowest
    current_lowest_path_loss = 1e10
    current_lowest_path = []

    # Create a set of all the points we need to check
    frontier = {
        (start_xy, start_xy): (0, [(0, 0)])
    }  # {(prev_xy, current_xy, loss): path}
    # Create a list of all the points we have checked
    closed_losses = {}  # {(prev_xy, current_xy): loss}

    # Loop until we have checked all the points
    step = 0
    while frontier:
        step += 1
        print("\nSTEP:", step)
        print("\nFrontier")
        for xy, (l, p) in frontier.items():
            print(xy, l)
        print()

        # Get next to try
        prev, current = list(frontier.keys())[0]
        loss, path_so_far = frontier.pop((prev, current))

        print("Popped:", prev, current, loss)
        print("Path so far:", path_so_far)
        print()

        print_map(path_so_far, losses)
        print()

        # If we have reached the end, return the path
        if current == end_xy:
            if loss < current_lowest_path_loss:
                current_lowest_path_loss = loss
                current_lowest_path = path_so_far
                print("current_lowest_path", current_lowest_path)
                print("loss", loss)

        # Add the current point to the closed list
        if (prev, current) not in closed_losses:
            closed_losses[(prev, current)] = loss
        elif closed_losses[(prev, current)] > loss:
            closed_losses[(prev, current)] = loss
        # Get the neighbours of the current point
        neighbours = get_neighbours(current, prev, losses)

        print("Neighbours", neighbours)

        # Loop through the neighbours
        for neighbour, neighbour_loss in neighbours:
            total_loss = loss + neighbour_loss
            print("\nNeighbour:", neighbour, total_loss)
            print("Total loss", total_loss)

            # Ignore any neighbours that make a long straight line
            if is_straight_line(neighbour, path_so_far):
                print("Is straight, skipping")
                continue

            # If the neighbour is in the closed list, skip it
            if (current, neighbour) in closed_losses:
                print("Neighbour in closed:", neighbour)
                if closed_losses[(current, neighbour)] <= total_loss:
                    print(
                        "Closed neighbour is better:",
                        closed_losses[(current, neighbour)],
                    )
                    continue
                else:
                    print("Current neighbour better than closed")

            # If the neighbour is not in the open list, add it
            if (current, neighbour) not in frontier:
                frontier[(current, neighbour)] = (total_loss, path_so_far + [neighbour])
                print("Frontier new:", current, neighbour, total_loss)
            elif frontier[(current, neighbour)][0] > total_loss:
                frontier[(current, neighbour)] = (total_loss, path_so_far + [neighbour])
                print("Frontier update:", current, neighbour, total_loss)
            else:
                print(
                    "Frontier is better:",
                    current,
                    neighbour,
                    total_loss,
                    frontier[(current, neighbour)][0],
                )

    # We have checked all the points
    return current_lowest_path_loss, current_lowest_path


def get_path_heat_loss(path, losses):
    total = 0
    for xy in path:
        total += losses[xy]
    return total


HEIGHT = len(data.splitlines())
WIDTH = len(data.splitlines()[0])

losses = get_losses(data)
heat_loss, path = get_lowest_path(losses, (0, 0), (WIDTH - 1, HEIGHT - 1))
print(heat_loss)
print(path)

for y in range(HEIGHT):
    for x in range(WIDTH):
        if (x, y) in path:
            print(".", end="")
        else:
            print(losses[(x, y)], end="")
    print()
