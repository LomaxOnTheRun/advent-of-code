# Start time: 06:36
# End time: 7:36

import aocd

data = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""

data = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""

data = aocd.get_data(year=2022, day=25)

SNAFU_DIGIT_VALUES = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}


def snafu_to_dec(snafu: str) -> int:
    dec = 0
    for i, digit in enumerate(snafu[::-1]):
        multiplier = pow(5, i)
        digit_value = SNAFU_DIGIT_VALUES[digit]
        dec += multiplier * digit_value
    return dec


def dec_to_snafu(dec: int) -> str:
    num_snafu_chars = 1
    while snafu_to_dec("2" * num_snafu_chars) < dec:
        num_snafu_chars += 1

    snafu = "=" * num_snafu_chars
    for i in range(len(snafu)):
        for snafu_char in "210-=":
            snafu_chars = list(snafu)
            snafu_chars[i] = snafu_char
            new_snafu = "".join(snafu_chars)
            if snafu_to_dec(new_snafu) <= dec:
                snafu = new_snafu
                break

    return snafu


print(dec_to_snafu(sum([snafu_to_dec(snafu) for snafu in data.split()])))
