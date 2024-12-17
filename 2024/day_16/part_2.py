# Start time: 09:56
# End time: 10:30

import aocd, heapq


data = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

# data = """#################
# #...#...#...#..E#
# #.#.#.#.#.#.#.#.#
# #.#.#.#...#...#.#
# #.#.#.#.###.#.#.#
# #...#.#.#.....#.#
# #.#.#.#.#.#####.#
# #.#...#.#.#.....#
# #.#.#####.#.###.#
# #.#.#.......#...#
# #.#.###.#####.###
# #.#.#...#.....#.#
# #.#.#.#####.###.#
# #.#.#.........#.#
# #.#.#.#########.#
# #S#.............#
# #################"""

data = aocd.get_data(year=2024, day=16)

N, E, S, W = 0, 1, 2, 3


class State:
    def __init__(
        self,
        x: int,
        y: int,
        facing: int,
        cost: int,
        prev_xys: set,
        prev_xy_facings: set,
    ) -> None:
        self.x = x
        self.y = y
        self.facing = facing
        self.cost = cost
        self.prev_xys = prev_xys
        self.prev_xy_facings = prev_xy_facings

    def __repr__(self):
        facing_str = {0: "N", 1: "E", 2: "S", 3: "W"}[self.facing]
        return f"State({self.x}, {self.y}, {facing_str}, {self.cost})"

    def __lt__(self, other):
        return self.cost < other.cost


COORDS = set()
start_xy, end_xy = (), ()
for y, row in enumerate(data.split()):
    for x, char in enumerate(row):
        if char == "S":
            start_xy = (x, y)
            COORDS.add((x, y))
        elif char == "E":
            end_xy = (x, y)
            COORDS.add((x, y))
        elif char == ".":
            COORDS.add((x, y))

DIRS = {N: (0, -1), E: (1, 0), S: (0, 1), W: (-1, 0)}
seen_xy_facings: dict[tuple, list[State]] = {}  # {(x, y, facing): [State]}
next_states = []  # {cost: (next_xy, facing)}


def left_turn(facing: int) -> int:
    return {N: W, E: N, S: E, W: S}[facing]


def right_turn(facing: int) -> int:
    return {N: E, E: S, S: W, W: N}[facing]


def get_next_states(state: State) -> list[State]:
    next_states = []
    x, y, facing, cost = state.x, state.y, state.facing, state.cost
    new_prev_xys = state.prev_xys | {(x, y)}
    new_prev_xy_facings = state.prev_xy_facings | {(x, y, facing)}

    # Step forward
    dx, dy = DIRS[state.facing]
    new_x, new_y = (x + dx, y + dy)
    if (new_x, new_y) in COORDS:
        next_states.append(
            State(
                new_x, new_y, state.facing, cost + 1, new_prev_xys, new_prev_xy_facings
            )
        )

    # Left turn
    left_facing = left_turn(state.facing)
    dx, dy = DIRS[left_facing]
    new_xy = (x + dx, y + dy)
    if new_xy in COORDS and new_xy not in state.prev_xys:
        next_states.append(
            State(x, y, left_facing, cost + 1000, new_prev_xys, new_prev_xy_facings)
        )

    # Right turn
    right_facing = right_turn(state.facing)
    dx, dy = DIRS[right_facing]
    new_xy = (x + dx, y + dy)
    if new_xy in COORDS and new_xy not in state.prev_xys:
        next_states.append(
            State(x, y, right_facing, cost + 1000, new_prev_xys, new_prev_xy_facings)
        )

    return next_states


def update_seen_states(state, prev_xys_to_add):
    for seen_state in seen_states:
        if (state.x, state.y) in seen_state.prev_xys:
            seen_state.prev_xys |= prev_xys_to_add


start = State(start_xy[0], start_xy[1], 1, 0, set(), set())
heapq.heappush(next_states, (0, start))
best_prev_xys = set()
best_cost = 0
while next_states:
    cost, state = heapq.heappop(next_states)

    xy_facing = (state.x, state.y, state.facing)
    if xy_facing in seen_xy_facings:
        seen_states = seen_xy_facings[xy_facing]
        seen_cost = seen_states[0].cost
        if cost > seen_cost:
            continue
        elif cost == seen_cost:
            seen_xy_facings[xy_facing].append(state)
        elif cost < seen_cost:
            seen_xy_facings[xy_facing] = [state]
    else:
        seen_xy_facings[xy_facing] = [state]

    if (state.x, state.y) == end_xy:
        if 0 < best_cost < cost:
            break
        best_prev_xys |= state.prev_xys
        best_cost = cost

    for next_state in get_next_states(state):
        heapq.heappush(next_states, (next_state.cost, next_state))


print(len(best_prev_xys) + 1)  # +end
