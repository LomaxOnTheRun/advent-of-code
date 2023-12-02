# Start time: 05:35
# End time: 06:09

import aocd, re

data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

data = aocd.get_data(year=2023, day=2)

MAX_VALS = {"red": 12, "green": 13, "blue": 14}
sum = 0

for line in data.split("\n"):
    red = max(int(val) for val in re.findall(r"(\d+) red", line))
    if red > MAX_VALS["red"]:
        continue
    green = max(int(val) for val in re.findall(r"(\d+) green", line))
    if green > MAX_VALS["green"]:
        continue
    blue = max(int(val) for val in re.findall(r"(\d+) blue", line))
    if blue > MAX_VALS["blue"]:
        continue

    game_id = int(line.split(":")[0][5:])
    sum += game_id
    # print(game_id, red, green, blue)

print(sum)

