import aocd

data = [conn.split("-") for conn in aocd.get_data(year=2021, day=12).split("\n")]

# Create a dict of a cave to all viable next caves
conns = {}
for cave_1, cave_2 in data:
    conns[cave_1] = conns.get(cave_1, []) + ([cave_2] * (cave_2 != "start"))
    conns[cave_2] = conns.get(cave_2, []) + ([cave_1] * (cave_1 != "start"))

# Shortcut for getting all the lower caves in a path
lower = lambda path: [cave for cave in path if cave == cave.lower()]

# The criteria for valid caves for each part of the problem
valid_1 = lambda path, cave: cave == cave.upper() or cave not in path
valid_2 = lambda path, c: valid_1(path, c) or len(set(lower(path))) == len(lower(path))

# Given a possibly partial path (and a validation function):
# - Return a list with only that path if it's complete
# - Return a list of paths which validly extend the inital one by a step
add = lambda p, v: [p] if p[-1] == "end" else [p + [c] for c in conns[p[-1]] if v(p, c)]


# Get all the paths for a given validation criteria
def get_paths(valid, paths=[], new_paths=[["start"]]):
    while new_paths != paths:
        paths = new_paths
        # For each current path, get all extended possibilities, then flatter them all
        new_paths = [p for paths in [add(path, valid) for path in paths] for p in paths]
    return paths


# Print the answers to both parts
print(f"{len(get_paths(valid_1))}\n{len(get_paths(valid_2))}")
