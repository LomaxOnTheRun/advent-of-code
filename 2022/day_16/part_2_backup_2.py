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


def get_score(minute: int, valve: str) -> int:
    return (TOTAL_MINUTES - minute) * VALUES[valve]


def do_next_actions(minute: int, actions: list[str, int], open_valves: set, score: int):
    elapsed_time = min([time_left for _, time_left in actions])
    new_minute = minute + elapsed_time

    new_actions = set()
    current_locations = []
    new_open_valves = set()
    for valve, time_left in actions:
        if time_left == elapsed_time:
            new_open_valves.add(valve)
            current_locations.append(valve)
            score += get_score(new_minute, valve)
        else:
            new_actions.add((valve, time_left - elapsed_time))

    new_open_valves |= open_valves

    return (new_minute, new_actions, open_valves, current_locations, score)


def will_time_out(minute: int, actions: list) -> bool:
    if not actions:
        return False
    min_time_left = min([time_left for _, time_left in actions])
    return minute + min_time_left >= TOTAL_MINUTES


def get_next_possible_actions_for_valve(
    current_actions: list, current_valve: str, open_valves: set
) -> list:
    next_actions = []
    current_action_valves = set([valve for valve, _ in current_actions])

    possible_next_valves = ALL_VALVES - (
        open_valves | current_action_valves | {current_valve}
    )
    for next_valve in possible_next_valves:
        distance = DISTANCES[current_valve][next_valve]
        next_actions.append((next_valve, distance))
    return next_actions


def get_next_possible_actions(
    current_actions: list, open_valves: set, current_locations: list
):
    valves_left = ALL_VALVES - (open_valves | set([v for v, _ in current_actions]))

    if not valves_left:
        return [current_actions]

    current_locations = sorted(current_locations)

    first_valve_actions = get_next_possible_actions_for_valve(
        current_actions, current_locations[0], open_valves
    )

    if len(current_locations) == 1 or len(valves_left) == 1:
        possible_actions = []
        for action in first_valve_actions:
            possible_actions.append((*current_actions, action))
        return possible_actions

    assert not current_actions

    next_actions = []
    for first_valve_action in first_valve_actions:
        second_valve_actions = get_next_possible_actions_for_valve(
            [first_valve_action], current_locations[1], open_valves
        )
        for second_valve_action in second_valve_actions:
            next_actions.append((first_valve_action, second_valve_action))
    return next_actions


def take_actions(
    minute: int, actions: list, open_valves: set, score: int, max_score, num_paths
):
    # if will_time_out(minute, actions):
    #     print("TIME OUT")

    # if len(open_valves) == len(ALL_VALVES):
    #     print("ALL VALVES OPEN")

    # Check for time-outs or if we've opened all valves
    if will_time_out(minute, actions) or len(open_valves) == len(ALL_VALVES):
        if score > max_score[0]:
            max_score[0] = score
        num_paths[0] += 1
        return

    # TODO: FIGURE OUT AN EARLY STOP
    remaining_time = TOTAL_MINUTES - minute
    remaining_valves = ALL_VALVES - open_valves
    remaining_value = sum([VALUES[valve] for valve in remaining_valves])
    # print(remaining_time)
    # print(remaining_valves)
    # print(remaining_value)
    if score + (remaining_time * remaining_value) < max_score[0]:
        return

    # Do shortest action(s)
    minute, actions, open_valves, current_locations, score = do_next_actions(
        minute, actions, open_valves, score
    )

    # Get next possible actions
    next_possible_actions = get_next_possible_actions(
        actions, open_valves, current_locations
    )

    # Take another step down the rabbit hole
    for next_actions in next_possible_actions:
        take_actions(minute, next_actions, open_valves, score, max_score, num_paths)


TOTAL_MINUTES = 10
TOTAL_MINUTES = 26

import time

start_time = time.perf_counter()

max_score = [0]
num_paths = [0]
take_actions(0, [("AA", 0), ("AA", 0)], {"AA"}, 0, max_score, num_paths)

end_time = time.perf_counter()
print(f"Run time: {end_time - start_time:.2f}")

print("Total minutes:", TOTAL_MINUTES)
print("Num paths:", num_paths[0])
print("Max score:", max_score[0])

# print()
# print(VALUES)
# print()
# print(DISTANCES["AA"])

# for path in PATHS:
#     print()
#     print(path)
