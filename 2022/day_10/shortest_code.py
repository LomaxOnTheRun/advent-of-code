# 7 lines

import aocd

# Create a list of every cycle value
vals = [1]
for line in aocd.get_data(year=2022, day=10).split("\n"):
    vals.extend([vals[-1], vals[-1] + int(line[5:])] if line[0] == "a" else [vals[-1]])

# Part 1: Sum certain cycle strengths
print(sum([i * vals[i - 1] for i in (20, 60, 100, 140, 180, 220)]))

# Part 2: Draw out the sprite overlaps
for y in range(6):
    print("".join(["#" if abs(vals[(y * 40) + x] - x) < 2 else "." for x in range(40)]))
