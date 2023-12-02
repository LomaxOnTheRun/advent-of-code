# Start time: 10:59
# End time:

import aocd

from perf_utils import timeit, print_logged_times


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

# data = aocd.get_data(year=2022, day=16)


### INITIAL SETUP ###


def get_shortest_route(start_valve, end_valve):
    visited_valves = set()
    previous_node = {}
    valves_to_visit = [start_valve]
    while end_valve not in valves_to_visit:
        valve = valves_to_visit.pop(0)
        for next_valve in ALL_CONNECTIONS[valve]:
            if next_valve in visited_valves:
                continue
            valves_to_visit.append(next_valve)
            previous_node[next_valve] = valve
        visited_valves.add(valve)

    chain = [end_valve]
    while chain[-1] != start_valve:
        chain.append(previous_node[chain[-1]])

    # We don't subtract 1 because we also need to spend one turn opening the valve
    return len(chain)


ALL_CONNECTIONS = {}
DISTANCES = {"AA": {}}
VALUES = {"AA": 0}
ALL_VALVES = {"AA"}
for line in data.split("\n"):
    parts = line.split()
    name = parts[1]
    valve_value = int(parts[4][5:-1])
    ALL_CONNECTIONS[name] = {valve.strip(",") for valve in parts[9:]}
    if valve_value > 0:
        DISTANCES[name] = {}
        VALUES[name] = valve_value
        ALL_VALVES.add(name)

# Calculate the shortest distance from each useful node to other useful nodes
for start_valve in DISTANCES:
    for end_valve in DISTANCES.keys() - {start_valve, "AA"}:
        DISTANCES[start_valve][end_valve] = get_shortest_route(start_valve, end_valve)


###


CurrentNodes = tuple[str, ...]
MoveInProgress = tuple[str, int]  # Destination, steps left
MovesInProgress = tuple[MoveInProgress, ...]
State = tuple[int, int, MovesInProgress, CurrentNodes]


@timeit
def get_state(
    minute: int,
    score: int,
    current_nodes: CurrentNodes,
    moves_in_progress: MovesInProgress,
    remaining_valves: set[str],
    path: list[tuple[int, str]],
) -> State:
    return (
        minute,
        score,
        tuple(current_nodes),
        tuple(moves_in_progress),
        remaining_valves,
        path,
    )


@timeit
def get_score(minute: int, valve: str) -> int:
    return (TOTAL_MINUTES - minute) * VALUES[valve]


@timeit
def get_next_moves_in_progress_1(current_nodes, moves_in_progress, remaining_valves):
    print("get_next_moves_in_progress_1")
    assert len(current_nodes) == 1
    assert len(moves_in_progress) == 1

    next_moves = []
    distances = DISTANCES[current_nodes[0]]
    for next_valve in remaining_valves:
        new_move = (next_valve, distances[next_valve])
        next_moves.append((moves_in_progress[0], new_move))

    return next_moves


@timeit
def get_next_moves_in_progress_2(current_nodes, moves_in_progress, remaining_valves):
    """
    When both actors are looking for their next moves.
    """
    print("get_next_moves_in_progress_2")
    assert len(current_nodes) == 2
    assert len(moves_in_progress) == 0
    assert len(remaining_valves) >= 2

    moves_dist = {}

    for next_valve_1 in remaining_valves:
        dist_1 = DISTANCES[current_nodes[0]][next_valve_1]
        new_move_1 = (next_valve_1, dist_1)
        for next_valve_2 in remaining_valves:
            dist_2 = DISTANCES[current_nodes[0]][next_valve_2]
            new_move_2 = (next_valve_2, dist_2)

            if next_valve_1 == next_valve_2:
                continue

            moves = sorted(next_valve_1, next_valve_2)
            moves_dist[moves] = min(dist_1 + dist_2, moves_dist.get(moves, 1e10))

    # next_moves = []
    # for next_valve_1 in remaining_valves:
    #     # Move from current node 1 to next node 1
    #     dist_11 = DISTANCES[current_nodes[0]][next_valve_1]
    #     new_move_11 = (next_valve_1, dist_11)
    #     # Move from current node 2 to next node 1
    #     dist_21 = DISTANCES[current_nodes[1]][next_valve_1]
    #     new_move_21 = (next_valve_1, dist_21)

    #     for next_valve_2 in remaining_valves:
    #         # Move from current node 1 to next node 1
    #         dist_12 = DISTANCES[current_nodes[0]][next_valve_2]
    #         new_move_12 = (next_valve_2, dist_12)
    #         # Move from current node 2 to next node 1
    #         dist_22 = DISTANCES[current_nodes[1]][next_valve_2]
    #         new_move_22 = (next_valve_2, dist_22)

    #         if next_valve_1 == next_valve_2:
    #             continue

    #         if dist_11 + dist_22 < dist_12 + dist_21:
    #             next_moves.append((new_move_11, new_move_22))
    #         else:
    #             next_moves.append((new_move_12, new_move_21))

    return next_moves


