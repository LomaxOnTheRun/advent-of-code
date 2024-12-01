# Start time: 14:48
# End time:

import aocd

data = """3   4
4   3
2   5
1   3
3   9
3   3"""

data = aocd.get_data(year=2024, day=1)

left, right = [], []
for line in data.splitlines():
    l, r = line.split("  ")
    left.append(int(l))
    right.append(int(r))

left.sort()
right.sort()

total = 0
for i, l in enumerate(left):
    c = right.count(l)
    total += l * c

print(total)
