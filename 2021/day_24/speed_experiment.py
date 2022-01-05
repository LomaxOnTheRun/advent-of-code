from time import time

# TIMING UTILS #

LOG_TIME = {}
LOG_COUNTS = {}


def timeit(method):
    def timed(*args, **kw):
        ts = time()
        result = method(*args, **kw)
        te = time()
        name = method.__name__
        if name not in LOG_TIME:
            LOG_TIME[name] = 0
        LOG_TIME[name] += (te - ts) * 1000
        if name not in LOG_COUNTS:
            LOG_COUNTS[name] = 0
        LOG_COUNTS[name] += 1
        return result

    return timed


def print_logged_times():
    """
    Show how long each function has taken to run.
    """
    sorted_times = reversed(sorted(LOG_TIME.items(), key=lambda kv: kv[1]))
    print("\nFunction run times (ms):\n")
    for name, time in sorted_times:
        time = int(time)
        count = LOG_COUNTS[name]
        time_space, count_space = 8 - len(str(time)), 10 - len(str(count))
        per_call = f"{(time / count):.5f}"
        print(
            f"{time} ms{' ' * time_space}x {count}{' ' * count_space}{per_call}    {name}"
        )


################


data = """mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 8
mul y x
add z y"""


@timeit
def inp(a, b, mem):
    mem[a] = b
    return mem


@timeit
def add(a, b, mem):
    mem[a] += b
    return mem


@timeit
def mul(a, b, mem):
    mem[a] *= b
    return mem


@timeit
def div(a, b, mem):
    mem[a] = int(mem[a] / b)
    return mem


@timeit
def mod(a, b, mem):
    mem[a] %= b
    return mem


@timeit
def eql(a, b, mem):
    mem[a] = int(mem[a] == b)
    return mem


@timeit
def get_instructions_1(data):
    """Split instructions into 14 groups (one group per input)."""
    instructions = []
    for line in data.split("\n"):
        instructions.append(line.strip().split(" "))
    return instructions


@timeit
def run_ops_1(instructions, mem):
    for op_name, a, b in instructions:
        op = OPERATIONS[op_name]
        if b in "wxyz":
            b = mem[b]
        mem = op(a, int(b), mem)
    return mem


@timeit
def get_instructions_2(data):
    """Split instructions into 14 groups (one group per input)."""
    instructions = []
    for line in data.split("\n"):
        op_name, a, b = line.strip().split(" ")
        op = OPERATIONS[op_name]
        instructions.append((op, a, b))
    return instructions


@timeit
def run_ops_2(instructions, mem):
    for op, a, b in instructions:
        if b in "wxyz":
            b = mem[b]
        mem = op(a, int(b), mem)
    return mem


@timeit
def run_ops_3(mem):
    mem[X] *= 0
    mem[X] += mem[Z]
    mem[X] %= 26
    mem[Z] /= 1
    mem[X] += 11
    mem[X] = int(mem[X] == mem[W])
    mem[X] = int(mem[X] == 0)
    mem[Y] *= 0
    mem[Y] += 25
    mem[Y] *= mem[X]
    mem[Y] += 1
    mem[Z] *= mem[Y]
    mem[Y] *= 0
    mem[Y] += mem[W]
    mem[Y] += 8
    mem[Y] *= mem[X]
    mem[Z] += mem[Y]
    return mem


W, X, Y, Z = "wxyz"

ops_str_4 = """@timeit
def run_ops_4(mem):
    mem[X] *= 0
    mem[X] += mem[Z]
    mem[X] %= 26
    mem[Z] /= 1
    mem[X] += 11
    mem[X] = int(mem[X] == mem[W])
    mem[X] = int(mem[X] == 0)
    mem[Y] *= 0
    mem[Y] += 25
    mem[Y] *= mem[X]
    mem[Y] += 1
    mem[Z] *= mem[Y]
    mem[Y] *= 0
    mem[Y] += mem[W]
    mem[Y] += 8
    mem[Y] *= mem[X]
    mem[Z] += mem[Y]
    return mem
"""


ops_str_5 = """@timeit
def run_ops_5(mem):
    mem[X] = (mem[Z] % 26) + 11
    mem[X] = int(mem[X] == mem[W])
    mem[X] = int(mem[X] == 0)
    mem[Y] = (25 * mem[X]) + 1
    mem[Z] *= mem[Y]
    mem[Y] = (mem[W] + 8) * mem[X]
    mem[Z] += mem[Y]
    return mem
"""


ops_str_6 = """@timeit
def run_ops_6(w, x, y, z):
    x *= 0
    x += z
    x %= 26
    z /= 1
    x += 11
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 8
    y *= x
    z += y
    return w, x, y, z
"""

ops_str_7 = """@timeit
def run_ops_7(w, x, y, z):
    x = (z % 26) + 11
    x = int(x == w)
    x = int(x == 0)
    y = (25 * x) + 1
    z *= y
    y = (w + 8) * x
    z += y
    return w, x, y, z
"""

W, X, Y, Z = "wxyz"
OPERATIONS = {"inp": inp, "add": add, "mul": mul, "div": div, "mod": mod, "eql": eql}

instructions_1 = get_instructions_1(data)
instructions_2 = get_instructions_2(data)
exec(ops_str_4, globals())
exec(ops_str_5, globals())
exec(ops_str_6, globals())
exec(ops_str_7, globals())

runs = 20
for w in range(runs):
    for x in range(runs):
        for y in range(runs):
            for z in range(runs):
                mem = {W: w, X: x, Y: y, Z: z}
                # print(mem)
                # mem_1 = run_ops_1(instructions_1, mem.copy())
                # mem_2 = run_ops_2(instructions_2, mem.copy())
                # mem_3 = run_ops_3(mem.copy())
                mem_4 = run_ops_4(mem.copy())
                mem_5 = run_ops_5(mem.copy())
                w, x, y, z = mem[W], mem[X], mem[Y], mem[Z]
                mem_6 = run_ops_6(w, x, y, z)
                mem_7 = run_ops_7(w, x, y, z)
                # assert mem_1 == mem_2 == mem_3 == mem_4 == mem_5
                # ), f"{mem_1} != {mem_2} != {mem_3} != {mem_4}"

print_logged_times()
