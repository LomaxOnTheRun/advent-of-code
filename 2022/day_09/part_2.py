# Start time: 12:39
# End time: 14:22

import aocd

data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

data = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

data = """R 5
U 8"""

data = aocd.get_data(year=2022, day=9)


def print_rope(rope_x, rope_y, map_size):
    for y in range(map_size):
        row = ""
        for x in range(map_size):
            char = "."
            for piece in range(9, -1, -1):
                pos_x, pos_y = rope_x[piece], rope_y[piece]
                # print((x, y), (pos_x, pos_y), f"piece: {piece}")
                if pos_x == x and pos_y == map_size - 1 - y:
                    # print(f"Piece found: {piece} at {(pos_x, pos_y)}")
                    char = str(piece)
            row += char
        print(row)
    print("\n")


rope_length = 10
rope_x, rope_y = [0] * rope_length, [0] * rope_length
tail_trail = set()
for line in data.split("\n"):
    dir, num = line.split(" ")

    for _ in range(int(num)):

        if dir == "R":
            rope_x[0] += 1
        if dir == "L":
            rope_x[0] -= 1
        if dir == "U":
            rope_y[0] += 1
        if dir == "D":
            rope_y[0] -= 1

        for piece in range(1, rope_length):
            diff_x = rope_x[piece - 1] - rope_x[piece]
            diff_y = rope_y[piece - 1] - rope_y[piece]

            if abs(diff_x) > 1:
                rope_x[piece] += int(diff_x / abs(diff_x))
                if diff_y:
                    rope_y[piece] += int(diff_y / abs(diff_y))

            elif abs(diff_y) > 1:
                rope_y[piece] += int(diff_y / abs(diff_y))
                if diff_x:
                    rope_x[piece] += int(diff_x / abs(diff_x))

        tail_trail.add((rope_x[-1], rope_y[-1]))

        # print_rope(rope_x, rope_y, 10)

print(len(tail_trail))

# 2498 is too high
