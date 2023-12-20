# Start time: 18:02
# End time: 18:15

import aocd

data = """HASH"""
data = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

data = aocd.get_data(year=2023, day=15)


def get_hash(word: str) -> int:
    # word = word.split("=")[0].split("-")[0]
    value = 0
    for char in word:
        value += ord(char)
        value = value * 17
        value = value % 256
    return value


print(sum(get_hash(word) for word in data.split(",")))
