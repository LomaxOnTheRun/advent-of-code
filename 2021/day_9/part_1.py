# Start time: 7:12am
# End time: 7:44am

import aocd

data = """2199943210
3987894921
9856789892
8767896789
9899965678"""

data = aocd.get_data(year=2021, day=9)


data = data.split("\n")


def create_lowest_grid(data):
    height = len(data)
    width = len(data[0])
    lowest = [[True] * width for _ in data]
    for y in range(height):
        for x in range(width):
            if x > 0 and data[y][x] >= data[y][x - 1]:
                lowest[y][x] = False
            if x < width - 1 and data[y][x] >= data[y][x + 1]:
                lowest[y][x] = False
            if y > 0 and data[y][x] >= data[y - 1][x]:
                lowest[y][x] = False
            if y < height - 1 and data[y][x] >= data[y + 1][x]:
                lowest[y][x] = False
    return lowest


lowest = create_lowest_grid(data)

sum = 0
for y in range(len(data)):
    for x in range(len(data[0])):
        if lowest[y][x]:
            sum += int(data[y][x]) + 1

print(sum)
