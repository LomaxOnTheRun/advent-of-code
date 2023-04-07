# Start time: 13:30
# End time: 13:32

import aocd

data = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
"""

data = aocd.get_data(year=2020, day=2)


def get_answer(data: str) -> int:
    """
    Get least and most chars in a password, then check if the password contains
    that many of the specified char.
    """

    # Convert data to a list of ints
    data = [line for line in data.splitlines()]

    # Find three numbers in data that add up to 2020
    valid_passwords = 0
    for line in data:
        # Split line into parts
        parts = line.split(" ")
        # Get least and most chars
        least_most = parts[0].split("-")
        least = int(least_most[0])
        most = int(least_most[1])
        # Get char
        char = parts[1][0]
        # Get password
        password = parts[2]
        # Check if password contains char enough times
        if least <= password.count(char) <= most:
            valid_passwords += 1

    return valid_passwords


print(get_answer(data))
