# Start time: 07:52
# End time: 08:32

import aocd

data = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

data = """#...##..##..#
...##..####..
.#.##........
###.#.##..##.
...##.#.##.#.
.....#..##..#
...#.#..##..#
...##.#.##.#.
###.#.##..##."""

data = """###.#.#
##...##
#..##.#
##.#.##
..##...
..#.##.
#####..
#####..
..#.##."""

data = aocd.get_data(year=2023, day=13)


def get_num_diffs(line_1: tuple[str], line_2: tuple[str]) -> int:
    """
    Return the number of differences between lines.
    """
    num_diffs = 0
    for i in range(len(line_1)):
        if line_1[i] != line_2[i]:
            num_diffs += 1
        # Shortcut to save time
        # We never care if there are more than two diffs
        if num_diffs == 2:
            break
    return num_diffs


def mirror_is_found(lines: list) -> tuple[bool, int]:
    for i in range(1, len(lines)):
        smudges = 0
        num_diffs = get_num_diffs(lines[i - 1], lines[i])
        if num_diffs > 1:
            continue

        # Possible match found

        # Check all other lines
        mirror_found = True
        di = 0
        while i - di >= 1 and i + di < len(lines):
            num_diffs = get_num_diffs(lines[i - di - 1], lines[i + di])
            if num_diffs > 1:
                # Failure - too many smudges required
                mirror_found = False
                break

            if num_diffs == 1:
                smudges += 1

            if smudges > 1:
                # Failure - too many smudges required
                mirror_found = False
                break

            di += 1

        # Success
        if mirror_found and smudges == 1:
            return True, i

    # Failure
    return False, -1


fields = data.split("\n\n")

total = 0
for field in fields:
    rows = [tuple(row) for row in field.splitlines()]
    cols = list(zip(*rows))

    mirror_found, row = mirror_is_found(rows)
    if mirror_found:
        total += 100 * row

    mirror_found, col = mirror_is_found(cols)
    if mirror_found:
        total += col

print(total)
