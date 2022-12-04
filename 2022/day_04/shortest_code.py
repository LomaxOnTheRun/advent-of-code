# 5 lines

import aocd, re

# Split all data into one list of numbers
data = [int(n) for n in re.sub("[,-]", " ", aocd.get_data(year=2022, day=4)).split()]

# Create sets representing all areas
areas = [set(range(area[0], area[1] + 1)) for area in zip(data[::2], data[1::2])]

# Part 1: Check for subsets
print(sum([(e1 <= e2 or e1 >= e2) for e1, e2 in zip(areas[::2], areas[1::2])]))

# Part 2: Check for overlaps
print(sum([bool(elf_1 & elf_2) for elf_1, elf_2 in zip(areas[::2], areas[1::2])]))
