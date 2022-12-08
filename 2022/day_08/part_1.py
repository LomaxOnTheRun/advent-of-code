# Start time: 06:38
# End time: 06:57

import aocd

data = """30373
25512
65332
33549
35390"""

data = aocd.get_data(year=2022, day=8)

trees = [[int(num) for num in line] for line in data.split()]
visible = [[False for tree in line] for line in trees]
height, width = range(len(trees)), range(len(trees[0]))

# Left
for y in height:
    tallest = -1
    for x in width:
        tree = trees[y][x]
        if tree > tallest:
            tallest = tree
            visible[y][x] = True

# Top
for x in width:
    tallest = -1
    for y in height:
        tree = trees[y][x]
        if tree > tallest:
            tallest = tree
            visible[y][x] = True

# Right
for y in height:
    tallest = -1
    for x in width[::-1]:
        tree = trees[y][x]
        if tree > tallest:
            tallest = tree
            visible[y][x] = True

# Bottom
for x in width:
    tallest = -1
    for y in height[::-1]:
        tree = trees[y][x]
        if tree > tallest:
            tallest = tree
            visible[y][x] = True

print(sum([sum(line) for line in visible]))
