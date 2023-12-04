# Start time: 06:51
# End time: 07:05

import aocd

data = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

data = aocd.get_data(year=2023, day=4)

copies = {}
for line in data.splitlines():
    card = int(line.split(":")[0].split()[1])
    win = set(line.split(":")[1].split("|")[0].split())
    have = set(line.split("|")[1].split())
    for i in range(card + 1, card + len(win & have) + 1):
        num_copies = (copies[card] if card in copies else 0) + 1
        copies[i] = copies[i] + num_copies if i in copies else num_copies

print(sum(copies.values()) + len(data.splitlines()))
