# 4 lines

import aocd

data = aocd.get_data(year=2022, day=6)

# Part 1
print([len(set(data[i - 4 : i])) for i in range(len(data))].index(4))

# Part 2
print([len(set(data[i - 14 : i])) for i in range(len(data))].index(14))
