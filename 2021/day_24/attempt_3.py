import aocd
from datetime import datetime as dt
import operator


def example_1():
    # SANITY CHECK 1
    example_data = """inp x
        mul x -1"""
    in_out = [("0", 0), ("1", -1), ("2", -2)]
    instructions = get_instructions(example_data)
    for monad_digit, output_val in in_out:
        # mem = {W: 0, X: 0, Y: 0, Z: 0}
        mem = (0, 0, 0, 0)
        mem = run_instructions_group(instructions[0], int(monad_digit), mem)
        # assert mem[X] == output_val
        assert mem[1] == output_val


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
        ("0", (0, 0, 0, 0)),
        ("1", (0, 0, 0, 1)),
        ("2", (0, 0, 1, 0)),
        ("3", (0, 0, 1, 1)),
        ("4", (0, 1, 0, 0)),
        ("5", (0, 1, 0, 1)),
        ("6", (0, 1, 1, 0)),
        ("7", (0, 1, 1, 1)),
        ("8", (1, 0, 0, 0)),
        ("9", (1, 0, 0, 1)),
    ]
    instructions = get_instructions(example_data)
    for monad_digit, output_val in in_out:
        # mem = {W: 0, X: 0, Y: 0, Z: 0}
        mem = (0, 0, 0, 0)
        mem = run_instructions_group(instructions[0], int(monad_digit), mem)
        # assert mem[W] == output_val[0]
        # assert mem[X] == output_val[1]
        # assert mem[Y] == output_val[2]
        # assert mem[Z] == output_val[3]
        assert mem == output_val


def example_3():
    example_data = """inp z
        inp x
        mul z 3
        eql z x"""
    in_out = [("00", 1), ("13", 1), ("26", 1), ("10", 0), ("12", 0)]
    instructions = get_instructions(example_data)
    for monad, output_val in in_out:
        # mem = [{W: 0, X: 0, Y: 0, Z: 0}]
        mem = [(0, 0, 0, 0)]
        mems = run_instructions(monad, instructions, mem)
        # assert (
        #     mems[-1][Z] == output_val
        # ), f"{monad}, {output_val} => {mem[Z]} != {output_val}"
        assert (
            mems[-1][3] == output_val
        ), f"{monad}, {output_val} => {mem[3]} != {output_val}"


def example_4():
    example_data = """inp x
        add x 1
        inp y
        div y x
        inp z
        mul z y"""
    monad = "148"
    # in_out = [
    #     ([{W: 0, X: 0, Y: 0, Z: 0}], 16),
    #     ([{W: 0, X: 0, Y: 0, Z: 0}, {W: 0, X: 4, Y: 0, Z: 0}], 8),
    #     ([{W: 0, X: 0, Y: 0, Z: 0}, {W: 0, X: 1, Y: 0, Z: 0}], 32),
    #     (
    #         [
    #             {W: 0, X: 0, Y: 0, Z: 0},
    #             {W: 0, X: 0, Y: 0, Z: 0},
    #             {W: 0, X: 0, Y: 0, Z: 0},
    #         ],
    #         0,
    #     ),
    #     (
    #         [
    #             {W: 0, X: 0, Y: 0, Z: 0},
    #             {W: 0, X: 0, Y: 0, Z: 0},
    #             {W: 0, X: 0, Y: 1, Z: 0},
    #         ],
    #         8,
    #     ),
    #     (
    #         [
    #             {W: 0, X: 0, Y: 0, Z: 0},
    #             {W: 0, X: 0, Y: 0, Z: 0},
    #             {W: 0, X: 0, Y: 2, Z: 0},
    #         ],
    #         16,
    #     ),
    # ]
    in_out = [
        ([(0, 0, 0, 0)], 16),
        ([(0, 0, 0, 0), (0, 4, 0, 0)], 8),
        ([(0, 0, 0, 0), (0, 1, 0, 0)], 32),
        ([(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)], 0),
        ([(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 1, 0)], 8),
        ([(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 2, 0)], 16),
    ]
    instructions = get_instructions(example_data)
    for mems, z in in_out:
        mems = run_instructions(monad, instructions, mems)
        # assert mems[-1][Z] == z
        assert mems[-1][3] == z


def example_5():
    partial_mems = [1, 2, 3, 4]
    in_out = [
        ("999", "998", [1, 2, 3]),
        ("999", "997", [1, 2, 3]),
        ("999", "989", [1, 2]),
        ("999", "899", [1]),  # The base one will always stay
    ]
    for old_monad, new_monad, expected_partials in in_out:
        new_partials = update_partial_mems(old_monad, new_monad, partial_mems)
        assert (
            new_partials == expected_partials
        ), f"{old_monad}, {new_monad} => {new_partials} != {expected_partials}"


class EarlyStop(Exception):
    def __init__(self, inp_index):
        self.inp_index = inp_index


def is_var(var_or_number):
    return var_or_number in "wxyz"


# def apply_op(a, b, op, w, x, y, z):
#     if a == W:
#         return {W: op(w, z), X: x, Y: y, Z: z}
#     if a == X:
#         return {W: w, X: op(x, b), Y: y, Z: z}
#     if a == Y:
#         return {W: w, X: x, Y: op(y, b), Z: z}
#     if a == Z:
#         return {W: w, X: x, Y: y, Z: op(z, b)}


# def inp(a, b, mem):
#     mem[a] = b
#     return mem


# def add(a, b, mem):
#     mem[a] += b
#     return mem

# def mul(a, b, mem):
#     mem[a] *= b
#     return mem


# def div(a, b, mem):
#     mem[a] = int(mem[a] / b)
#     return mem


# def mod(a, b, mem):
#     mem[a] %= b
#     return mem


