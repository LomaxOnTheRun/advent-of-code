import aocd

# data = """...>...
# .......
# ......>
# v.....>
# ......>
# .......
# ..vvv.."""

data = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""

data = aocd.get_data(year=2021, day=25)

RIGHT = ">"
DOWN = "v"


def create_grid_sets(data):
    # {(x, y), ...}
    right_slugs = set()
    down_slugs = set()
    for y, row in enumerate(data.split("\n")):
        for x, slug in enumerate(row):
            if slug == RIGHT:
                right_slugs.add((x, y))
            if slug == DOWN:
                down_slugs.add((x, y))
    return right_slugs, down_slugs, x, y


def step(right_slugs, down_slugs):
    new_right_slugs = set()
    new_down_slugs = set()

    for x, y in right_slugs:
        new_pos = ((x + 1) % (max_x + 1), y)
        if new_pos in right_slugs or new_pos in down_slugs:
            new_pos = (x, y)
        new_right_slugs.add(new_pos)

    for x, y in down_slugs:
        new_pos = (x, (y + 1) % (max_y + 1))
        # NOTE: We check against new_right_slugs here, not right_slugs
        if new_pos in new_right_slugs or new_pos in down_slugs:
            new_pos = (x, y)
        new_down_slugs.add(new_pos)

    return new_right_slugs, new_down_slugs


def print_grid(right_slugs, down_slugs, max_x, max_y, step):
    print(f"\nStep {step}:\n")
    for y in range(max_y + 1):
        row = ""
        for x in range(max_x + 1):
            if (x, y) in right_slugs:
                row += RIGHT
            elif (x, y) in down_slugs:
                row += DOWN
            else:
                row += "."
        print(row)


right_slugs, down_slugs, max_x, max_y = create_grid_sets(data)
# print_grid(right_slugs, down_slugs, max_x, max_y, 0)

steps_taken = 0
while True:
    new_right_slugs, new_down_slugs = step(right_slugs, down_slugs)
    steps_taken += 1

    if new_right_slugs == right_slugs and new_down_slugs == down_slugs:
        print(steps_taken)
        break

    right_slugs, down_slugs = new_right_slugs, new_down_slugs
