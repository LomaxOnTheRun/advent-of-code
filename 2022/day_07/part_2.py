# Start time: 06:34
# End time: 07:45

import aocd

data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

data = aocd.get_data(year=2022, day=7)

sizes = {"/": 0}
path = []
for line in data.split("\n"):
    if line == "$ cd /":
        path = ["/"]
    elif line == "$ cd ..":
        path = path[:-1]
    elif line[:5] == "$ cd ":
        path.append(line[5:])

    elif line.split(" ")[0].isdigit():
        size = int(line.split(" ")[0])
        for i in range(1, len(path) + 1):
            dir_full_path = "/".join(path[:i])
            if dir_full_path not in sizes:
                sizes[dir_full_path] = 0
            sizes[dir_full_path] += size

cut_required = sizes["/"] - 40000000
smallest_cut = 1e10
for dir in sizes:
    if sizes[dir] > cut_required and sizes[dir] < smallest_cut:
        smallest_cut = sizes[dir]

print(smallest_cut)
