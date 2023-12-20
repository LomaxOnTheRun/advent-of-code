# Start time: 07:54
# End time: 18:41

import aocd, re

data = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

data = """.???#??.???????. 4,3"""
# data = """???.### 1,1,3"""
# data = """.??..??...?##. 1,1,3"""

data = aocd.get_data(year=2023, day=12)


def try_next(springs_str: str, blocks: list[int], total: int) -> int:
    # print(springs_str)
    # End
    if "?" not in springs_str:
        # Success
        if [len(x) for x in springs_str.split(".") if x] == blocks:
            # print("Success:", total + 1)
            return total + 1
        # Failure
        # print("Failure:", total)
        return total

    # Early failure
    first_section = springs_str.split(".")[0]
    if "#" in first_section and len(first_section) < blocks[0]:
        # print("Early failure:", total)
        return total

    # Try unbroken
    total = try_next(re.sub("\?", ".", springs_str, 1), blocks, total)
    # print("After unbroken:", total)
    # Try broken
    total = try_next(re.sub("\?", "#", springs_str, 1), blocks, total)
    # print("After broken:", total)

    return total


total = 0
for line in data.splitlines():
    # print(line)
    springs_str, blocks = line.split(" ")
    blocks = [int(x) for x in blocks.split(",")]

    total += try_next(springs_str, blocks, 0)

print(total)
