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

# data = aocd.get_data(year=2023, day=17)


def get_losses(data):
    losses = {}  # {(x, y): loss}
    for y, line in enumerate(data.splitlines()):
        for x, loss_str in enumerate(line):
            losses[(x, y)] = int(loss_str)
    return losses


def get_distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


def is_straight_line(neighbour, current, came_from):
    cx, cy = current
    nx, ny = neighbour
    dx, dy = nx - cx, ny - cy
    return (
        (cx, cy) in came_from
        and (cx - dx, cy - dy) in came_from
        and came_from[(cx, cy)] == (cx - dx, cy - dy)
        and came_from[(cx - dx, cy - dy)]
        == (
            cx - dx - dx,
            cy - dy - dy,
        )
    )


def get_neighbours(x, y, losses):
    neighbours = []
    dx_dy = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for dx, dy in dx_dy:
        if (x + dx, y + dy) in losses:
            neighbours.append((x + dx, y + dy))
    return neighbours


def get_lowest_f_score(open_list, f_score):
    lowest_xy = open_list[0]
    lowest_f_score = f_score[lowest_xy]
    for xy in open_list[1:]:
        if f_score[xy] < lowest_f_score:
            lowest_xy = xy
            lowest_f_score = f_score[xy]
    return lowest_xy


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        next = came_from[current]
        path.append(next)
        current = next
    return path[::-1]


def get_lowest_path(losses, start_xy, end_xy):
    """
    Use an A* algorithm to find the shortest path from start_xy to end_xy.
    """
    # Create a list of all the points we need to check
    open_list = [start_xy]
    # Create a list of all the points we have checked
    closed_list = []
    # Create a dict of all the points we have checked, and the point we came from
    came_from = {}
    # Create a dict of all the points we have checked, and the cost to get there
    g_score = {}
    # Create a dict of all the points we have checked, and the estimated cost to get to the end
    f_score = {}

    # Set the start point
    g_score[start_xy] = 0
    f_score[start_xy] = get_distance(*start_xy, *end_xy)

    # Loop until we have checked all the points
    while open_list:
        # Get the point with the lowest f_score
        current = get_lowest_f_score(open_list, f_score)
        # If we have reached the end, return the path
        if current == end_xy:
            return reconstruct_path(came_from, current)
        # Remove the current point from the open list
        open_list.remove(current)
        # Add the current point to the closed list
        closed_list.append(current)
        # Get the neighbours of the current point
        neighbours = get_neighbours(*current, losses)
        # Loop through the neighbours
        for neighbour in neighbours:
            if is_straight_line(neighbour, current, came_from):
                continue
            # If the neighbour is in the closed list, skip it
            if neighbour in closed_list:
                continue
            # If the neighbour is not in the open list, add it
            if neighbour not in open_list:
                open_list.append(neighbour)
            # Get the cost to get to the neighbour
            tentative_g_score = g_score[current] + losses[neighbour]
            # If the cost to get to the neighbour is higher than the cost to get to the current point, skip it
            if tentative_g_score >= g_score.get(neighbour, float("inf")):
                continue
            # Set the cost to get to the neighbour
            g_score[neighbour] = tentative_g_score
            # Set the estimated cost to get to the end
            f_score[neighbour] = tentative_g_score + get_distance(*neighbour, *end_xy)
            # Set the point we came from
            came_from[neighbour] = current

    # If we have checked all the points and not found the end


def get_path_heat_loss(path, losses):
    total = 0
    for xy in path:
        total += losses[xy]
    return total


HEIGHT = len(data.splitlines())
WIDTH = len(data.splitlines()[0])

losses = get_losses(data)
path = get_lowest_path(losses, (0, 0), (WIDTH - 1, HEIGHT - 1))
heat_loss = get_path_heat_loss(path, losses)
print(heat_loss)

for y in range(HEIGHT):
    for x in range(WIDTH):
        if (x, y) in path:
            print(".", end="")
        else:
            print(losses[(x, y)], end="")
    print()
