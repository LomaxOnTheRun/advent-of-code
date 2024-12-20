# Start time: 14:53
# End time: 14:57

import aocd, functools

data = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

data = aocd.get_data(year=2024, day=19)

towels, patterns = data.split("\n\n")
towels = tuple(towels.split(", "))
patterns = patterns.split()

# print(towels)
# print(patterns)


@functools.cache
def get_num_possible(pattern_left, towels):
    if not pattern_left:
        return True

    num_possible = 0
    for towel in towels:
        len_towel = len(towel)
        if pattern_left[:len_towel] == towel:
            num_possible += get_num_possible(pattern_left[len_towel:], towels)

    return num_possible


possible_patterns = 0
for pattern in patterns:
    possible_patterns += get_num_possible(pattern, towels)
print(possible_patterns)
