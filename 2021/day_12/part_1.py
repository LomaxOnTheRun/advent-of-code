# Start time: 7:40am(ish)
# End time: 8:12am

import aocd

data = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

data = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

data = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""

data = aocd.get_data(year=2021, day=12)

data = [conn.split("-") for conn in data.split("\n")]

conns = {}
for cave_1, cave_2 in data:
    conns[cave_1] = conns.get(cave_1, []) + [cave_2]
    conns[cave_2] = conns.get(cave_2, []) + [cave_1]


def add_node(path):
    if path[-1] == "end":
        return [path]

    new_paths = []
    for next in conns[path[-1]]:
        if next == next.upper() or next not in path:
            new_paths.append(path + [next])

    return new_paths


paths = [["start"]]
for _ in range(99999):
    paths += add_node(paths.pop(0))

print(len(paths))
