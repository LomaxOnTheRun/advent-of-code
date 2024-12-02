# Start time: 08:20
# End time: 08:42

import aocd

data = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

data = aocd.get_data(year=2024, day=2)


def is_report_safe(levels: list[int]) -> bool:
    diffs = []
    for i in range(len(levels) - 1):
        diffs.append(levels[i + 1] - levels[i])

    if all(d > 0 for d in diffs) or all(d < 0 for d in diffs):
        if all(0 < abs(d) < 4 for d in diffs):
            return True

    return False


total = 0
for report in data.splitlines():
    levels = [int(level) for level in report.split()]
    if is_report_safe(levels):
        total += 1
        continue

    for i in range(len(levels)):
        report_is_safe = False
        reduced = [levels[j] for j in range(len(levels)) if j != i]
        if is_report_safe(reduced):
            total += 1
            report_is_safe = True
            break

        if report_is_safe:
            continue

print(total)
