# 16 lines

import aocd


def tail_trail_length(rope_length):
    rope = [[0, 0] for _ in range(rope_length)]
    tail_trail = set()
    for line in aocd.get_data(year=2022, day=9).split("\n"):
        for _ in range(int(line[2:])):
            # Move the head
            move = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}
            rope[0] = [rope[0][i] + move[line[0]][i] for i in (0, 1)]

            # Move the rest of the string
            for piece in range(1, rope_length):
                # Difference in x and y between piece and next piece ahead
                diff = [rope[piece - 1][i] - rope[piece][i] for i in (0, 1)]

                # If there's a big enough difference, move the later piece
                for xy in (0, 1) if (abs(diff[0]) > 1 or abs(diff[1]) > 1) else ():
                    rope[piece][xy] += (1 if diff[xy] >= 0 else -1) if diff[xy] else 0

            # Keep track of tail positions
            tail_trail.add(tuple(rope[-1]))

    return len(tail_trail)


print(tail_trail_length(2))
print(tail_trail_length(10))
