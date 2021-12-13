import aocd

# Split up instructions
dots, folds = aocd.get_data(year=2021, day=13).split(("\n\n"))
# Create a set of dot positions
dots = {tuple(map(int, dot.split(","))) for dot in dots.split("\n")}

# Get the new x or y value after flipping over fold line
flip = lambda xy, fold: xy if xy < int(fold[13:]) else 2 * int(fold[13:]) - xy

# Do all of the folds
for fold in folds.split("\n"):
    dots = {(flip(x, fold), y) if "x" in fold else (x, flip(y, fold)) for x, y in dots}
    # Part 1
    print(len(dots)) if fold == folds.split("\n")[0] else None

# Part 2
for y in range(max([y for _, y in dots]) + 1):
    print("".join([[" ", "#"][(x, y) in dots] for x in range(sorted(dots)[-1][0])]))
