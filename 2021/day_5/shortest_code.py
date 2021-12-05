import aocd


### A walk through the deep dark forest of recursion ###

# def split(data: str, ops: t.List):
#     return [split(part, ops[1:]) if ops[1:] else part for part in data.split(ops[0])]

# def make_int(data: t.List):
#     return [int(part) if type(part) == str else make_int(part) for part in data]

# data = aocd.get_data(year=2021, day=5)
# sp = lambda data, ops: [sp(d, ops[1:]) if ops[1:] else d for d in data.split(ops[0])]
# make_int = lambda data: [int(d) if type(d) == str else make_int(d) for d in data]
# lines = make_int(sp(data, ["\n", " -> ", ","]))

### End of walk ###


data = aocd.get_data(year=2021, day=5).split("\n")

# Turn into nested list of ints
lines = [line.split(" -> ") for line in data]
lines = [[xy1.split(","), xy2.split(",")] for xy1, xy2 in lines]
lines = [[[int(xy[0]), int(xy[1])] for xy in line] for line in lines]

### Alternative line splitting ###
# split_list = lambda str_list, splitter: [val.split(splitter) for val in str_list]
# lines = [split_list(xy, ",") for xy in split_list(data.split("\n"), " -> ")]
# lines = [[[int(xy[0]), int(xy[1])] for xy in line] for line in lines]
### End of alternative ###

# Keep count of how many lines go over each square
part_1_coords, part_2_coords = {}, {}
for xy1, xy2 in lines:
    min_x, max_x, min_y, max_y = sorted([xy1[0], xy2[0]]) + sorted([xy1[1], xy2[1]])
    for i in range(max(max_x - min_x, max_y - min_y) + 1):
        x = min(min_x + i, max_x)
        y = min(min_y + i if min(xy1, xy2)[1] == min_y else max_y - i, max_y)
        # Part 1
        if xy1[0] == xy2[0] or xy1[1] == xy2[1]:
            part_1_coords[(x, y)] = part_1_coords.get((x, y), 0) + 1
        # Part 2
        part_2_coords[(x, y)] = part_2_coords.get((x, y), 0) + 1

# Part 1 solution
print(len([val for val in part_1_coords.values() if val > 1]))

# Part 2 solution
print(len([val for val in part_2_coords.values() if val > 1]))
