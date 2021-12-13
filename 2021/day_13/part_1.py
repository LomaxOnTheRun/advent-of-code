# Start time: 7:22am
# End time: 7:41am

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

ff = folds[0]  # First fold

if ff[0] == "x":
    dots = {(x if x < ff[1] else ff[1] - (x - ff[1]), y) for x, y in dots}
else:
    dots = {(x, y if y < ff[1] else ff[1] - (y - ff[1])) for x, y in dots}
