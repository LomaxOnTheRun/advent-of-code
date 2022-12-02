# Start time: 06:40
# End time: 06:49

import aocd

data = """A Y
B X
C Z"""

data = aocd.get_data(year=2022, day=2)

points = {"X": 0, "Y": 3, "Z": 6}
win = {"A": 2, "B": 3, "C": 1}
draw = {"A": 1, "B": 2, "C": 3}
loss = {"A": 3, "B": 1, "C": 2}
outcomes = {"X": loss, "Y": draw, "Z": win}

score = 0
for line in data.split("\n"):
    elf, outcome = line.split(" ")
    score += points[outcome]
    score += outcomes[outcome][elf]

print(score)
