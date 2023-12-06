# Start time: 06:40
# End time: 08:20

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


def create_conv_map(map_data: str) -> list[list[int, int, int]]:
    return [[int(x) for x in line.split()] for line in map_data.splitlines()]


def create_conv_maps_list(map_strs: list[str]) -> list[dict[int, int]]:
    conv_maps = []
    for map_str in map_strs:
        map_data = map_str.split(" map:\n")[1]
        conv_maps.append(create_conv_map(map_data))
    return conv_maps


def get_seed_location(value: int, conv_maps: list) -> int:
    for conv_map in conv_maps:
        for dest_start, src_start, rng in conv_map:
            if src_start <= value < src_start + rng:
                value = dest_start + value - src_start
                break
    return value


seeds_str, *map_strs = data.split("\n\n")
seeds = [int(x) for x in seeds_str.split()[1:]]
conv_maps = create_conv_maps_list(map_strs)
print(min(get_seed_location(seed, conv_maps) for seed in seeds))
