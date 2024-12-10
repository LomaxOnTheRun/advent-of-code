import aocd


def get_ends(x0, y0, val, ends):
    # Check in each adjacent space
    for x, y in [(x0, y0 + 1), (x0, y0 - 1), (x0 + 1, y0), (x0 - 1, y0)]:
        # Check next coord is in grid
        # Check next coord is one step higher
        # (xy := (x, y)) is always true, and sets xy = (x, y) for the next line
        if (xy := (x, y)) and 0 <= x <= max_x and 0 <= y <= max_y and z[xy] == val + 1:
            # If we hit the end of a path, add (x, y) to the ends list we're building
            # Else run get_ends(x, y, val + 1, ends)
            # [] * bool(...) always equals [], so adding it to ends does nothing
            ends += [xy] if z[xy] == 9 else [] * bool(get_ends(x, y, val + 1, ends))
    # Return a list of all end coords, one per path to get there
    return ends


# Build a map of (x, y) coords to z-heights
# max_x and max_y will be left as the maximum x and y coords for get_ends to use
z = {}
for max_y, row in enumerate(aocd.get_data(year=2024, day=10).split()):
    for max_x, val in enumerate(row):
        z[(max_x, max_y)] = int(val)

# For all starts, get all end coords it can reach (one end coord per path to it)
ends = [get_ends(x, y, 0, []) for x, y in [xy for xy in z if z[xy] == 0]]
# Part 1 reduces lists to sets as it only cares about end points
# Part 2 keeps the lists as each end represents one path to get there
print(f"{sum(len(set(end)) for end in ends)}\n{sum(len(end) for end in ends)}")
