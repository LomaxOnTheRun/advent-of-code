import aocd

data = aocd.get_data(year=2021, day=2).split("\n")
data = [(line.split(" ")[0], int(line.split(" ")[1])) for line in data]

distance = 0
depth = 0

for direction, value in data:
    if direction == "forward":
        distance += value
    if direction == "up":
        depth -= value
    if direction == "down":
        depth += value

print(distance * depth)
