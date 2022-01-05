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
        # mem = run_instructions_group(instructions[0], int(monad_digit), mem, {}, 0)
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
        mem = {W: 0, X: 0, Y: 0, Z: 0}
        # mem = run_instructions_group(instructions[0], int(monad_digit), mem, {}, 0)
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
        # mem = [{W: 0, X: 0, Y: 0, Z: 0}]
        mem = {W: 0, X: 0, Y: 0, Z: 0}
        # mems = run_instructions(monad, instructions, mem, {})
        # mem = run_instructions(monad, instructions, mem, {})
        mem = run_instructions(monad, instructions, mem)
        assert (
            # mems[-1][Z] == output_val
            mem[Z]
            == output_val
        ), f"{monad}, {output_val} => {mem[Z]} != {output_val}"


# def example_4():
#     example_data = """inp x
#         add x 1
#         inp y
#         div y x
#         inp z
#         mul z y"""
#     monad = "148"
#     in_out = [
#         ([{W: 0, X: 0, Y: 0, Z: 0}], 16),
#         ([{W: 0, X: 0, Y: 0, Z: 0}, {W: 0, X: 4, Y: 0, Z: 0}], 8),
#         ([{W: 0, X: 0, Y: 0, Z: 0}, {W: 0, X: 1, Y: 0, Z: 0}], 32),
#         (
#             [
#                 {W: 0, X: 0, Y: 0, Z: 0},
#                 {W: 0, X: 0, Y: 0, Z: 0},
#                 {W: 0, X: 0, Y: 0, Z: 0},
#             ],
#             0,
#         ),
#         (
#             [
#                 {W: 0, X: 0, Y: 0, Z: 0},
#                 {W: 0, X: 0, Y: 0, Z: 0},
#                 {W: 0, X: 0, Y: 1, Z: 0},
#             ],
#             8,
#         ),
#         (
#             [
#                 {W: 0, X: 0, Y: 0, Z: 0},
#                 {W: 0, X: 0, Y: 0, Z: 0},
#                 {W: 0, X: 0, Y: 2, Z: 0},
#             ],
#             16,
#         ),
#     ]
#     instructions = get_instructions(example_data)
#     for mems, z in in_out:
#         mems = run_instructions(monad, instructions, mems, {})
#         assert mems[-1][Z] == z


# def example_5():
#     partial_mems = [1, 2, 3, 4]
#     in_out = [
#         ("999", "998", [1, 2, 3]),
#         ("999", "997", [1, 2, 3]),
#         ("999", "989", [1, 2]),
#         ("999", "899", [1]),  # The base one will always stay
#     ]
#     for old_monad, new_monad, expected_partials in in_out:
#         new_partials = update_partial_mems(old_monad, new_monad, partial_mems)
#         assert (
#             new_partials == expected_partials
#         ), f"{old_monad}, {new_monad} => {new_partials} != {expected_partials}"


class EarlyStop(Exception):
    def __init__(self, inp_index):
        self.inp_index = inp_index


def is_var(var_or_number):
    return var_or_number in "wxyz"


def inp(a, b, mem):
    mem[a] = b
    return mem


def add(a, b, mem):
    mem[a] += b
    return mem


def mul(a, b, mem):
    mem[a] *= b
    return mem


def div(a, b, mem):
    mem[a] = int(mem[a] / b)
    return mem


def mod(a, b, mem):
    mem[a] %= b
    return mem


def eql(a, b, mem):
    mem[a] = int(mem[a] == b)
    return mem


def is_valid(mem):
    return mem["z"] == 0


def get_instructions(data):
    """Split instructions into 14 groups (one group per input)."""
    instructions = []
    for line in data.split("\n"):
        op_name, ab = line.strip().split(" ", 1)
        op = OPERATIONS[op_name]
        if op == inp:
            instructions.append([])
            ab += " INP"
        a, b = ab.split(" ")
        instructions[-1].append((op, a, b))
    return instructions


def run_instructions_group(instructions_group, input_val, mem):
    # First instruction is always input
    mem = mem.copy()
    _, a, _ = instructions_group[0]
    mem = inp(a, input_val, mem)

    for op, a, b in instructions_group[1:]:
        if is_var(b):
            b = mem[b]
        mem = op(a, int(b), mem)

    return mem


