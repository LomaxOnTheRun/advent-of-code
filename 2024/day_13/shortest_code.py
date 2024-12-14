import aocd, re


for part in (0, 1):
    total = 0
    for lines in aocd.get_data(year=2024, day=13).split("\n\n"):
        # Get machine values
        match = re.match(re.compile(".*?([0-9]+)" * 6, re.DOTALL), lines)
        ax, ay, bx, by, px, py = [int(val) for val in match.groups()]
        px, py = px + int(part * 1e13), py + int(part * 1e13)

        # Get only possible solutions
        top, bottom = (px * by) - (py * bx), (ax * by) - (ay * bx)
        if (num_a := top // bottom) == top / bottom:
            total += (3 * num_a) + ((px - (num_a * ax)) // bx)

    print(total)
