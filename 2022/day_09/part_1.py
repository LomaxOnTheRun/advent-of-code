# Start time: 12:27
# End time: 12:39

import aocd

data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

data = aocd.get_data(year=2022, day=9)

head_x, head_y = 0, 0
tail_x, tail_y = 0, 0
tail_trail = set()
for line in data.split("\n"):
    dir, num = line.split(" ")

    for _ in range(int(num)):

        if dir == "R":
            head_x += 1
            if abs(head_x - tail_x) > 1:
                tail_x += 1
                tail_y = head_y

        if dir == "L":
            head_x -= 1
            if abs(head_x - tail_x) > 1:
                tail_x -= 1
                tail_y = head_y

        if dir == "U":
            head_y += 1
            if abs(head_y - tail_y) > 1:
                tail_y += 1
                tail_x = head_x

        if dir == "D":
            head_y -= 1
            if abs(head_y - tail_y) > 1:
                tail_y -= 1
                tail_x = head_x

        tail_trail.add((tail_x, tail_y))

print(len(tail_trail))
