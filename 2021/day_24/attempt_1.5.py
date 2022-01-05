import aocd
from datetime import datetime as dt

data = """inp x
mul x -1"""

data = """inp z
inp x
mul z 3
eql z x"""

data = """inp w
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

data = aocd.get_data(year=2021, day=24)

W, X, Y, Z = VARS = "wxyz"


class EarlyStop(Exception):
    def __init__(self, inp_index):
        self.inp_index = inp_index


def is_var(var_or_number):
    return var_or_number in VARS


def is_number(var_or_number):
    return isinstance(var_or_number, int)


# def inp(a, value, mem):
#     mem[a] = value
#     return mem


# def add(a, b, mem):
#     val = mem[b] if is_var(b) else int(b)
#     mem[a] += val
#     return mem


# def mul(a, b, mem):
#     val = mem[b] if is_var(b) else int(b)
#     mem[a] *= val
#     return mem


# def div(a, b, mem):
#     val = mem[b] if is_var(b) else int(b)
#     mem[a] = int(mem[a] / val)
#     return mem


# def mod(a, b, mem):
#     val = mem[b] if is_var(b) else int(b)
#     mem[a] %= val
#     return mem


# def eql(a, b, mem):
#     val = mem[b] if is_var(b) else int(b)
#     mem[a] = int(mem[a] == val)
#     return mem


# def is_valid(mem):
#     return mem[Z] == 0


def get_val(name, w, x, y, z):
    if name == W:
        return w
    if name == X:
        return x
    if name == Y:
        return y
    if name == Z:
        return z


def inp(a, value, w, x, y, z):
    if a == W:
        w = value
    elif a == X:
        x = value
    elif a == Y:
        y = value
    elif a == Z:
        z = value
    return w, x, y, z


def add(a, a_val, b_val, w, x, y, z):
    return inp(a, a_val + b_val, w, x, y, z)


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
    return mem[Z] == 0


def copy_mem(mem):
    return {k: v for k, v in mem.items()}


def run_instructions(monad, partial_mems, debug=False):
    # Current working memory
    w, x, y, z = partial_mems[-1]

    # Keep track of which input is next
    inp_index = 0

    skipping = True
    for line in data.split("\n"):

        if debug:
            print("len(partial_mems)", len(partial_mems))

        if debug:
            print(line)

        instruction, ab = line.split(" ", 1)

        # part=2, inp=0, inp -> skip (inp+=1)
        # part=2, inp=1, not inp -> skip
        # part=2, inp=1, inp -> don't skip

        # Skip instructions while we have valid mem checkpoints

        if skipping and instruction == "inp":
            if len(partial_mems) == inp_index + 1:
                skipping = False
            else:
                inp_index += 1

        if skipping:
            continue

        # print(line)

        if instruction == "inp":
            partial_mems.append(copy_mem(mem))
            mem = inp(ab, int(monad[inp_index]), mem)
            inp_index += 1
        else:
            a, b = ab.split(" ")
            op = operations[instruction]
            a_val = get_val(a, w, x, y, z)
            b_val = get_val(b, w, x, y, z) if is_var(b) else int(b)
            mem = op(a, a_val, b_val, w, x, y, z)

    return is_valid(mem), partial_mems


def update_times_dict(last_dt, times, name):
    new_dt = dt.now()
    diff = new_dt - last_dt
    # print(type(diff))
    times[name] = diff if name not in times else times[name] + diff
    return new_dt


operations = {"add": add, "mul": mul, "div": div, "mod": mod, "eql": eql}

monad = 99999999999999

# Keep track of state before every new input [(w, x, y, z), ...]
partial_mems = [(0, 0, 0, 0)]

times = {}
i = 0
while True:
    i += 1
    last_dt = dt.now()

    valid, partial_mems = run_instructions(str(monad), partial_mems, debug=False)

    last_dt = update_times_dict(last_dt, times, "run_instructions")

    # print(monad, valid, len(partial_mems))

    # if monad % 10000 == 1111:
    #     print(monad, valid)

    if valid:
        break

    last_dt = update_times_dict(last_dt, times, "time_checks")

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

    # print(prev_monad - monad)
    # TODO: Maybe subtract each digit and see how big remaining number is?
    # partial_mems = partial_mems[: 15 - len(str(prev_monad - monad))]

    print(prev_monad, monad, len(partial_mems))

    last_dt = update_times_dict(last_dt, times, "update_partials")

    if i == 10:
        for name in times:
            print(f"{name}: {str(times[name])}")
        exit()

#     if valid:
#         break

print(monad, valid)
