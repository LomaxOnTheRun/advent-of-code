# Start time: 10:59
# End time:

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

# for conn in connections:
#     if "OPEN" not in conn:
#         print(conn, connections[conn])

# Multi-step walks that can be done faster
shortcuts_4 = []
for conn, next_conns in connections.items():
    if "OPEN" in conn:
        continue
    for next_conn in next_conns:
        if "OPEN" in next_conn:
            continue
        for n2_conn in connections[next_conn]:
            if "OPEN" in n2_conn:
                continue
            if n2_conn == conn:
                continue
            if n2_conn in next_conns:
                shortcuts_4.append([conn, next_conn, n2_conn])
            for n3_conn in connections[n2_conn]:
                if "OPEN" in n3_conn:
                    continue
                if n3_conn in (conn, next_conn):
                    continue
                if n3_conn in next_conns:
                    shortcuts_4.append([conn, next_conn, n2_conn, n3_conn])


# print(shortcuts_4)

shortcuts_5 = []
for conn, next_conns in connections.items():
    if "OPEN" in conn:
        continue
    for next_conn in next_conns:
        if "OPEN" in next_conn:
            continue
        for n2_conn in connections[next_conn]:
            if "OPEN" in n2_conn:
                continue
            if n2_conn == conn:
                continue
            for n3_conn in connections[n2_conn]:
                if "OPEN" in n3_conn:
                    continue
                if n3_conn in (conn, next_conn):
                    continue
                for n4_conn in connections[n3_conn]:
                    if "OPEN" in n4_conn:
                        continue
                    if n4_conn in (conn, next_conn, n2_conn):
                        continue
                    if n4_conn in next_conns:
                        shortcuts_5.append([conn, next_conn, n2_conn, n3_conn, n4_conn])


# print(shortcuts_5)

shortcuts_6 = []
for conn, next_conns in connections.items():
    if "OPEN" in conn:
        continue
    for next_conn in next_conns:
        if "OPEN" in next_conn:
            continue
        for n2_conn in connections[next_conn]:
            if "OPEN" in n2_conn:
                continue
            if n2_conn == conn:
                continue
            for n3_conn in connections[n2_conn]:
                if "OPEN" in n3_conn:
                    continue
                if n3_conn in (conn, next_conn):
                    continue
                for n4_conn in connections[n3_conn]:
                    if "OPEN" in n4_conn:
                        continue
                    if n4_conn in (conn, next_conn, n2_conn):
                        continue
                    for n5_conn in connections[n4_conn]:
                        if "OPEN" in n5_conn:
                            continue
                        if n5_conn in (conn, next_conn, n2_conn, n3_conn):
                            continue
                        if n5_conn in next_conns:
                            shortcuts_6.append(
                                [conn, next_conn, n2_conn, n3_conn, n4_conn, n5_conn]
                            )


# print(shortcuts_6)

completed_paths = set()
seen_paths = set()
tally = {}  # {place: {open valves: {{path_length: score}}}
max_score = [-1]


MAX_PATH_LENGTH = 10
# MAX_PATH_LENGTH = 27


def useless_double_back(paths, length):
    if len(paths) > length:
        if paths[-1][0] in paths[-length - 1] or paths[-1][1] in paths[-length - 1]:
            for move_1, move_2 in paths[-length:-1]:
                if "OPEN" in move_1 or "OPEN" in move_2:
                    return False
            return True
    return False


def keep_going(
    paths: list[tuple[str, str]],
    path_1: list,
    path_2: list,
    score: int,
    max_score: list,
    open_valves: list,
) -> str:
    # print(paths)
    if tuple(paths) in seen_paths:
        # print("-- 1")
        return

    # Someone is trying to open an already opened valve
    if paths[-1][0] in open_valves or paths[-1][1] in open_valves:
        # print("-- 2")
        return

    if useless_double_back(paths, 2):
        return

    if useless_double_back(paths, 3):
        return

    if useless_double_back(paths, 4):
        return

    if "OPEN" in paths[-1][0] and paths[-1][0] == paths[-1][1]:
        # print("-- 4")
        return

    # if path_1[-4:] in shortcuts_4 or path_2[-4:] in shortcuts_4:
    #     return

    # if path_1[-5:] in shortcuts_5 or path_2[-5:] in shortcuts_5:
    #     return

    if len(paths) > 5:
        if path_1[-6:] in shortcuts_6 or path_2[-6:] in shortcuts_6:
            return

    if len(paths) == MAX_PATH_LENGTH:
        # print(score)
        completed_paths.add(tuple(paths))
        max_score[0] = max(max_score[0], score)
        return max_score

    if "OPEN" in paths[-1][0]:
        open_valves = open_valves + [paths[-1][0]]
    if "OPEN" in paths[-1][1]:
        open_valves = open_valves + [paths[-1][1]]

    score += sum([flow_rates[move[:2]] for move in open_valves])
    # print(open_valves, score)
    # print(paths)

    # print()

    for conn_1 in connections[path_1[-1]]:
        for conn_2 in connections[path_2[-1]]:

            # print(conn_1, conn_2)
            # new_open_valves = []
            # if "OPEN" in conn_1:
            #     if conn_1 in open_valves:
            #         continue
            #     new_open_valves.append(conn_1)
            # if "OPEN" in conn_2:
            #     if conn_2 in open_valves:
            #         continue
            #     new_open_valves.append(conn_2)

            ordered_conns = tuple(sorted([conn_1, conn_2]))

            keep_going(
                paths + [ordered_conns],
                path_1 + [conn_1],
                path_2 + [conn_2],
                score,
                max_score,
                open_valves,
            )


import time

start_time = time.perf_counter()

keep_going([("AA", "AA")], ["AA"], ["AA"], 0, max_score, [])

end_time = time.perf_counter()
print(f"Total run time: {end_time - start_time:.2f}s")

print(f"Max path length: {MAX_PATH_LENGTH}")
print(f"Number of completed paths: {len(completed_paths)}")
print(max_score[0])

# for path in completed_paths:
#     print(path)

# 2179 is too low
# 1508 is too low
