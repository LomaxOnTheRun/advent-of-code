# Start time: 08:12
# End time: 08:20

import aocd

data = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

data = aocd.get_data(year=2024, day=2)

total = 0
for report in data.splitlines():
    levels = report.split()
    diffs = []
    for i in range(len(levels) - 1):
        diffs.append(int(levels[i + 1]) - int(levels[i]))

    if all(d > 0 for d in diffs) or all(d < 0 for d in diffs):
        if all(0 < abs(d) < 4 for d in diffs):
            total += 1

print(total)
