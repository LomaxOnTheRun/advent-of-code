# Start time: 8:12am
# End time: 8:36am

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


def valid_add(path, node):
    if node == "start":
        return False
    if node == "end":
        return True
    if node == node.upper():
        return True
    if node not in path:
        return True
    return not any([path.count(node) > 1 for node in path if node == node.lower()])


def add_node(path):
    if path[-1] == "end":
        return [path]

    new_paths = []
    for next in conns[path[-1]]:
        if valid_add(path, next):
            new_paths.append(path + [next])

    return new_paths


paths, new_paths = [], [["start"]]
while new_paths != paths:
    paths = new_paths
    new_paths = [add_node(path) for path in paths]
    new_paths = [path for paths in new_paths for path in paths]

print(len(paths))
