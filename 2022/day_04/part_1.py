# Start time: 06:34
# End time: 06:47

import aocd

data = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

data = aocd.get_data(year=2022, day=4)

overlaps = 0
for line in data.split():
    elf_1, elf_2 = line.split(",")
    elf_1 = [int(num) for num in elf_1.split("-")]
    elf_1 = set(range(elf_1[0], elf_1[1] + 1))
    elf_2 = [int(num) for num in elf_2.split("-")]
    elf_2 = set(range(elf_2[0], elf_2[1] + 1))
    if elf_1 <= elf_2 or elf_1 >= elf_2:
        overlaps += 1

print(overlaps)
