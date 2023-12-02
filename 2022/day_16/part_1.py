# Start time: 06:05
# End time: 10:59

import aocd

data = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

data = aocd.get_data(year=2022, day=16)

flow_rates = {}
connections = {}

for line in data.split("\n"):
    line_parts = line.split(" ")
    valve = line_parts[1]
    flow_rates[valve] = int(line_parts[4][5:-1])
    connections[valve] = [conn.strip(",") for conn in line_parts[9:]]
    if flow_rates[valve] > 0:
        connections[f"{valve} OPEN"] = [conn for conn in connections[valve]]
        connections[valve].insert(0, f"{valve} OPEN")

# print(connections)

completed_paths = set()
tally = {}  # {(length, place, open valves): score}
max_score = [-1]


def keep_going(path: list, score: int, max_score: list) -> str:
    if "OPEN" in path[-1] and path[-1] in path[:-1]:
        return

    open_valves = tuple(sorted([move for move in path if "OPEN" in move]))
    # score += sum([flow_rates[move[:2]] for move in open_valves])
    tally_key = (len(path), path[-1], open_valves)
    # tally_key = (len(path), path[-1])
    if score > tally.get(tally_key, -1):
        tally[tally_key] = score
    else:
        return

    if len(path) > 2 and path[-3] == path[-1]:
        return

    for i in range(3, 5):
        if (
            len(path) > i
            and path[-1] == path[-i - 1]
            and not any(["OPEN" in move for move in path[-i:-1]])
        ):
            return

    if len(path) == 31:
        completed_paths.add(tuple(path))
        max_score[0] = max(max_score[0], score)
        return max_score

    score += sum([flow_rates[move[:2]] for move in open_valves])
    for conn in connections[path[-1]]:
        keep_going(path + [conn], score, max_score)


keep_going(["AA"], 0, max_score)

print(len(completed_paths))
print(max_score[0])

# print(len(completed_paths))
# # for path in completed_paths:
# #     print(len(path))

scores = []
for path in completed_paths:
    score = 0
    total_flow = 0
    for move in path[1:]:
        score += total_flow
        if "OPEN" in move:
            total_flow += flow_rates[move[:2]]
    scores.append(score)

print(max(scores))


# 1406 is too low
# 1493 is too low
