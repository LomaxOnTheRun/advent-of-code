# Start time: 10:44
# End time: 11:10

import aocd

data = """..X...
.SAMX.
.A..A.
XMAS.S
.X...."""

data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

data = aocd.get_data(year=2024, day=4)

letters = data.splitlines()
# print(letters)

coords = {"X": [], "M": [], "A": [], "S": []}
for y, row in enumerate(letters):
    for x, letter in enumerate(row):
        if letter != ".":
            coords[letter].append((x, y))

# print()
# print(coords)

xmas_coords = []
for x, y in coords["X"]:
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            xmas_coords += [[(x + (i * dx), y + (i * dy)) for i in (0, 1, 2, 3)]]

# print()
# print(xmas_coords)

total = 0
for xmas in xmas_coords:
    total += all(xmas[i] in coords["XMAS"[i]] for i in (0, 1, 2, 3))

# print()
print(total)
