import aocd
from datetime import datetime as dt


def example_1():
    # SANITY CHECK 1
    example_data = """inp x
        mul x -1"""
    in_out = [("0", 0), ("1", -1), ("2", -2)]
    instructions = get_instructions(example_data)
    for monad_digit, output_val in in_out:
        mem = {W: 0, X: 0, Y: 0, Z: 0}
        mem = run_instructions_group(instructions[0], int(monad_digit), mem)
        assert mem[X] == output_val


def example_2():
    example_data = """inp w
        add z w
        mod z 2
        div w 2
        add y w
        mod y 2
        div w 2
        add x w
        mod x 2
        div w 2
        mod w 2"""
    in_out = [
        ("0", [0, 0, 0, 0]),
        ("1", [0, 0, 0, 1]),
        ("2", [0, 0, 1, 0]),
        ("3", [0, 0, 1, 1]),
        ("4", [0, 1, 0, 0]),
        ("5", [0, 1, 0, 1]),
        ("6", [0, 1, 1, 0]),
        ("7", [0, 1, 1, 1]),
        ("8", [1, 0, 0, 0]),
        ("9", [1, 0, 0, 1]),
    ]
    instructions = get_instructions(example_data)
    for monad_digit, output_val in in_out:
        mem = {W: 0, X: 0, Y: 0, Z: 0}
        mem = run_instructions_group(instructions[0], int(monad_digit), mem)
        assert mem[W] == output_val[0]
        assert mem[X] == output_val[1]
        assert mem[Y] == output_val[2]
        assert mem[Z] == output_val[3]


def example_3():
    example_data = """inp z
        inp x
        mul z 3
        eql z x"""
    in_out = [("00", 1), ("13", 1), ("26", 1), ("10", 0), ("12", 0)]
    instructions = get_instructions(example_data)
    for monad, output_val in in_out:
        mem = [{W: 0, X: 0, Y: 0, Z: 0}]
        mems = run_instructions(monad, instructions, mem)
        assert (
            mems[-1][Z] == output_val
        ), f"{monad}, {output_val} => {mem[Z]} != {output_val}"


def example_4():
    example_data = """inp x
        add x 1
        inp y
        div y x
        inp z
        mul z y"""
    monad = "148"
    in_out = [
        ([{W: 0, X: 0, Y: 0, Z: 0}], 16),
        ([{W: 0, X: 0, Y: 0, Z: 0}, {W: 0, X: 4, Y: 0, Z: 0}], 8),
        ([{W: 0, X: 0, Y: 0, Z: 0}, {W: 0, X: 1, Y: 0, Z: 0}], 32),
        (
            [
                {W: 0, X: 0, Y: 0, Z: 0},
                {W: 0, X: 0, Y: 0, Z: 0},
                {W: 0, X: 0, Y: 0, Z: 0},
            ],
            0,
        ),
        (
            [
                {W: 0, X: 0, Y: 0, Z: 0},
                {W: 0, X: 0, Y: 0, Z: 0},
                {W: 0, X: 0, Y: 1, Z: 0},
            ],
            8,
        ),
        (
            [
                {W: 0, X: 0, Y: 0, Z: 0},
                {W: 0, X: 0, Y: 0, Z: 0},
                {W: 0, X: 0, Y: 2, Z: 0},
            ],
            16,
        ),
    ]
    instructions = get_instructions(example_data)
    for mems, z in in_out:
        mems = run_instructions(monad, instructions, mems)
        assert mems[-1][Z] == z


class EarlyStop(Exception):
    def __init__(self, inp_index):
        self.inp_index = inp_index


def is_var(var_or_number):
    return var_or_number in "wxyz"


def inp(a, b, mem):
    mem[a] = b
    return mem


def add(a, b, mem):
    val = mem[b] if is_var(b) else int(b)
    mem[a] += val
    return mem


def mul(a, b, mem):
    val = mem[b] if is_var(b) else int(b)
    mem[a] *= val
    return mem


def div(a, b, mem):
    val = mem[b] if is_var(b) else int(b)
    mem[a] = int(mem[a] / val)
    return mem


def mod(a, b, mem):
    val = mem[b] if is_var(b) else int(b)
    mem[a] %= val
    return mem


def eql(a, b, mem):
    val = mem[b] if is_var(b) else int(b)
    mem[a] = int(mem[a] == val)
    return mem


def is_valid(mem):
    return mem["z"] == 0


def copy_mem(mem):
    return {k: v for k, v in mem.items()}


def run_instructions_group(instructions_group, input_val, mem):
    for op_name, a, b in instructions_group:
        if op_name == "inp":
            b = input_val

        op = OPERATIONS[op_name]
        mem = op(a, b, mem)

    return mem


def run_instructions(monad, instructions, partial_mems, debug=False):
    # Current working memory
    mem = copy_mem(partial_mems[-1])

    for inp_index, instruction_group in enumerate(instructions):
        if inp_index < len(partial_mems) - 1:
            continue

        for op_name, a, b in instruction_group:
            if debug:
                print("len(partial_mems)", len(partial_mems))
                print("instruction", (op_name, a, b))
                print("inp_index", inp_index)
                print("int(monad[inp_index])", int(monad[inp_index]))

            if op_name == "inp":
                b = int(monad[inp_index])

            op = OPERATIONS[op_name]
            mem = op(a, b, mem)

        partial_mems.append(copy_mem(mem))

    return partial_mems


def update_times_dict(last_dt, times, name):
    new_dt = dt.now()
    diff = new_dt - last_dt
    times[name] = diff if name not in times else times[name] + diff
    return new_dt


def get_instructions(data):
    """Split instructions into 14 groups (one group per input)."""
    instructions = []
    for line in data.split("\n"):
        op_name, ab = line.strip().split(" ", 1)
        if op_name == "inp":
            instructions.append([])
            ab += " "
        a, b = ab.split(" ")
        instructions[-1].append((op_name, a, b))
    return instructions


data = aocd.get_data(year=2021, day=24)

W, X, Y, Z = "wxyz"

OPERATIONS = {"inp": inp, "add": add, "mul": mul, "div": div, "mod": mod, "eql": eql}

# Samity checks
example_1()
example_2()
example_3()
example_4()

# Start the counter
times = {}
start = dt.now()
last_dt = dt.now()

monad = 99999999999999

# Keep track of state before every new input
partial_mems = [{W: 0, X: 0, Y: 0, Z: 0}]

instructions = get_instructions(data)

last_dt = update_times_dict(last_dt, times, "setup")

i = 0
while True:
    i += 1

    partial_mems = run_instructions(str(monad), instructions, partial_mems, debug=False)

    last_dt = update_times_dict(last_dt, times, "run_instructions")

    if is_valid(partial_mems[-1]):
        break

    last_dt = update_times_dict(last_dt, times, "valid_check")

    prev_monad = monad
    monad -= 1
    while "0" in str(monad):
        monad -= 1

    last_dt = update_times_dict(last_dt, times, "update_monad")

    # Only keep relevant partial mems
    for monad_index in range(14):
        if str(prev_monad)[monad_index] != str(monad)[monad_index]:
            partial_mems = partial_mems[: monad_index + 1]
            break

    last_dt = update_times_dict(last_dt, times, "update_partials")

    if i == 10000:
        print(f"\nTotal runs: {i}")
        print("\nTimes:")
        for name in times:
            print(f"- {name}: {str(times[name])}")
        print(f"\nLowest monad tried: {monad}")
        print(f"\nTotal time: {dt.now() - start}")
        exit()

print(f"Largest valid monad: {monad}")
