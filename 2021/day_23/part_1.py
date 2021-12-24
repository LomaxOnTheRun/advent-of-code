import aocd, itertools as it

data = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

data = aocd.get_data(year=2021, day=23)

data = data.split("\n")[2:]
data = [[am for am in list(line) if am in "ABCD"] for line in data]

# Final rooms
A, B, C, D = ["A", "B", "C", "D"]
# Hallway, LB and RB are back of L and R, LF and RF are front of L and R (near hall)
LB, LF, RB, RF, AB, BC, CD = ["LB", "LF", "RB", "RF", "AB", "BC", "CD"]

HALLWAY = [LB, LF, AB, BC, CD, RF, RB]
ROOM_SIZE = {A: 2, B: 2, C: 2, D: 2, LB: 1, LF: 1, RB: 1, RF: 1, AB: 1, BC: 1, CD: 1}

STEP_MULTIPLIER = {A: 1, B: 10, C: 100, D: 1000}

# Lists go from back to hallway
init_hallway = {LF: (), LB: (), RF: (), RB: (), AB: (), BC: (), CD: ()}
init_rooms = {A: (), B: (), C: (), D: (), **init_hallway}
for line in [line for line in data if line]:
    for i, room_name in enumerate("ABCD"):
        init_rooms[room_name] = (line[i], *init_rooms.get(room_name, ()))


def steps_from_entry(name, rooms):
    return ROOM_SIZE[name] - len(rooms[name])


def steps_to(from_, to_, rooms):
    if from_ == A:
        hallway_dict = {LB: 3, LF: 2, AB: 2, BC: 4, CD: 6, RF: 8, RB: 9}
        dist_dict = {A: 0, B: 4, C: 6, D: 8, **hallway_dict}
    elif from_ == B:
        hallway_dict = {LB: 5, LF: 4, AB: 2, BC: 2, CD: 4, RF: 6, RB: 7}
        dist_dict = {A: 4, B: 0, C: 4, D: 6, **hallway_dict}
    elif from_ == C:
        hallway_dict = {LB: 7, LF: 6, AB: 4, BC: 2, CD: 2, RF: 4, RB: 5}
        dist_dict = {A: 6, B: 4, C: 0, D: 4, **hallway_dict}
    elif from_ == D:
        hallway_dict = {LB: 9, LF: 8, AB: 6, BC: 4, CD: 2, RF: 2, RB: 3}
        dist_dict = {A: 8, B: 6, C: 4, D: 0, **hallway_dict}
    elif from_ == LF:
        hallway_dict = {LB: 1, LF: 0, AB: 2, BC: 4, CD: 6, RF: 8, RB: 9}
        dist_dict = {A: 2, B: 4, C: 6, D: 8, **hallway_dict}
    elif from_ == LB:
        hallway_dict = {LB: 0, LF: 1, AB: 3, BC: 5, CD: 7, RF: 9, RB: 10}
        dist_dict = {A: 3, B: 5, C: 7, D: 9, **hallway_dict}
    elif from_ == RF:
        hallway_dict = {LB: 9, LF: 8, AB: 6, BC: 4, CD: 2, RF: 0, RB: 1}
        dist_dict = {A: 8, B: 6, C: 4, D: 2, **hallway_dict}
    elif from_ == RB:
        hallway_dict = {LB: 10, LF: 9, AB: 7, BC: 5, CD: 3, RF: 1, RB: 0}
        dist_dict = {A: 9, B: 7, C: 5, D: 3, **hallway_dict}
    elif from_ == AB:
        hallway_dict = {LB: 3, LF: 2, AB: 0, BC: 2, CD: 4, RF: 6, RB: 7}
        dist_dict = {A: 2, B: 2, C: 4, D: 6, **hallway_dict}
    elif from_ == BC:
        hallway_dict = {LB: 5, LF: 4, AB: 2, BC: 0, CD: 2, RF: 4, RB: 5}
        dist_dict = {A: 4, B: 2, C: 2, D: 4, **hallway_dict}
    elif from_ == CD:
        hallway_dict = {LB: 7, LF: 6, AB: 4, BC: 2, CD: 0, RF: 2, RB: 3}
        dist_dict = {A: 6, B: 4, C: 2, D: 2, **hallway_dict}

    return (
        steps_from_entry(from_, rooms)
        + dist_dict[to_]
        + steps_from_entry(to_, rooms)
        - 1
    )