def run_instructions(monad, instructions, mem):
    for inp_index, instructions_group in enumerate(instructions):
        input_val = int(monad[inp_index])
        mem = run_instructions_group(instructions_group, input_val, mem)

    return mem


def update_times_dict(last_dt, times, name):
    new_dt = dt.now()
    diff = new_dt - last_dt
    times[name] = diff if name not in times else times[name] + diff
    return dt.now()


def print_times(times):
    tt = sorted([(delta, name) for name, delta in times.items()], reverse=True)
    print("\nTimes:")
    for delta, name in tt:
        print(f"- {str(delta)}: {name}")


data = aocd.get_data(year=2021, day=24)

W, X, Y, Z = "wxyz"

OPERATIONS = {"inp": inp, "add": add, "mul": mul, "div": div, "mod": mod, "eql": eql}

# Samity checks
example_1()
example_2()
example_3()
# example_4()
# example_5()

# Start the counter
keep_times = False
keep_total_time = True
# times = {}
# if keep_times:
#     last_dt = dt.now()
if keep_total_time or keep_times:
    start = dt.now()

monad = "99999999999999"
# Makes updating the monad slightly easier
nines = {x: "9" * (14 - x) for x in range(1, 14)}

# Keep track of states for sections of the monad {shared_monad: mem}
monad_cache = {}
shared_monad = ""

instructions = get_instructions(data)

# if keep_times:
#     last_dt = update_times_dict(last_dt, times, "setup")

# TODO: LOOK INTO AST BREAKDOWN OF WHAT CODE IS RUNNING

step = 0
while True:
    step += 1

    # TODO: THIS IS BROKEN:
    # -->> ONLY THE SHARED MONAD GETS CHECKED, I DON'T RUN THE REST OF THE NUMBER
    mem = monad_cache.get(shared_monad)
    if not mem:
        mem = {W: 0, X: 0, Y: 0, Z: 0}
        mem = run_instructions(monad, instructions, mem)
        monad_cache[shared_monad] = mem.copy()

        # TODO: Is there a way / benefit to getting rid of the unrequired mems here?

        # TODO: Reintroduce some sort of partials computing?
        # - CHECK TIMES TO SEE IF THIS IS EVEN A GOOD IDEA

    # if shared_monad in monad_cache:
    #     mem = monad_cache[shared_monad]
    #     # if keep_times:
    #     #     last_dt = update_times_dict(last_dt, times, "get_from_monad_cache")
    # else:
    #     mem = {W: 0, X: 0, Y: 0, Z: 0}
    #     mem = run_instructions(monad, instructions, mem)
    #     # if keep_times:
    #     #     last_dt = update_times_dict(last_dt, times, "run_instructions")

    #     monad_cache[shared_monad] = mem.copy()
    #     # if keep_times:
    #     #     last_dt = update_times_dict(last_dt, times, "save_to_monad_cache")

    if is_valid(mem):
        break

    # if keep_times:
    #     last_dt = update_times_dict(last_dt, times, "valid_check")

    while monad[-1] == "1":
        monad = monad[:-1]
    monad = str(int(monad) - 1)
    if len(monad) < 14:
        monad += nines[len(monad)]

    # if keep_times:
    #     last_dt = update_times_dict(last_dt, times, "update_monad")

    while shared_monad not in monad:
        shared_monad = shared_monad[:-1]

    # if keep_times:
    #     last_dt = update_times_dict(last_dt, times, "update_shared_monad")

    # if step == 10000000:  # ~10s (9999997...)
    # if step == 100000000:  # ~2mins (999997...)
    # if step == 1000000000:  # ~16mins (99997...)
    # if step == 10000000000:  # ~3h (9997...)
    if step == 100000000000:  # ~27h 20m (996...)
        # if step == 1000000000000:  # ~20000mins ~300h (97... in theory)
        # if step == 10000000000000:  # ~200000mins ~3000h (7... in theory)
        print(f"\nTotal runs: {step}")
        # if keep_times:
        #     print_times(times)
        if keep_total_time or keep_times:
            print(f"\nTotal time: {dt.now() - start}")
        print(f"\nLowest monad tried: {monad}")
        exit()

print(f"Largest valid monad: {monad}")
