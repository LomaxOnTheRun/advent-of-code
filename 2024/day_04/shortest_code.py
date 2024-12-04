import aocd

# Build coords list for each letter
coords = {"X": [], "M": [], "A": [], "S": []}
width = len(aocd.get_data(year=2024, day=4).split("\n")[0])
for i, letter in enumerate(aocd.get_data(year=2024, day=4).replace("\n", "")):
    coords.get(letter, []).append((i % width, i // width))

total_1, total_2 = 0, 0
for x, y in coords["A"]:
    # Part 1
    # Find all potential letter positions for XMAS based on A coords
    for dx, dy in [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]:
        for xmas in [[(x + (i * dx), y + (i * dy)) for i in (-2, -1, 0, 1)]]:
            # Check which potential positions match actual letters
            total_1 += all(xmas[i] in coords["XMAS"[i]] for i in (0, 1, 2, 3))

    # Part 2
    # Find all potential letter positions for X-MAS based on A coords
    dxy = [(-1, -1), (-1, 1), (1, 1), (1, -1)] * 2
    for mmss in [[(x + dx, y + dy) for dx, dy in dxy[i : i + 4]] for i in range(4)]:
        # Check which potential positions match actual letters
        total_2 += all(mmss[i] in coords["MMSS"[i]] for i in (0, 1, 2, 3))

print(f"{total_1}\n{total_2}")