def has_clear_path(room_from, room_to, rooms, debug=False):
    # Left to right
    if room_from in [LB] and room_to in [A, AB, B, BC, C, CD, D, RF, RB] and rooms[LF]:
        if debug:
            print(f"Obstacle at LB: {rooms[LB]}")
        return False
    if room_from in [LB, LF, A] and room_to in [B, BC, C, CD, D, RF, RB] and rooms[AB]:
        if debug:
            print(f"Obstacle at AB: {rooms[AB]}")
        return False
    if room_from in [LB, LF, A, AB, B] and room_to in [C, CD, D, RF, RB] and rooms[BC]:
        if debug:
            print(f"Obstacle at BC: {rooms[BC]}")
        return False
    if room_from in [LB, LF, A, AB, B, BC, C] and room_to in [D, RF, RB] and rooms[CD]:
        if debug:
            print(f"Obstacle at CD: {rooms[CD]}")
        return False
    # Right to left
    if room_from in [A, AB, B, BC, C, CD, D, RF, RB] and room_to in [LB] and rooms[LF]:
        if debug:
            print(f"Obstacle at LF: {rooms[LF]}")
        return False
    if room_from in [B, BC, C, CD, D, RF, RB] and room_to in [LB, LF, A] and rooms[AB]:
        if debug:
            print(f"Obstacle at AB: {rooms[AB]}")
        return False
    if room_from in [C, CD, D, RF, RB] and room_to in [LB, LF, A, AB, B] and rooms[BC]:
        if debug:
            print(f"Obstacle at BC: {rooms[BC]}")
        return False
    if room_from in [D, RF, RB] and room_to in [LB, LF, A, AB, B, BC, C] and rooms[CD]:
        if debug:
            print(f"Obstacle at CD: {rooms[CD]}")
        return False
    return True


def move(room_from, room_to, rooms, debug=False) -> int:
    """Try to move the outer-most amphipod to another room."""

    # Moving to same room
    if from_room == to_room:
        if debug:
            print(f"Move {room_from} > {room_to} not allowed: Same room")
        return None, 0

    # Current room is empty
    if not rooms[from_room]:
        if debug:
            print(f"Move {room_from} > {room_to} not allowed: Current room is empty")
        return None, 0

    # Can't move from hallway to hallway
    if room_from in HALLWAY and room_to in HALLWAY:
        if debug:
            print(
                f"Move {room_from} > {room_to} not allowed: Moving from hallway to hallway"
            )
        return None, 0

    # New room is full
    if len(rooms[room_to]) == ROOM_SIZE[room_to]:
        if debug:
            print(f"Move {room_from} > {room_to} not allowed: Next room is full")
        return None, 0

    # Only move into a room if it's only populated by the correct type (or empty)
    for am in rooms[to_room]:
        if to_room not in HALLWAY and am != to_room:
            if debug:
                print(
                    f"Move {room_from} > {room_to} not allowed: Next room has incorrect type in it"
                )
            return None, 0

    # Path to new location must be clear
    if not has_clear_path(from_room, to_room, rooms):
        if debug:
            print(f"Move {room_from} > {room_to} not allowed: Obstacle in path")
        return None, 0

    if from_room not in HALLWAY and all([am == from_room for am in rooms[from_room]]):
        if debug:
            print(
                f"Move {room_from} > {room_to} not allowed: Amphipod already in correct room"
            )
        return None, 0

    # Calculate steps required
    steps = steps_to(room_from, room_to, rooms)

    # Copy rooms so the old one doesn't get overwritten
    new_rooms = {k: tuple(a for a in v) for k, v in rooms.items()}

    # Move out of room
    amphipod = new_rooms[room_from][-1]
    new_rooms[room_from] = new_rooms[room_from][:-1]

    # Amphipod can only go into own room
    if room_to not in HALLWAY and amphipod != room_to:
        if debug:
            print(
                f"Move {room_from} > {room_to} not allowed: Next room not correct for amphipod"
            )
        return None, 0

    # Move into new room
    new_rooms[room_to] = (*new_rooms[room_to], amphipod)

    # Calculate step energy
    steps *= STEP_MULTIPLIER[amphipod]

    return new_rooms, steps


def all_moves():
    """Get all combinations of from and to rooms."""
    return it.product(ROOM_SIZE.keys(), repeat=2)


