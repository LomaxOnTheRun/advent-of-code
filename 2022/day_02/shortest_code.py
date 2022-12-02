# 4 lines

"""
Part 2 workings out

A Y = rock      draw    =>  89 - 65 = 24    => rock         65 - 24 = 41    => %3 = 1
B X = paper     lose    =>  88 - 66 = 22    => rock         66 - 22 = 44    => %3 = 1
C Z = scissors  win     =>  90 - 67 = 23    => rock         67 - 23 = 44    => %3 = 1
A Z = rock      win     =>  90 - 65 = 25    => paper        65 - 25 = 40    => %3 = 2
B Y = paper     draw    =>  89 - 66 = 23    => paper        66 - 23 = 43    => %3 = 2
C X = scissors  lose    =>  88 - 67 = 21    => paper        67 - 21 = 46    => %3 = 2
A X = rock      lose    =>  88 - 65 = 23    => scissors     65 - 23 = 42    => %3 = 0
B Z = paper     win     =>  90 - 66 = 24    => scissors     66 - 24 = 42    => %3 = 0
C Y = scissors  draw    =>  89 - 67 = 22    => scissors     67 - 22 = 45    => %3 = 0
"""

import aocd

data = [[ord(l[0]), ord(l[2])] for l in aocd.get_data(year=2022, day=2).split("\n")]

# Part 1
print(sum([me - 87 + ((me - elf + 2) % 3) * 3 for elf, me in data]))

# Part 2
print(sum([((end - 88) * 3) + ((end - (2 * elf) + 2) % 3) + 1 for elf, end in data]))
