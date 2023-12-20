# Start time: 18:41
# End time:

import aocd, time

data = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

# data = """.???#??.???????. 4,3"""
# data = """???.### 1,1,3"""
# data = """.??..??...?##. 1,1,3"""
# data = """#?#????????.?#. 4,1,2,1"""
# data = """????#??.#. 1,4,1"""
# data = """??#???.??#???#?# 2,3,4"""
data = """?###???????? 3,2,1"""
# data = """????.#...#... 4,1,1"""
# data = """??????.????? 1,1,1,1"""

data = aocd.get_data(year=2023, day=12)

t0 = time.time()


def get_num_options(sections: tuple[str], blocks: tuple[int], cache: dict) -> int:
    # print(sections, blocks)
    # time.sleep(0.1)

    if (sections, blocks) in cache:
        # print("Cache use:", cache[(sections, blocks)])
        return cache[(sections, blocks)]

    # Failure: nowhere to put blocks
    if not sections:
        # print("Failure: nowhere to put blocks")
        return 0

    num_blocks_in_sections = 0
    for section in sections:
        num_blocks_in_sections += len(["#" for char in section if char == "#"])

    # Success
    if not blocks:
        if num_blocks_in_sections > 0:
            return 0
        # print("Success")
        return 1

    # Failure: too few blocks remaining
    if sum(blocks) < num_blocks_in_sections:
        # print("Failure: too few blocks remaining")
        return 0

    first_section = sections[0]
    first_block = blocks[0]
    # Failure: impossible configuration
    if "#" in first_section and len(first_section) < first_block:
        # print("Failure: impossible configuration")
        return 0

    # Skip section and keep going
    if len(first_section) < first_block:
        return get_num_options(sections[1:], blocks, cache)

    total = 0
    # Put blocks at start of section
    if len(first_section) == first_block or first_section[first_block] == "?":
        # print("Placing first block at start of sections", first_block, sections)
        new_sections = (first_section[first_block + 1 :], *sections[1:])
        total += get_num_options(new_sections, blocks[1:], cache)
    # Don't put block at start of section
    if first_section[0] != "#":
        # print("Placing first block at start of sections", first_block, sections)
        new_sections = (first_section[1:], *sections[1:])
        total += get_num_options(new_sections, blocks, cache)

    # print("Cache save:", (sections, blocks), total)
    cache[(sections, blocks)] = total

    # print("Current total:", total, sections, blocks)

    return total


max_line, max_value = -1, 0

total = 0
for i, line in enumerate(data.splitlines()):
    # print(i, line)
    springs_str, blocks = line.split(" ")
    multiplier = 5
    # multiplier = 1
    springs_str = "?".join([springs_str] * multiplier)
    blocks = tuple([int(x) for x in blocks.split(",")] * multiplier)
    sections = tuple(section for section in springs_str.split(".") if section)

    # Ignore all sections which are too small to accommodate any block
    sections = tuple(section for section in sections if len(section) >= min(blocks))

    cache = {}
    line_total = get_num_options(sections, blocks, cache)
    total += line_total

    # print("Line total:", line_total)
    # print("Tried:", tried)

    if line_total > max_value:
        max_line = i
        max_value = line_total

print(total)

# print(f"Total tile: {time.time() - t0:.1f}s")

# print("Max line:", max_line, max_value)
