# Start time: 13:12
# End time: 13:17

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
    Find two numbers that add up to 2020 in data, then multiply them together.
    """

    data = [int(line) for line in data.splitlines()]
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] + data[j] == 2020:
                return data[i] * data[j]


print(get_answer(data))


# To use aocd, you need to set the environment variable AOC_SESSION to your session cookie.
# To get your AOC_SESSION cookie, open the developer console in your browser, and copy the value of the session cookie.
