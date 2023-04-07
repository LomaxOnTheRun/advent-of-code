# Start time: 13:32
# End time: 13:34

import aocd

data = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
"""

data = aocd.get_data(year=2020, day=2)


def get_answer(data: str) -> int:
    """
    Get the positions of the char in the password, then check if the password
    contains the char at one of those positions.
    """

    # Convert data to a list of ints
    data = [line for line in data.splitlines()]

    # Find three numbers in data that add up to 2020
    valid_passwords = 0
    for line in data:
        # Split line into parts
        parts = line.split(" ")
        # Get positions
        positions = parts[0].split("-")
        pos1 = int(positions[0]) - 1
        pos2 = int(positions[1]) - 1
        # Get char
        char = parts[1][0]
        # Get password
        password = parts[2]
        # Check if password contains char at one of the positions
        if (password[pos1] == char) ^ (password[pos2] == char):
            valid_passwords += 1

    return valid_passwords


print(get_answer(data))
