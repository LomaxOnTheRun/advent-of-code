# Start time: 11:10
# End time: 11:22

import aocd

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
        if letter in coords:
            coords[letter].append((x, y))

# print()
# print(coords)

xmas_coords = []
for x, y in coords["A"]:
    dxy = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
    for i in range(4):
        ms = [dxy[i], dxy[(i + 1) % 4]]
        ss = [dxy[(i + 2) % 4], dxy[(i + 3) % 4]]
        xmas_coords += [[(x + dx, y + dy) for dx, dy in ms + ss]]

# print()
# print(xmas_coords)

total = 0
for m1, m2, s1, s2 in xmas_coords:
    ms, ss = coords["M"], coords["S"]
    total += m1 in ms and m2 in ms and s1 in ss and s2 in ss

# print()
print(total)
