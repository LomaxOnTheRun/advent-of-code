# Start time: 06:33
# End time: 06:40

import aocd

data = """A Y
B X
C Z"""

data = aocd.get_data(year=2022, day=2)

points = {"X": 1, "Y": 2, "Z": 3}
wins = ["A Y", "B Z", "C X"]
draws = ["A X", "B Y", "C Z"]

score = 0
for line in data.split("\n"):
    elf, me = line.split(" ")
    score += points[me]
    if line in wins:
        score += 6
    elif line in draws:
        score += 3

print(score)
