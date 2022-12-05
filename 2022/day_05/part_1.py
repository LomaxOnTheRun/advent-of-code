# Start time: 06:34
# End time: 06:56

import aocd

data = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

data = aocd.get_data(year=2022, day=5)

start, moves = [part.split("\n") for part in data.split("\n\n")]

stacks = [[] for _ in range((len(start[0]) + 1) // 4)]
for line in start[:-1]:
    for i, stack in enumerate(stacks):
        crate = line[(i * 4) + 1]
        if crate != " ":
            stack.insert(0, crate)

for move in moves:
    _, num_crates, _, start, _, end = move.split()
    for crate in range(int(num_crates)):
        crate = stacks[int(start) - 1].pop()
        stacks[int(end) - 1].append(crate)

print("".join([stack[-1] for stack in stacks]))
