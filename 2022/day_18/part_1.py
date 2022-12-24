# Start time: 08:11
# End time: 08:19

import aocd

data = """1,1,1
2,1,1"""

data = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

data = aocd.get_data(year=2022, day=18)

drops = [eval(f"({line})") for line in data.split()]

dirs = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]

total_sides = 0
for drop in drops:
    for dir in dirs:
        if (drop[0] + dir[0], drop[1] + dir[1], drop[2] + dir[2]) not in drops:
            total_sides += 1

print(total_sides)
