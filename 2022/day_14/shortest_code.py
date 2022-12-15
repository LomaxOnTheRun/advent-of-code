# 20 lines

import aocd

# Build set of each coord that is a wall
walls = set()
for line in aocd.get_data(year=2022, day=14).split("\n"):
    # Build list of list of corners
    for i in range(len(corners := [eval(f"({c})") for c in line.split(" -> ")]) - 1):
        # Get ends of each wall
        (x0, y0), (x1, y1) = sorted(corners[i : i + 2])
        # Add coord for each step between corners
        for x, y in [(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]:
            walls.add((x, y))

# Find lowest depth of any wall part (not floor)
max_depth = max([depth for _, depth in walls])


def settle_sand(stop_condition):
    # Keep track of all taken spaces (t)
    t = set() | walls
    # Check passed stopping condition (difference between part 1 and 2)
    while not stop_condition(t - walls, max_depth):
        # Start new unit of sand falling
        (x, y) = (500, 0)
        while True:
            # Stop if we hit the floor (i.e. fall into abyss for part 1) ...
            # ... or if there is no free space to move into
            if y == max_depth + 1 or all((x + dx, y + 1) in t for dx in [0, -1, 1]):
                t.add((x, y))
                break
            # Otherwise move into the next available space
            x, y = [(x + dx, y + 1) for dx in [0, -1, 1] if (x + dx, y + 1) not in t][0]

    # Only return settled sand (i.e. without the walls)
    return t - walls


# Part 1 - Stop when sand falls below walls
# (the -1 at the end is because we "catch" the first bit of sand that falls into the abyss)
print(len(settle_sand(lambda ss, md: max([depth for _, depth in ss] + [0]) >= md)) - 1)

# Part 2 - Stop when start point is covered
print(len(settle_sand(lambda ss, _: (500, 0) in ss)))
