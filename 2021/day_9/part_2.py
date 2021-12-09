# Start time: 7:44am
# End time: 8:26am

import aocd

data = """2199943210
3987894921
9856789892
8767896789
9899965678"""

data = aocd.get_data(year=2021, day=9)


data = data.split("\n")
height = len(data)
width = len(data[0])


def create_lowest_grid(data, height, width):
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


lowest = create_lowest_grid(data, height, width)


basins = []
for x in range(width):
    for y in range(height):
        if lowest[y][x]:
            basins.append([(y, x)])


def add_new_neighbours(basin, point, data, height, width):
    y, x = point
    new_points = []
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_y = y + dy
        new_x = x + dx
        new_point = (new_y, new_x)
        if new_point in basin:
            continue
        if 0 <= new_y <= height - 1 and 0 <= new_x <= width - 1:
            if int(data[new_y][new_x]) < 9:
                new_points.append(new_point)
    return new_points


for basin in basins:
    for point in basin:
        new_points = add_new_neighbours(basin, point, data, height, width)
        basin += new_points


def prod(numbers):
    product = 1
    for number in numbers:
        product *= number
    return product


print(prod(sorted([len(basin) for basin in basins])[-3:]))
