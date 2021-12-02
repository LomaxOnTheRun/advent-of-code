import aocd

data = aocd.get_data(year=2021, day=2).split("\n")

# Part 1
get_values = lambda dir, line: int(line.split(" ")[1]) * (line[0] == dir)
distances = [get_values("f", line) for line in data]
depths = [get_values("d", line) - get_values("u", line) for line in data]
print(sum(distances) * sum(depths))

# Part 2
aims = [sum(depths[:i]) for i in range(len(depths))]
new_depths = [dist * aim for dist, aim in zip(distances, aims)]
print(sum(distances) * sum(new_depths))
