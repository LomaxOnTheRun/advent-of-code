# Start time: 14:36
# End time: 14:53

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
def is_possible(pattern_left, towels):
    if not pattern_left:
        return True

    for towel in towels:
        len_towel = len(towel)
        if pattern_left[:len_towel] == towel:
            can_create = is_possible(pattern_left[len_towel:], towels)
            if can_create:
                return True

    return False


possible_patterns = 0
# print("Num patterns:", len(patterns))
for pattern in patterns:
    if is_possible(pattern, towels):
        possible_patterns += 1
        # print("Pattern possible")
    # print("Pattern not possible")
print(possible_patterns)
