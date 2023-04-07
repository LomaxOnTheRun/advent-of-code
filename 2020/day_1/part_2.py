# Start time: 13:17
# End time: 13:22

import aocd

data = """1721
979
366
299
675
1456"""

data = aocd.get_data(year=2020, day=1)


def get_answer(data: str) -> int:
    """
    Find three numbers that add up to 2020 in data, then multiply them together.
    """

    # Convert data to a list of ints
    data = [int(line) for line in data.splitlines()]

    # Find three numbers in data that add up to 2020
    nums = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            for k in range(j + 1, len(data)):
                if data[i] + data[j] + data[k] == 2020:
                    nums = [data[i], data[j], data[k]]
                    break

    # Multiply them together
    return nums[0] * nums[1] * nums[2]


print(get_answer(data))
