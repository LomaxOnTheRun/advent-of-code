# Start time: 06:12
# End time: 07:52

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

data = aocd.get_data(year=2023, day=13)

fields = data.split("\n\n")

total = 0
for field in fields:
    rows = field.splitlines()
    cols = list(zip(*rows))

    for i in range(1, len(rows)):
        if rows[i - 1] == rows[i]:
            mirror_found = True
            di = 0
            while i - di - 1 >= 0 and i + di < len(rows):
                if rows[i - di - 1] != rows[i + di]:
                    mirror_found = False
                    break
                di += 1
            if mirror_found:
                total += 100 * i
                break

    for i in range(1, len(cols)):
        if cols[i - 1] == cols[i]:
            mirror_found = True
            di = 0
            while i - di - 1 >= 0 and i + di < len(cols):
                if cols[i - di - 1] != cols[i + di]:
                    mirror_found = False
                    break
                di += 1
            if mirror_found:
                total += i
                break

print(total)
