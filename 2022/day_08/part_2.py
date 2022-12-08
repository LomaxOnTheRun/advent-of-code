# Start time: 06:57
# End time: 08:05

import aocd

data = """30373
25512
65332
33549
35390"""

data = aocd.get_data(year=2022, day=8)


def score_up(trees, x, y):
    new_y = y - 1
    dist = 0
    while new_y >= 0:
        dist += 1
        if trees[new_y][x] >= trees[y][x]:
            return dist
        new_y -= 1
    return dist


def score_left(trees, x, y):
    new_x = x - 1
    dist = 0
    while new_x >= 0:
        dist += 1
        if trees[y][new_x] >= trees[y][x]:
            return dist
        new_x -= 1
    return dist


def score_down(trees, x, y):
    new_y = y + 1
    dist = 0
    while new_y < len(trees):
        dist += 1
        if trees[new_y][x] >= trees[y][x]:
            return dist
        new_y += 1
    return dist


def score_right(trees, x, y):
    new_x = x + 1
    dist = 0
    while new_x < len(trees[0]):
        dist += 1
        if trees[y][new_x] >= trees[y][x]:
            return dist
        new_x += 1
    return dist


trees = [[int(num) for num in line] for line in data.split()]
scores = [[0 for _ in line] for line in trees]
height, width = range(len(trees)), range(len(trees[0]))

for y in height:
    for x in width:
        up = score_up(trees, x, y)
        left = score_left(trees, x, y)
        down = score_down(trees, x, y)
        right = score_right(trees, x, y)
        score = up * left * down * right

        scores[y][x] = score

print(max([max(line) for line in scores]))
