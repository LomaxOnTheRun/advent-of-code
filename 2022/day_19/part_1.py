# Start time: 10:57
# End time: 16:37

import aocd, math, time

data = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""

data = aocd.get_data(year=2022, day=19)


CostsType = dict[str, dict[str, int]]


def get_costs(blueprint_data: str) -> CostsType:
    split_data = blueprint_data.split(":")[1].split(".")[:-1]

    costs = {}
    for line in split_data:
        words = line.strip().split(" ")

        robot = words[1]

        robot_costs = {}
        i = 4
        while i < len(words):
            mat_type = words[i + 1]
            num_required = int(words[i])
            robot_costs[mat_type] = num_required
            i += 3

        costs[robot] = robot_costs

    return costs


def can_build_robot(next_robot: str, materials: dict, costs: CostsType) -> bool:
    robot_costs = costs[next_robot]
    for mat_type, num_required in robot_costs:
        if materials[mat_type] < num_required:
            return False
    return True


def get_num_moves_to_build(
    robots: dict, materials: dict, next_robot: str, costs: CostsType
) -> int:
    robot_costs = costs[next_robot]
    max_moves = -1
    for mat_type, num_required in robot_costs.items():
        if robots[mat_type] == 0:
            return 24

        num_still_required = num_required - materials[mat_type]
        moves_required = math.ceil(num_still_required / robots[mat_type])
        max_moves = max(moves_required, max_moves, 0)

    # We add 1 because it takes a turn to build the robot
    return max_moves + 1


def collect_materials(robots: dict, materials: dict, num_moves: int = 1) -> dict:
    new_materials = {mat_type: num for mat_type, num in materials.items()}
    for mat_type, num_robots in robots.items():
        new_materials[mat_type] += num_robots * num_moves
    return new_materials


def build_robot(
    robots: dict, new_materials: dict, next_robot: str, costs: CostsType
) -> dict:
    new_robots = {mat_type: num for mat_type, num in robots.items()}
    robot_costs = costs[next_robot]
    for mat_type, num_required in robot_costs.items():
        new_materials[mat_type] -= num_required
    new_robots[next_robot] += 1
    return new_robots


def next_move(
    robots: dict,
    materials: dict,
    robots_to_build: list,
    blueprint_id: int,
    move_num: int,
    costs: CostsType,
):

    max_geodes = MAX_GEODES[blueprint_id]
    current_geodes = materials["geode"]

    if robots["geode"] == 0:
        i = 0
        potential_geodes = 0
        while max_geodes >= potential_geodes:
            i += 1
            potential_geodes += i
            if move_num > TOTAL_MOVES - i:
                return

    if robots["geode"] == 1:
        i = 1
        potential_geodes = 1
        while max_geodes >= current_geodes + potential_geodes:
            i += 1
            potential_geodes += i
            if move_num > TOTAL_MOVES - i:
                return

    if robots_to_build:
        next_robot = robots_to_build[-1]
        num_moves_to_build = get_num_moves_to_build(
            robots, materials, next_robot, costs
        )

        if move_num + num_moves_to_build > TOTAL_MOVES:
            moves_left = TOTAL_MOVES - move_num
            new_materials = collect_materials(robots, materials, moves_left)
            MAX_GEODES[blueprint_id] = max(MAX_GEODES[blueprint_id], materials["geode"])
            COMBINATIONS_TRIED[blueprint_id].append(robots_to_build)
            return

        new_materials = collect_materials(robots, materials, num_moves_to_build)
        new_robots = build_robot(robots, new_materials, next_robot, costs)

    else:
        new_robots = robots
        new_materials = materials
        num_moves_to_build = 0

    for mat_type in ("geode", "obsidian", "clay", "ore"):

        # Skip impossible next robot types
        if mat_type == "obsidian" and robots["clay"] == 0:
            continue
        if mat_type == "geode" and (robots["clay"] == 0 or robots["obsidian"] == 0):
            continue

        next_move(
            new_robots,
            new_materials,
            robots_to_build + [mat_type],
            blueprint_id,
            move_num + num_moves_to_build,
            costs,
        )


TOTAL_MOVES = 24

MATERIAL_TYPES = ("ore", "clay", "obsidian", "geode")

COMBINATIONS_TRIED = {}
MAX_GEODES = {}  # {blueprint_id: max_geodes}

for blueprint_data in data.split("\n"):

    start_time = time.perf_counter()

    robots = {mat_type: 0 for mat_type in MATERIAL_TYPES}
    robots["ore"] = 1
    materials = {mat_type: 0 for mat_type in MATERIAL_TYPES}

    blueprint_id = int(blueprint_data.split()[1][:-1])
    COMBINATIONS_TRIED[blueprint_id] = []
    MAX_GEODES[blueprint_id] = 0

    costs = get_costs(blueprint_data)

    next_move(robots, materials, [], blueprint_id, 0, costs)

    end_time = time.perf_counter()
    # print(f"Total run time: {end_time - start_time:.2f}s")
    # print(f"Num combinations tried: {len(COMBINATIONS_TRIED[blueprint_id])}")
    # print(f"Num geodes: {MAX_GEODES[blueprint_id]}")
    # print()

print(
    sum([blueprint_id * num_geodes for blueprint_id, num_geodes in MAX_GEODES.items()])
)
