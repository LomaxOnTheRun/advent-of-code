# Start time: 7:41am
# End time: 7:50am

import aocd

data = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

data = aocd.get_data(year=2021, day=13)

dots, folds = data.split(("\n\n"))
dots = {tuple(map(int, dot.split(","))) for dot in dots.split("\n")}

folds = [(fold[11], int(fold[13:])) for fold in folds.split("\n")]

for fold in folds:
    if fold[0] == "x":
        dots = {(x if x < fold[1] else fold[1] - (x - fold[1]), y) for x, y in dots}
    else:
        dots = {(x, y if y < fold[1] else fold[1] - (y - fold[1])) for x, y in dots}

max_x, max_y = max([dot[0] for dot in dots]), max([dot[1] for dot in dots])
for y in range(max_y + 1):
    row = ""
    for x in range(max_x + 1):
        row += "#" if (x, y) in dots else " "
    print(row)
