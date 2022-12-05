# 18 lines

import aocd


def create_start_stacks(initial, stack_nums):
    stacks_list = zip(*[list(line[1::4]) for line in initial[:-1]])
    stacks = {num: stack for num, stack in zip(stack_nums, stacks_list)}
    return {num: [c for c in stacks[num] if c != " "] for num in stack_nums}


def do_move_part_1(stacks, num_crates, start, end):
    [stacks[end].insert(0, stacks[start].pop(0)) for _ in range(int(num_crates))]


def do_move_part_2(stacks, num_crates, start, end):
    crates = stacks[start][: int(num_crates)]
    stacks[start] = stacks[start][int(num_crates) :]
    stacks[end] = crates + stacks[end]


def solve_part(initial, stack_nums, moves, do_move):
    stacks = create_start_stacks(initial, stack_nums)
    [do_move(stacks, *move.split()[1::2]) for move in moves]
    print("".join([stacks[stack_num][0] for stack_num in stack_nums]))


initial, moves = [_.split("\n") for _ in aocd.get_data(year=2022, day=5).split("\n\n")]
solve_part(initial, initial[-1].split(), moves, do_move_part_1)
solve_part(initial, initial[-1].split(), moves, do_move_part_2)
