# Start time: 06:38
# End time: 06:42

import aocd

data = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

data = aocd.get_data(year=2023, day=9)


def get_diff_line(num_line: list[int]) -> list[int]:
    """
    Create list of differences for given list.
    """
    diff_line = []
    for i in range(1, len(num_line)):
        diff_line.append(num_line[i] - num_line[i - 1])
    return diff_line


def get_all_diff_lines(num_line: list[int]) -> list[list[int]]:
    """
    Get diff lines until we have a line of all zeros.
    """
    num_lines = [num_line]
    diff_line = get_diff_line(num_line)
    while not all(diff == 0 for diff in diff_line):
        num_lines.append(diff_line)
        diff_line = get_diff_line(diff_line)
    num_lines.append(diff_line)
    return num_lines


def get_next_num(num_line: list[int]) -> int:
    """
    Add the last diff value of each line to the end number of the previous diff line.
    """
    num_lines = get_all_diff_lines(num_line)
    last_nums = [line[-1] for line in num_lines[::-1]]
    for i in range(1, len(last_nums)):
        last_nums[i] += last_nums[i - 1]
    return last_nums[-1]


total = 0
for line in data.splitlines():
    next_num = get_next_num([int(val) for val in line.split(" ")[::-1]])
    total += next_num

print(total)