# def eql(a, b, mem):
#     mem[a] = int(mem[a] == b)
#     return mem


# def is_valid(mem):
#     return mem["z"] == 0


# def copy_mem(mem):
#     return {k: v for k, v in mem.items()}


def apply_op(a, b, op, w, x, y, z):
    if a == W:
        return (op(w, b), x, y, z)
    if a == X:
        return (w, op(x, b), y, z)
    if a == Y:
        return (w, x, op(y, b), z)
    if a == Z:
        return (w, x, y, op(z, b))


def inp_base(_, y):
    return y


def inp(a, b, w, x, y, z):
    if a == W:
        return (b, x, y, z)
    if a == X:
        return (w, b, y, z)
    if a == Y:
        return (w, x, b, z)
    if a == Z:
        return (w, x, y, b)


def add_base(x, y):
    return x + y


def add(a, b, w, x, y, z):
    if a == W:
        return (w + b, x, y, z)
    if a == X:
        return (w, x + b, y, z)
    if a == Y:
        return (w, x, y + b, z)
    if a == Z:
        return (w, x, y, z + b)


def mul_base(x, y):
    return x * y


def mul(a, b, w, x, y, z):
    if a == W:
        return (w * b, x, y, z)
    if a == X:
        return (w, x * b, y, z)
    if a == Y:
        return (w, x, y * b, z)
    if a == Z:
        return (w, x, y, z * b)


def div_base(x, y):
    return int(x / y)


def div(a, b, w, x, y, z):
    if a == W:
        return (int(w / b), x, y, z)
    if a == X:
        return (w, int(x / b), y, z)
    if a == Y:
        return (w, x, int(y / b), z)
    if a == Z:
        return (w, x, y, int(z / b))


def mod_base(x, y):
    return x % y


def mod(a, b, w, x, y, z):
    if a == W:
        return (w % b, x, y, z)
    if a == X:
        return (w, x % b, y, z)
    if a == Y:
        return (w, x, y % b, z)
    if a == Z:
        return (w, x, y, z % b)


def eql_base(x, y):
    return int(x == y)


def eql(a, b, w, x, y, z):
    if a == W:
        return (int(w == b), x, y, z)
    if a == X:
        return (w, int(x == b), y, z)
    if a == Y:
        return (w, x, int(y == b), z)
    if a == Z:
        return (w, x, y, int(z == b))


def is_valid(z):
    return z == 0


def get_instructions(data):
    """Split instructions into 14 groups (one group per input)."""
    instructions = []
    for line in data.split("\n"):
        op_name, ab = line.strip().split(" ", 1)
        op = OPERATIONS[op_name]
        # op = BASE_OPERATIONS[op_name]
        if op == inp:
            # if op == inp_base:
            instructions.append([])
            ab += " INP"
        a, b = ab.split(" ")
        instructions[-1].append((op, a, b))
    return instructions


def run_instructions_group(instructions_group, input_val, mem):
    for op, a, b in instructions_group:
        if b == "INP":
            b = input_val
        # elif is_var(b):
        #     b = mem[b]
        elif b == W:
            b = mem[0]
        elif b == X:
            b = mem[1]
        elif b == Y:
            b = mem[2]
        elif b == Z:
            b = mem[3]
        mem = op(a, int(b), *mem)
        # mem = apply_op(a, int(b), op, *mem)
    return mem


def run_instructions(monad, instructions, partial_mems):
    # Current working memory
    # mem = copy_mem(partial_mems[-1])
    mem = partial_mems[-1]

    for inp_index, instructions_group in enumerate(instructions):
        if inp_index < len(partial_mems) - 1:
            continue

        input_val = int(monad[inp_index])
        mem = run_instructions_group(instructions_group, input_val, mem)

        # partial_mems.append(copy_mem(mem))
        partial_mems.append(mem)

    return partial_mems


def update_times_dict(last_dt, times, name):
    new_dt = dt.now()
    diff = new_dt - last_dt
    times[name] = diff if name not in times else times[name] + diff
    return new_dt


def update_partial_mems(old_monad, new_monad, partial_mems):
    old_str, new_str = str(old_monad), str(new_monad)
    for monad_index in range(14):
        if old_str[monad_index] != new_str[monad_index]:
            return partial_mems[: monad_index + 1]


data = aocd.get_data(year=2021, day=24)

W, X, Y, Z = "wxyz"

OPERATIONS = {"inp": inp, "add": add, "mul": mul, "div": div, "mod": mod, "eql": eql}
# BASE_OPERATIONS = {
#     "inp": inp_base,
#     "add": add_base,
#     "mul": mul_base,
#     "div": div_base,
#     "mod": mod_base,
#     "eql": eql_base,
# }

# Samity checks
example_1()
example_2()
example_3()
example_4()
example_5()

# Start the counter
times = {}
start = dt.now()
last_dt = dt.now()

monad = 99999999999999

# Keep track of state before every new input
# partial_mems = [{W: 0, X: 0, Y: 0, Z: 0}]
partial_mems = [(0, 0, 0, 0)]

instructions = get_instructions(data)

last_dt = update_times_dict(last_dt, times, "setup")

i = 0
while True:
    i += 1

    partial_mems = run_instructions(str(monad), instructions, partial_mems)

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
    partial_mems = update_partial_mems(prev_monad, monad, partial_mems)

    last_dt = update_times_dict(last_dt, times, "update_partials")

    # if i == 10000:
    if monad < 99999999990000:
        print(f"\nTotal runs: {i}")
        print("\nTimes:")
        for name in times:
            print(f"- {name}: {str(times[name])}")
        print(f"\nLowest monad tried: {monad}")
        print(f"\nTotal time: {dt.now() - start}")
        exit()

print(f"Largest valid monad: {monad}")
