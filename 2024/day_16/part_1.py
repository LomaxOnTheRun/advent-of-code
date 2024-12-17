# Start time: 07:49
# End time: 09:56

import aocd, heapq

# data = """###############
# #.......#....E#
# #.#.###.#.###.#
# #.....#.#...#.#
# #.###.#####.#.#
# #.#.#.......#.#
# #.#.#####.###.#
# #...........#.#
# ###.#.#####.#.#
# #...#.....#.#.#
# #.#.#.###.#.#.#
# #.....#...#.#.#
# #.###.#.#.#.#.#
# #S..#.....#...#
# ###############"""

# data = """#######
# #SE#
# #######"""

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
    def __init__(self, x: int, y: int, facing: int, cost: int, prev_xys: set) -> None:
        self.x = x
        self.y = y
        self.facing = facing
        self.cost = cost
        self.prev_xys = prev_xys

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
seen_xy_facings = set()  # {(x, y, facing)}
next_states = []  # {cost: (next_xy, facing)}


def left_turn(facing: int) -> int:
    return {N: W, E: N, S: E, W: S}[facing]


def right_turn(facing: int) -> int:
    return {N: E, E: S, S: W, W: N}[facing]


def get_next_states(state: State) -> list[State]:
    next_states = []
    x, y = state.x, state.y
    new_prev_xys = state.prev_xys | {(x, y)}

    # Step forward
    dx, dy = DIRS[state.facing]
    new_x, new_y = (x + dx, y + dy)
    if (new_x, new_y) in COORDS:
        next_states.append(
            State(new_x, new_y, state.facing, state.cost + 1, new_prev_xys)
        )

    # Left turn
    left_facing = left_turn(state.facing)
    dx, dy = DIRS[left_facing]
    new_xy = (x + dx, y + dy)
    if new_xy in COORDS and new_xy not in state.prev_xys:
        next_states.append(State(x, y, left_facing, state.cost + 1000, new_prev_xys))

    # Right turn
    right_facing = right_turn(state.facing)
    dx, dy = DIRS[right_facing]
    new_xy = (x + dx, y + dy)
    if new_xy in COORDS and new_xy not in state.prev_xys:
        next_states.append(State(x, y, right_facing, state.cost + 1000, new_prev_xys))

    return next_states


start = State(start_xy[0], start_xy[1], 1, 0, set())
heapq.heappush(next_states, (0, start))
while next_states:
    cost, state = heapq.heappop(next_states)

    xy_facing = (state.x, state.y, state.facing)
    if xy_facing in seen_xy_facings:
        continue
    seen_xy_facings.add(xy_facing)

    if (state.x, state.y) == end_xy:
        print(cost)
        break

    for next_state in get_next_states(state):
        heapq.heappush(next_states, (next_state.cost, next_state))