def is_finished(rooms):
    filled = {A: (A, A), B: (B, B), C: (C, C), D: (D, D)}
    empty = {LF: (), LB: (), RF: (), RB: (), AB: (), BC: (), CD: ()}
    return rooms == {**filled, **empty}


def hash_rooms(rooms):
    return (
        f"A:{rooms[A]}_B:{rooms[B]}_C:{rooms[C]}_D:{rooms[D]}_"
        + f"LF:{rooms[LF]}_LB:{rooms[LB]}_RF:{rooms[RF]}_RB:{rooms[RB]}_"
        + f"AB:{rooms[AB]}_BC:{rooms[BC]}_CD:{rooms[CD]}"
    )


def print_state(old_rooms, new_rooms):
    def spot_str(rooms, name, index):
        return rooms[name][index] if len(rooms[name]) > index else "."

    def left_right_str(rooms):
        left_str = spot_str(rooms, LB, 0) + spot_str(rooms, LF, 0)
        right_str = spot_str(rooms, RF, 0) + spot_str(rooms, RB, 0)
        return left_str, right_str

    old, new = old_rooms, new_rooms
    # Line 0
    print("#############    #############")
    # Line 1
    old_LEFT, old_RIGHT = left_right_str(old)
    new_LEFT, new_RIGHT = left_right_str(new)
    old_AB, new_AB = spot_str(old, AB, 0), spot_str(new, AB, 0)
    old_BC, new_BC = spot_str(old, BC, 0), spot_str(new, BC, 0)
    old_CD, new_CD = spot_str(old, CD, 0), spot_str(new, CD, 0)
    old_line_1 = f"#{old_LEFT}.{old_AB}.{old_BC}.{old_CD}.{old_RIGHT}#"
    new_line_1 = f"#{new_LEFT}.{new_AB}.{new_BC}.{new_CD}.{new_RIGHT}#"
    print(f"{old_line_1}    {new_line_1}")
    # Line 2
    old_line_2 = f"###{spot_str(old, A, 1)}#{spot_str(old, B, 1)}#{spot_str(old, C, 1)}#{spot_str(old, D, 1)}###"
    new_line_2 = f"###{spot_str(new, A, 1)}#{spot_str(new, B, 1)}#{spot_str(new, C, 1)}#{spot_str(new, D, 1)}###"
    print(f"{old_line_2}    {new_line_2}")
    # Line 3
    old_line_3 = f"  #{spot_str(old, A, 0)}#{spot_str(old, B, 0)}#{spot_str(old, C, 0)}#{spot_str(old, D, 0)}#  "
    new_line_3 = f"  #{spot_str(new, A, 0)}#{spot_str(new, B, 0)}#{spot_str(new, C, 0)}#{spot_str(new, D, 0)}#  "
    print(f"{old_line_3}    {new_line_3}")
    # Line 4
    print("  #########        #########  ")


# Try all combinations
states_dict = {hash_rooms(init_rooms): init_rooms}
steps_dict = {hash_rooms(init_rooms): 0}
finished_steps = 1e10

# from datetime import datetime as dt

# start = dt.now()