@timeit
def get_next_moves_in_progress_3(current_nodes, moves_in_progress, remaining_valves):
    print("get_next_moves_in_progress_3")
    assert len(current_nodes) == 2
    assert len(moves_in_progress) == 0
    assert len(remaining_valves) == 1

    next_moves = []
    for next_valve in remaining_valves:
        distance_1 = DISTANCES[current_nodes[0]][next_valve]
        distance_2 = DISTANCES[current_nodes[1]][next_valve]
        next_moves.append(((next_valve, min(distance_1, distance_2)),))

    return next_moves


@timeit
def get_next_moves_in_progress(state: State):
    """
    Set up the next move, but don't actually move yet.
    """
    _, _, current_nodes, moves_in_progress, remaining_valves, _ = state

    # print(state)

    if len(moves_in_progress) == 1 and not remaining_valves:
        return [moves_in_progress]

    if len(current_nodes) == 1 and len(moves_in_progress) == 1:
        return get_next_moves_in_progress_1(
            current_nodes, moves_in_progress, remaining_valves
        )

    if len(remaining_valves) > 1:
        return get_next_moves_in_progress_2(
            current_nodes, moves_in_progress, remaining_valves
        )

    return get_next_moves_in_progress_3(
        current_nodes, moves_in_progress, remaining_valves
    )


@timeit
def get_next_state(
    minute: int,
    score: int,
    next_moves_in_progress: MovesInProgress,
    remaining_valves: set[str],
    path: list[tuple[int, str]],
) -> State:
    """
    Carry out the next shortest moves.
    """
    elapsed_time = min([time_left for _, time_left in next_moves_in_progress])
    new_minute = minute + elapsed_time

    new_moves_in_progress = []
    new_current_nodes = []
    new_score = score
    new_remaining_valves = set() | remaining_valves
    new_path = [step for step in path]

    for valve, time_left in next_moves_in_progress:
        if time_left == elapsed_time:
            new_current_nodes.append(valve)
            new_score += get_score(new_minute, valve)
        else:
            new_moves_in_progress.append((valve, time_left - elapsed_time))

        path_step = (minute + time_left, valve)
        if path_step not in new_path:
            new_path.append(path_step)

        new_remaining_valves -= {valve}

    new_state = get_state(
        new_minute,
        new_score,
        new_current_nodes,
        new_moves_in_progress,
        new_remaining_valves,
        new_path,
    )

    return new_state


@timeit
def will_time_out(minute: int, moves_in_progress: MovesInProgress) -> bool:
    if not moves_in_progress:
        return False
    min_time_left = min([time_left for _, time_left in moves_in_progress])
    return minute + min_time_left >= TOTAL_MINUTES


@timeit
def check_end_conditions(minute, score, max_score, next_state):
    _, next_score, _, moves_in_progress, remaining_valves, _ = next_state

    if will_time_out(minute, moves_in_progress):
        if score >= max_score:
            max_score = score
        return True, max_score

    if not remaining_valves and not moves_in_progress:
        if next_score >= max_score:
            max_score = next_score
        return True, max_score

    return False, max_score


TOTAL_MINUTES = 1
# TOTAL_MINUTES = 26

# print()
# for key in DISTANCES:
#     print(key, DISTANCES[key])
# print()

import time

start_time = time.perf_counter()

max_score = 0

# minute, score, current_nodes, moves_in_progress, remaining_valves, path
initial_state = get_state(0, 0, ("AA", "AA"), (), ALL_VALVES - {"AA"}, [])

states_to_check = [initial_state]
while states_to_check:
    state = states_to_check.pop(0)
    minute, score, _, moves_in_progress, remaining_valves, path = state

    print(state)

    all_next_moves_in_progress = get_next_moves_in_progress(state)

    for move in all_next_moves_in_progress:
        print(move)
    exit()

    for next_moves_in_progress in all_next_moves_in_progress:

        next_state = get_next_state(
            minute, score, next_moves_in_progress, remaining_valves, path
        )

        # End conditions
        end_found, max_score = check_end_conditions(
            minute, score, max_score, next_state
        )
        if end_found:
            continue

        if next_moves_in_progress != moves_in_progress:
            states_to_check.append(next_state)


# print()
# for key in DISTANCES:
#     print(key, DISTANCES[key])
# print()

print(max_score)

print_logged_times()

end_time = time.perf_counter()
print(f"\nTotal run time: {end_time - start_time:.2f}")
