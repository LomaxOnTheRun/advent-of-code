import aocd

data = list(map(int, aocd.get_data(year=2021, day=1).split("\n")))

# Part 1
print(len([i for i in range(len(data) - 1) if data[i + 1] > data[i]]))

# Part 2
print(len([i for i in range(len(data) - 3) if data[i + 3] > data[i]]))
