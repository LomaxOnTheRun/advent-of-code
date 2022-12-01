# 06:35
# 06:38

import aocd

data = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

data = aocd.get_data(year=2022, day=1)

cals = []
cal = 0
for line in data.split("\n"):
    if line == "":
        cals.append(cal)
        cal = 0
        continue

    cal += int(line)
cals.append(cal)

print(max(cals))
