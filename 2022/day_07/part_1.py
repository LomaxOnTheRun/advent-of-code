# Start time: 06:34
# End time: 07:36

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
files_seen = set()
dirs_seen = set()
for line in data.split("\n"):
    if line == "$ ls":
        continue
    if line[:4] == "dir ":
        continue

    if line == "$ cd /":
        path = ["/"]
    elif line == "$ cd ..":
        path = path[:-1]
    elif line[:5] == "$ cd ":
        full_path = "/".join(path) + "/" + line[5:]
        if full_path in dirs_seen:
            print(f"DIR ALREADY SEEN: {full_path}")
            continue
        dirs_seen.add(full_path)
        path.append(line[5:])

    elif line.split(" ")[0].isdigit():
        full_path = "/".join(path) + "/" + line
        if full_path in files_seen:
            print(f"FILE ALREADY SEEN: {full_path}")
            continue
        files_seen.add(full_path)
        size = int(line.split(" ")[0])
        for i in range(1, len(path) + 1):
            dir_full_path = "/".join(path[:i])
            if dir_full_path not in sizes:
                sizes[dir_full_path] = 0
            sizes[dir_full_path] += size

    else:
        print(line)

total_size = 0
for dir, size in sizes.items():
    if size <= 100000:
        total_size += size

print(total_size)

# 1079290 is too low
# 1121328 is too low
