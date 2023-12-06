# Start time: 08:20
# End time:

import aocd

data = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

data = aocd.get_data(year=2023, day=5)

conv_map_type = list[list[int, int, int]]
seed_ranges_type = list[tuple[int, int, int]]


def create_seed_ranges(seeds_str: str) -> seed_ranges_type:
    seed_start = [int(x) for x in seeds_str.split(": ")[1].split()[::2]]
    seed_range = [int(x) for x in seeds_str.split(": ")[1].split()[1::2]]
    return [(start, start, rng) for start, rng in zip(seed_start, seed_range)]


def create_conv_map(map_data: str) -> conv_map_type:
    return [[int(x) for x in line.split()] for line in map_data.splitlines()]


def create_conv_maps_list(map_strs: list[str]) -> list[conv_map_type]:
    conv_maps = []
    for map_str in map_strs:
        map_data = map_str.split(" map:\n")[1]
        conv_maps.append(create_conv_map(map_data))
    return conv_maps


def print_seed_ranges(seed_ranges: seed_ranges_type):
    print("\nSeed ranges")
    for location, seed, rng in seed_ranges:
        min_loc = location
        max_loc = location + rng
        min_seed = seed
        max_seed = seed + rng
        print(f"loc: {min_loc} => {max_loc}, seed: {min_seed} => {max_seed}")


def print_conv_line(dest_start: int, src_start: int, rng: int):
    print(f"{dest_start=}, {src_start=}, {rng=}")


def print_conv_map(conv_map: conv_map_type):
    print("\nConv map")
    for dest_start, src_start, rng in conv_map:
        # print(f"{dest_start=}, {src_start=}, {rng=}")
        min_dest = dest_start
        max_dest = dest_start + rng
        min_src = src_start
        max_src = src_start + rng
        print(f"dest: {min_dest} => {max_dest}, src: {min_src} => {max_src}")


def requires_split(location: int, seed_rng: int, dest_start: int, rng: int) -> bool:
    # Location starts in conv line
    if dest_start < location < dest_start + rng < location + seed_rng:
        return True
    # Location ends in conv line
    if location < dest_start < location + seed_rng < dest_start + rng:
        return True
    return False


def split_seed_ranges(
    seed_ranges: seed_ranges_type, src_start: int, rng: int
) -> seed_ranges_type:
    new_seed_ranges = []
    for location, seed_start, seed_rng in seed_ranges:
        # Location starts in conv line
        if src_start < location < src_start + rng < location + seed_rng:
            offset = src_start + rng - location
            # Left
            new_seed_ranges.append((location, seed_start, offset))
            # Right
            new_seed_ranges.append(
                (src_start + rng, seed_start + offset, seed_rng - offset)
            )
        # Location ends in conv line
        elif location < src_start < location + seed_rng < src_start + rng:
            offset = src_start - location
            # Left
            new_seed_ranges.append((location, seed_start, offset))
            # Right
            new_seed_ranges.append((src_start, seed_start + offset, seed_rng - offset))
        else:
            new_seed_ranges.append((location, seed_start, seed_rng))
    return new_seed_ranges


def update_seed_ranges_locations(
    seed_ranges: seed_ranges_type, conv_map: conv_map_type
) -> seed_ranges_type:
    new_seed_ranges = []
    for location, seed_start, seed_rng in seed_ranges:
        for dest_start, src_start, rng in conv_map:
            if src_start <= location < src_start + rng:
                location = dest_start + location - src_start
                break
        new_seed_ranges.append((location, seed_start, seed_rng))
    return new_seed_ranges


seeds_str, *map_strs = data.split("\n\n")
# [(dest, src, range), ...]
conv_maps = create_conv_maps_list(map_strs)
# [(location, seed_start, range), ...]
seed_ranges = create_seed_ranges(seeds_str)

# seed_ranges = [
#     (79, 79, 1),
#     (14, 14, 1),
#     (55, 55, 1),
#     (13, 13, 1),
# ]

for conv_map in conv_maps[:]:
    # conv_map = conv_maps[0]
    print("\n+++ New conv map +++")
    print_seed_ranges(seed_ranges)
    print_conv_map(conv_map)

    for dest_start, src_start, rng in conv_map:
        print("\n- Splitting seed ranges")
        seed_ranges = split_seed_ranges(seed_ranges, src_start, rng)
        print_seed_ranges(seed_ranges)

    print("\n- Updating seed locations")
    seed_ranges = update_seed_ranges_locations(seed_ranges, conv_map)
    print_seed_ranges(seed_ranges)

print(min(loc for loc, _, _ in seed_ranges))