while steps_dict:
    # Pop a state and related total step count
    rooms_hash = list(steps_dict)[0]
    steps = steps_dict[rooms_hash]
    del steps_dict[rooms_hash]
    rooms = states_dict[rooms_hash]

    # Speed up end states
    if steps > finished_steps:
        continue

    for from_room, to_room in all_moves():
        new_rooms, new_steps = move(from_room, to_room, rooms, debug=False)

        # New move not valid
        if not new_rooms:
            continue

        total_steps = steps + new_steps
        if is_finished(new_rooms):
            finished_steps = min(finished_steps, total_steps)
        else:
            new_rooms_hash = hash_rooms(new_rooms)
            states_dict[new_rooms_hash] = new_rooms

            if new_rooms_hash not in steps_dict:
                steps_dict[new_rooms_hash] = total_steps
            else:
                min_steps = min(total_steps, steps_dict[new_rooms_hash])
                steps_dict[new_rooms_hash] = min_steps

    # CHECKS FOLLOWING THE EXAMPLE SOLUTION

    # rms = {A: (A, B), B: (D, C), C: (C,), D: (A, D)}
    # hlwy = {LF: (), LB: (), RF: (), RB: (), AB: (B,), BC: (), CD: ()}
    # check_state_1 = {**rms, **hlwy}
    # if rooms == init_rooms:
    #     assert hash_rooms(check_state_1) in steps_dict
    #     assert steps_dict[hash_rooms(check_state_1)] == 40
    #     # print("Check 1 passed")

    # rms = {A: (A, B), B: (D,), C: (C, C), D: (A, D)}
    # hlwy = {LF: (), LB: (), RF: (), RB: (), AB: (B,), BC: (), CD: ()}
    # check_state_2 = {**rms, **hlwy}
    # if rooms == check_state_1:
    #     assert hash_rooms(check_state_2) in steps_dict
    #     assert steps_dict[hash_rooms(check_state_2)] == 440
    #     # print("Check 2 passed")

    # rms = {A: (A, B), B: (), C: (C, C), D: (A, D)}
    # hlwy = {LF: (), LB: (), RF: (), RB: (), AB: (B,), BC: (D,), CD: ()}
    # check_state_3 = {**rms, **hlwy}
    # if rooms == check_state_2:
    #     assert hash_rooms(check_state_3) in steps_dict
    #     assert steps_dict[hash_rooms(check_state_3)] == 3440
    #     # print("Check 3 passed")

    # rms = {A: (A, B), B: (B,), C: (C, C), D: (A, D)}
    # hlwy = {LF: (), LB: (), RF: (), RB: (), AB: (), BC: (D,), CD: ()}
    # check_state_4 = {**rms, **hlwy}
    # if rooms == check_state_3:
    #     assert hash_rooms(check_state_4) in steps_dict
    #     assert steps_dict[hash_rooms(check_state_4)] == 3470
    #     # print("Check 4 passed")

    # rms = {A: (A,), B: (B, B), C: (C, C), D: (A, D)}
    # hlwy = {LF: (), LB: (), RF: (), RB: (), AB: (), BC: (D,), CD: ()}
    # check_state_5 = {**rms, **hlwy}
    # if rooms == check_state_4:
    #     assert hash_rooms(check_state_5) in steps_dict
    #     assert steps_dict[hash_rooms(check_state_5)] == 3510
    #     # print("Check 5 passed")

    # rms = {A: (A,), B: (B, B), C: (C, C), D: (A,)}
    # hlwy = {LF: (), LB: (), RF: (), RB: (), AB: (), BC: (D,), CD: (D,)}
    # check_state_6 = {**rms, **hlwy}
    # if rooms == check_state_5:
    #     assert hash_rooms(check_state_6) in steps_dict
    #     assert steps_dict[hash_rooms(check_state_6)] == 5510
    #     # print("Check 6 passed")

    # rms = {A: (A,), B: (B, B), C: (C, C), D: ()}
    # hlwy = {LF: (), LB: (), RF: (A,), RB: (), AB: (), BC: (D,), CD: (D,)}
    # check_state_7 = {**rms, **hlwy}
    # if rooms == check_state_6:
    #     assert hash_rooms(check_state_7) in steps_dict
    #     assert steps_dict[hash_rooms(check_state_7)] == 5513
    #     # print("Check 7 passed")

    # rms = {A: (A,), B: (B, B), C: (C, C), D: (D,)}
    # hlwy = {LF: (), LB: (), RF: (A,), RB: (), AB: (), BC: (D,), CD: ()}
    # check_state_8 = {**rms, **hlwy}
    # if rooms == check_state_7:
    #     assert hash_rooms(check_state_8) in steps_dict
    #     assert steps_dict[hash_rooms(check_state_8)] == 8513
    #     # print("Check 8 passed")

    # rms = {A: (A,), B: (B, B), C: (C, C), D: (D, D)}
    # hlwy = {LF: (), LB: (), RF: (A,), RB: (), AB: (), BC: (), CD: ()}
    # check_state_9 = {**rms, **hlwy}
    # if rooms == check_state_8:
    #     assert hash_rooms(check_state_9) in steps_dict
    #     assert steps_dict[hash_rooms(check_state_9)] == 12513
    #     # print("Check 9 passed")

    # rms = {A: (A, A), B: (B, B), C: (C, C), D: (D, D)}
    # hlwy = {LF: (), LB: (), RF: (), RB: (), AB: (), BC: (), CD: ()}
    # check_state_10 = {**rms, **hlwy}
    # if rooms == check_state_9:
    #     assert finished_steps == 12521
    #     # print("Check 10 passed")

print(finished_steps)

# print(f"Time taken: {dt.now() - start}")
