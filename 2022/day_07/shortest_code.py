# 12 lines

import aocd

sizes, path = {}, []
for line in aocd.get_data(year=2022, day=7).split("\n"):
    # Go up one level
    if line == "$ cd ..":
        path = path[:-1]
    # Go down one level
    elif line[:5] == "$ cd ":
        path.append(line[5:])
    # Add size to all dirs in path
    elif (size := line.split(" ")[0]).isdigit():
        for i in range(len(path)):
            # Note: Duplicate dir names means we need to use full paths for each dir
            sizes[str(path[: i + 1])] = sizes.get(str(path[: i + 1]), 0) + int(size)

# Part 1
print(sum([size for size in sizes.values() if size < 100000]))

# Part 2
print(min([size for size in sizes.values() if size > sizes["['/']"] - 40000000]))
