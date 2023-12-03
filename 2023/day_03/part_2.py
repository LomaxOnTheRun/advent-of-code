# Start time: 09:31
# End time: 09:41

import aocd

data = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

data = aocd.get_data(year=2023, day=3)

all_num_locs, gear_locs = {}, {}

for y, line in enumerate(data.splitlines()):
    num, num_locs = "", ()
    for x, char in enumerate(line):
        if char in "1234567890":
            num += char
            num_locs += ((x, y),)
        elif num:
            all_num_locs[num_locs] = num
            num, num_locs = "", ()
        if char == "*":
            gear_locs[(x, y)] = [
                (x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)
            ]
    if num:
        all_num_locs[num_locs] = num
        num, num_locs = "", ()

total = 0
for gear_loc, gear_locs in gear_locs.items():
    adjacent_nums = []
    for num_locs, num in all_num_locs.items():
        if any(num_loc in gear_locs for num_loc in num_locs):
            adjacent_nums.append(int(num))
    if len(adjacent_nums) == 2:
        total += adjacent_nums[0] * adjacent_nums[1]

print(total)
