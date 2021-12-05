import aocd

# data = """0,9 -> 5,9
# 8,0 -> 0,8
# 9,4 -> 3,4
# 2,2 -> 2,1
# 7,0 -> 7,4
# 6,4 -> 2,0
# 0,9 -> 2,9
# 3,4 -> 1,4
# 0,0 -> 8,8
# 5,5 -> 8,2"""
# data = data.split("\n")

data = aocd.get_data(year=2021, day=5).split("\n")

# Turn into nested list of ints
lines = [line.split(" -> ") for line in data]
lines = [[xy1.split(","), xy2.split(",")] for xy1, xy2 in lines]
# lines = [[int(x), int(y)] for x, y in [xy for xy in [line for line in lines]]]
for line in lines:
    for xy in line:
        xy[0] = int(xy[0])
        xy[1] = int(xy[1])


def is_straight(line):
    return line[0][0] == line[1][0] or line[0][1] == line[1][1]


def is_diagonal(line):
    return abs(line[0][0] - line[1][0]) == abs(line[0][1] - line[1][1])


# Remove non-straight lines
lines = [line for line in lines if (is_straight(line) or is_diagonal(line))]

# Expand lines to cover every point in them
all_coords = {}
for line in lines:
    min_x, max_x = min(line[0][0], line[1][0]), max(line[0][0], line[1][0])
    min_y, max_y = min(line[0][1], line[1][1]), max(line[0][1], line[1][1])
    if is_straight(line):
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                all_coords[(x, y)] = all_coords.get((x, y), 0) + 1
    elif line[0] == [min_x, min_y] or line[0] == [max_x, max_y]:
        length = max_x - min_x
        for i in range(length + 1):
            x, y = min_x + i, min_y + i
            all_coords[(x, y)] = all_coords.get((x, y), 0) + 1
    else:
        length = max_x - min_x
        for i in range(length + 1):
            x, y = min_x + i, max_y - i
            all_coords[(x, y)] = all_coords.get((x, y), 0) + 1

print(len([val for val in all_coords.values() if val > 1]))

# Visualisation to help with debugging
# for y in range(10):
#     row = ""
#     for x in range(10):
#         row += str(all_coords.get((x, y), "."))
#     print(row)
