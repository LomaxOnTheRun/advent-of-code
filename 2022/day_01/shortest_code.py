# 4 lines

import aocd

data = [elf.split() for elf in aocd.get_data(year=2022, day=1).split("\n\n")]

# Part 1
print(max([sum([int(cal) for cal in elf]) for elf in data]))
# Part 2
print(sum(sorted([sum([int(cal) for cal in elf]) for elf in data])[-3:]))
