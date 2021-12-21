import aocd

data = """Player 1 starting position: 4
Player 2 starting position: 8"""

data = aocd.get_data(year=2021, day=21)

pos = [int(data[28]), int(data[-1])]
score = [0, 0]

player = 0
die = 99

rolled = 0
while True:
    for _ in range(3):
        die += 1
        rolled += 1
        pos[player] += (die % 100) + 1
    score[player] += ((pos[player] - 1) % 10) + 1

    if score[player] >= 1000:
        print(score[1 - player] * rolled)
        break

    player = 1 - player
