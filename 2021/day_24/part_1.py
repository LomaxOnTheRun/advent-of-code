import aocd, re


# TIMING UTILS #


from time import time

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
    total_time = int(sum([time for _, time in LOG_TIME.items()]))
    print(f"TOTAL: {total_time} ms\n")
    for name, time in sorted_times:
        time = int(time)
        count = LOG_COUNTS[name]
        time_space, count_space = 8 - len(str(time)), 10 - len(str(count))
        per_call = f"{(time / count):.5f}"
        print(
            f"{time} ms{' ' * time_space}x {count}{' ' * count_space}{per_call}    {name}"
        )


def print_total_time(total_run_time):
    total_search_seconds = (total_run_time * 1e13) / LOG_COUNTS["reduce_monad"]
    print(f"\nTotal search time:")
    print(f"  {int(total_search_seconds)} secs")
    total_mins = total_search_seconds / 60
    print(f"  {int(total_mins)} mins")
    total_hours = total_mins / 60
    print(f"  {int(total_hours)} hours")
    total_days = total_hours / 24
    print(f"  {int(total_days)} days")


# EXAMPLES #

EXAMPLE_DATA = """inp w
add w 1
inp x
add x 2
mul w x
inp y
add y 3
inp z
add z 4
mul y z
div y w
"""


def function_creation_example():
    test_function = create_function(EXAMPLE_DATA, "test_function")
    for monad_int in range(10000):
        monad = f"{monad_int:04}"
        mem = test_function(monad)

        w, x, y, z = [int(c) for c in monad]
        w += 1
        x += 2
        w *= x
        y += 3
        z += 4
        y *= z
        y = int(y / w)

        assert mem == (w, x, y, z), f"{monad} => {mem} != {(w, x, y, z)}"


def input_functions_creation_example():
    input_fns = create_input_functions(EXAMPLE_DATA)
    assert len(input_fns) == 4, f"input_fns: {input_fns}"
    out = [fn("1234", 0, 0, 0, 0) for fn in input_fns]
    assert out[0] == (1, 0, 0, 0), f"{out[0]} != {(1, 0, 0, 0)}"
    assert out[1] == (0, 2, 0, 0), f"{out[1]} != {(0, 2, 0, 0)}"
    assert out[2] == (0, 0, 3, 0), f"{out[2]} != {(0, 0, 3, 0)}"
    assert out[3] == (0, 0, 0, 4), f"{out[3]} != {(0, 0, 0, 4)}"


def maths_functions_creation_example():
    maths_fns = create_maths_functions(EXAMPLE_DATA)
    assert len(maths_fns) == 4, f"maths_fns: {maths_fns}"
    out = [fn("0000", 1, 2, 3, 4) for fn in maths_fns]
    assert out[0] == (2, 2, 3, 4), f"{out[0]} != {(2, 2, 3, 4)}"
    assert out[1] == (4, 4, 3, 4), f"{out[1]} != {(4, 4, 3, 4)}"
    assert out[2] == (1, 2, 6, 4), f"{out[2]} != {(1, 2, 6, 4)}"
    assert out[3] == (1, 2, 24, 8), f"{out[3]} != {(1, 2, 24, 8)}"


def growing_functions_creation_example():
    growing_fns = create_growing_functions(EXAMPLE_DATA)
    assert len(growing_fns) == 4, f"growing_fns: {growing_fns}"
    input_vars = ("1234", 0, 0, 0, 0)
    full_fn = create_function(EXAMPLE_DATA, "full_fn")
    assert growing_fns[-1](*input_vars) == full_fn(*input_vars)


def shrinking_functions_creation_example():
    shrinking_fns = create_shrinking_functions(EXAMPLE_DATA)
    assert len(shrinking_fns) == 4, f"shrinking_fns: {shrinking_fns}"
    input_vars = ("1234", 0, 0, 0, 0)
    full_fn = create_function(EXAMPLE_DATA, "full_fn")
    assert shrinking_fns[0](*input_vars)[3] == full_fn(*input_vars)[3]
    input_fns = create_input_functions(EXAMPLE_DATA)
    maths_fns = create_maths_functions(EXAMPLE_DATA)
    ex_out_1 = (8, 4, 6, 8)
    ex_out_2 = (0, 0, 0, 8)  # Shrinking functions only cares about z var
    monad_in = [
        (0, "1234", (0, 0, 0, 0)),
        (1, "1234", (2, 0, 0, 0)),
        (2, "1234", (8, 4, 0, 0)),
        (3, "1234", (8, 4, 6, 0)),
    ]
    for index, monad, ex_in in monad_in:
        mem_1 = apply_functions(monad, input_fns, maths_fns, ex_in, index)
        mem_2 = apply_shrinking_function(monad, input_fns, shrinking_fns, ex_in, index)
        assert mem_1 == ex_out_1, f"{mem_1} != {ex_out_1}"
        assert mem_2 == ex_out_2, f"{mem_2} != {ex_out_2}"


def apply_functions_example():
    input_fns = create_input_functions(EXAMPLE_DATA)
    maths_fns = create_maths_functions(EXAMPLE_DATA)
    in_out = [
        ("1", (2, 0, 0, 0)),
        ("12", (8, 4, 0, 0)),
        ("123", (8, 4, 6, 0)),
        ("1234", (8, 4, 6, 8)),
    ]
    for ex_in, ex_out in in_out:
        mem = apply_functions(ex_in, input_fns, maths_fns, (0, 0, 0, 0))
        assert mem == ex_out, f"{ex_in} => {mem} != {ex_out}"


def reduce_monad_examples():
    in_out = [("999", "998"), ("991", "989"), ("911", "899")]
    for ex_in, ex_out in in_out:
        reduced_monad = reduce_monad(ex_in, 3)
        assert reduced_monad == ex_out, f"{ex_in} => {reduced_monad} != {ex_out}"


def shared_monad_examples():
    old_new_shared = [("999", "998", "99"), ("999", "989", "9"), ("999", "899", "")]
    for old, new, ex_shared in old_new_shared:
        shared_monad = get_shared_monad(old, new)
        assert shared_monad == ex_shared


#############


def create_unique_var_names(code):
    d = {"w": 0, "x": 0, "y": 0, "z": 0}
    lines = [line for line in code.split("\n")]
    for index, line in enumerate(lines):
        # Replace signature
        if index == 0:
            for var in "wxyz":
                lines[0] = lines[0].replace(f" {var}", f" {var}0")
            continue

        # Create unique var names
        for var in "wxyz":
            if var in line:
                line = line.replace(f" {var} = ", f" {var}{d[var] + 1} = ")
                line = re.sub(rf"{var}([^\d]+|$)", rf"{var}{d[var]}\1", line)
                if f" {var}{d[var] + 1} = " in line:
                    d[var] += 1
        lines[index] = line
    return "\n".join(lines), d


def combine_vars(code, d):
    # print(code)
    for var in "wxyz":
        while d[var] > 0:
            # if var == "y" and d[var] == 8:
            #     print(len(re.findall(rf"{var}{d[var]}(\D|$)", code)))
            #     print(v)
            if len(re.findall(rf"{var}{d[var]}(\D|$)", code)) == 2:
                # Get original variable definition
                v = re.search(rf"    {var}{d[var]} = (.*)", code)[1]
                # if var == "y" and d[var] == 8:
                #     print("BEN TEST 1", v)
                # Remove original line
                code = re.sub(rf"\n.* {var}{d[var]} = .*", "", code)
                # if var == "y" and d[var] == 8:
                #     print("BEN TEST 2", code)
                #     m = re.search(rf"{var}{d[var]}( |,|\)|$)", code)
                #     print(m)
                # Place original definition into only other calling place
                # code = re.sub(rf"{var}{d[var]}( |,|\)|$)", rf"({v})\1", code)
                if re.search(rf"{var}{d[var]}( |,|\)|$)", code):
                    code = re.sub(rf"{var}{d[var]}( |,|\)|$)", rf"({v})\1", code)
                else:
                    code = re.sub(rf"{var}{d[var]}", rf"({v})", code)
                # if var == "y" and d[var] == 8:
                #     print("BEN TEST 3", code)
                #     exit()
            d[var] -= 1
    return code


def reduce_code(code):
    # (wxyz * 0) => 0
    code = re.sub(r"\([^\(]+ \* 0\)", "0", code)
    # wxyz * 0 => 0
    code = re.sub(r".\d+ \* 0", "0", code)
    # (wxyz + 0) => wxyz
    code = re.sub(r"\((.\d+) \+ 0\)", r"\1", code)
    # (0 + wxyz) => wxyz
    code = re.sub(r"\(0 \+ (.\d+)\)", r"\1", code)
    # int(wxyz / 1) => wxyz
    code = re.sub(r"int\((.\d+) / 1\)", r"\1", code)
    # int(wxyz) => wxyz
    code = re.sub(r"int\((.\d+)\)", r"\1", code)
    # (wxyz) => wxyz
    code = re.sub(r"\((.\d+)\)", r"\1", code)
    return code


def simplify_code(code, only_return_z=False):
    code, d = create_unique_var_names(code)
    if only_return_z:
        #     print("unique:", code, "\n")
        code = re.sub(r"return .*, (.+)$", r"return 0, 0, 0, \1", code)
    #     print("unique:", code, "\n")
    code = combine_vars(code, d)
    # if only_return_z:
    #     print("combine:", code, "\n")
    # print("combine:", code, "\n")
    code = reduce_code(code)
    # if only_return_z:
    #     print("reduce:", code, "\n")
    # print("reduce:", code, "\n")
    return code


def create_function(data, fn_name, inp_index=0, show_code=False):
    # function_str = f"@timeit\ndef {fn_name}(monad, w=0, x=0, y=0, z=0):\n"
    function_str = f"def {fn_name}(monad, w=0, x=0, y=0, z=0):\n"

    OP = {
        "add": "{0} + {1}",
        "mul": "{0} * {1}",
        "div": "int({0} / {1})",
        "mod": "{0} % {1}",
        # "eql": "int({0} == {1})",
        "eql": "{0} == {1}",
    }

    for line in data.strip().split("\n"):
        name, ab = line.strip().split(" ", 1)
        if name == "inp":
            function_str += f"    {ab} = int(monad[{inp_index}])\n"
            inp_index += 1
        else:
            a, b = ab.split(" ")
            function_str += f"    {a} = " + OP[name].format(a, b) + "\n"
    function_str += "    return w, x, y, z"
    # function_str += "    return int(w), int(x), int(y), int(z)"

    # if fn_name == "get_mem":
    # if fn_name[:9] == "shrinking":
    #     print(function_str, "\n")
    only_return_z = fn_name[:9] == "shrinking"
    function_str = simplify_code(function_str, only_return_z)
    # if fn_name == "get_mem":
    if show_code:
        print(function_str, "\n")

    exec(function_str, globals())

    return globals()[fn_name]


def create_input_functions(data):
    inp_index = 0
    fn_name = "input_0"
    input_functions = []
    for line in data.strip().split("\n"):
        if line.strip()[:3] == "inp":
            input_functions.append(create_function(line, fn_name, inp_index))
            inp_index += 1
            fn_name = f"input_{inp_index}"
    return input_functions


def create_maths_functions(data):
    # Split data into non-input sections
    maths_data = []
    current_data = ""
    for line in data.strip().split("\n"):
        if line.strip()[:3] != "inp":
            current_data += f"\n{line}"
        elif current_data:
            maths_data.append(current_data.strip())
            current_data = ""
    if current_data:
        maths_data.append(current_data.strip())
    # Create functions for each sections
    maths_functions = []
    for index, maths_data_section in enumerate(maths_data):
        fn_name = f"maths_{index}"
        maths_functions.append(create_function(maths_data_section, fn_name))
    return maths_functions


def create_growing_functions(data):
    # Create functions that start as first calc, and grow by one input section
    growing_data = ["" for _ in range(data.count("inp"))]
    inp_index = -1
    for line in data.strip().split("\n"):
        if line.strip()[:3] == "inp":
            inp_index += 1
        for index, fn_data in enumerate(growing_data[inp_index:]):
            growing_data[inp_index + index] = fn_data + f"\n{line}"
    # Create functions for each sections
    growing_functions = []
    for index, fn_data in enumerate(growing_data):
        fn_name = f"growing_{index}"
        growing_functions.append(create_function(fn_data, fn_name))
    return growing_functions


def create_shrinking_functions(data):
    # Create functions that start as full calc, and shorten by one input section
    shrinking_data = []
    for line in data.strip().split("\n"):
        if line.strip()[:3] == "inp":
            shrinking_data.append("")
        for index, fn_data in enumerate(shrinking_data):
            shrinking_data[index] = fn_data + f"\n{line}"
    # Create functions for each sections
    shrinking_functions = []
    for index, fn_data in enumerate(shrinking_data):
        fn_name = f"shrinking_{index}"
        shrinking_functions.append(create_function(fn_data, fn_name, inp_index=index))
    return shrinking_functions


def apply_functions(monad, input_fns, math_fns, mem=(0, 0, 0, 0), start_index=0):
    for index in range(start_index, len(monad)):
        mem = input_fns[index](monad, *mem)
        mem = math_fns[index](monad, *mem)
    return mem


# @timeit
# def apply_functions_grow(monad, input_fns, math_fns, mem=(0, 0, 0, 0), start_index=0):
#     return apply_functions(monad, input_fns, math_fns, mem, start_index)


# @timeit
# def apply_functions_shrink(monad, input_fns, math_fns, mem=(0, 0, 0, 0), start_index=0):
#     return apply_functions(monad, input_fns, math_fns, mem, start_index)


# @timeit
def apply_growing_function(shared_monad, growing_fns, mem=(0, 0, 0, 0)):
    return growing_fns[len(shared_monad) - 1](shared_monad, *mem)


# @timeit
def apply_shrinking_function_old(monad, shrinking_fns, shared_mem, start_index=0):
    return shrinking_fns[start_index](monad, *shared_mem)


# @timeit
def apply_shrinking_function(
    monad, input_fns, shrinking_fns, shared_mem, start_index, shrinking_cache={}
):
    mem = input_fns[start_index](monad, *shared_mem)
    cache_key = (start_index, mem)
    if cache_key in shrinking_cache:
        return shrinking_cache[cache_key]

    mem = shrinking_fns[start_index](monad, *shared_mem)
    shrinking_cache[cache_key] = mem

    return mem


# @timeit
def reduce_monad(monad, monad_len=14):
    while monad[-1] == "1":
        monad = monad[:-1]
    monad = str(int(monad) - 1)
    if len(monad) < monad_len:
        monad += NINES[monad_len - len(monad)]
    return monad


# @timeit
def get_shared_monad(old_monad, new_monad):
    shared_monad = new_monad[:-1]
    len_shared_monad = len(shared_monad)
    while old_monad[:len_shared_monad] != shared_monad:
        shared_monad = shared_monad[:-1]
        len_shared_monad -= 1
    return shared_monad


# @timeit
def get_or_save_shared_monad_mem(shared_monad, shared_cache, input_fns, maths_fns):
    max_index = len(shared_monad)
    partial = shared_monad[:max_index]
    # Roll back to smallest known cache
    while partial not in shared_cache:
        max_index -= 1
        partial = shared_monad[:max_index]

    # Now recreate missing caches
    while max_index < len(shared_monad):
        max_index += 1
        partial = shared_monad[:max_index]
        last_partial = partial[:-1]
        mem = shared_cache[last_partial]
        mem = input_fns[len(last_partial)](partial, *mem)
        mem = maths_fns[len(last_partial)](partial, *mem)
        shared_cache[partial] = mem

    return shared_cache[shared_monad]


NINES = {x: "9" * x for x in range(1, 14)}


# function_creation_example()
# input_functions_creation_example()
# maths_functions_creation_example()
# shrinking_functions_creation_example()
# growing_functions_creation_example()
# apply_functions_example()
# reduce_monad_examples()
# shared_monad_examples()

# Setup
data = aocd.get_data(year=2021, day=24)
# get_mem = create_function(data, "get_mem", show_code=True)
input_fns = create_input_functions(data)
maths_fns = create_maths_functions(data)
growing_fns = create_growing_functions(data)
shrinking_fns = create_shrinking_functions(data)
monad = "99999999999999"


# def get_mem(monad):
#     monad = [int(c) for c in monad]
#     z4 = monad[0] + 8
#     x13 = ((z4 % 26) + 12) != monad[1]
#     z7 = (z4 * ((25 * x13) + 1)) + ((monad[1] + 8) * x13)
#     x19 = ((z7 % 26) + 10) != monad[2]
#     z10 = (z7 * ((25 * x19) + 1)) + ((monad[2] + 12) * x19)
#     x25 = ((z10 % 26) - 8) != monad[3]
#     z13 = ((int(z10 / 26)) * ((25 * x25) + 1)) + ((monad[3] + 10) * x25)
#     x31 = ((z13 % 26) + 15) != monad[4]
#     z16 = (z13 * ((25 * x31) + 1)) + ((monad[4] + 2) * x31)
#     x37 = ((z16 % 26) + 15) != monad[5]
#     z19 = (z16 * ((25 * x37) + 1)) + ((monad[5] + 8) * x37)
#     x43 = ((z19 % 26) - 11) != monad[6]
#     z22 = ((int(z19 / 26)) * ((25 * x43) + 1)) + ((monad[6] + 4) * x43)
#     x49 = ((z22 % 26) + 10) != monad[7]
#     z25 = (z22 * ((25 * x49) + 1)) + ((monad[7] + 9) * x49)
#     x55 = ((z25 % 26) - 3) != monad[8]
#     z28 = ((int(z25 / 26)) * ((25 * x55) + 1)) + ((monad[8] + 10) * x55)
#     x61 = ((z28 % 26) + 15) != monad[9]
#     z31 = (z28 * ((25 * x61) + 1)) + ((monad[9] + 3) * x61)
#     x67 = ((z31 % 26) - 3) != monad[10]
#     z34 = ((int(z31 / 26)) * ((25 * x67) + 1)) + ((monad[10] + 7) * x67)
#     x73 = ((z34 % 26) - 1) != monad[11]
#     z37 = ((int(z34 / 26)) * ((25 * x73) + 1)) + ((monad[11] + 7) * x73)
#     x79 = ((z37 % 26) - 10) != monad[12]
#     z40 = ((int(z37 / 26)) * ((25 * x79) + 1)) + ((monad[12] + 2) * x79)
#     x85 = ((z40 % 26) - 16) != monad[13]
#     return 0, 0, 0, (((int(z40 / 26)) * ((25 * x85) + 1)) + ((monad[13] + 2) * x85))


def get_mem(monad):
    monad = [int(c) for c in monad]
    z4 = monad[0] + 8
    x13 = ((z4 % 26) + 12) != monad[1]
    if x13 == 1:
        return 0, 0, 0, 1
    z7 = (z4 * ((25 * x13) + 1)) + ((monad[1] + 8) * x13)
    x19 = ((z7 % 26) + 10) != monad[2]
    if x19 == 1:
        return 1, 0, 0, 1
    z10 = (z7 * ((25 * x19) + 1)) + ((monad[2] + 12) * x19)
    x25 = ((z10 % 26) - 8) != monad[3]
    if x25 == 1:
        return 2, 0, 0, 1
    z13 = ((int(z10 / 26)) * ((25 * x25) + 1)) + ((monad[3] + 10) * x25)
    x31 = ((z13 % 26) + 15) != monad[4]
    if x31 == 1:
        return 3, 0, 0, 1
    z16 = (z13 * ((25 * x31) + 1)) + ((monad[4] + 2) * x31)
    x37 = ((z16 % 26) + 15) != monad[5]
    if x37 == 1:
        return 4, 0, 0, 1
    z19 = (z16 * ((25 * x37) + 1)) + ((monad[5] + 8) * x37)
    x43 = ((z19 % 26) - 11) != monad[6]
    if x43 == 1:
        return 5, 0, 0, 1
    z22 = ((int(z19 / 26)) * ((25 * x43) + 1)) + ((monad[6] + 4) * x43)
    x49 = ((z22 % 26) + 10) != monad[7]
    if x49 == 1:
        return 6, 0, 0, 1
    z25 = (z22 * ((25 * x49) + 1)) + ((monad[7] + 9) * x49)
    x55 = ((z25 % 26) - 3) != monad[8]
    if x55 == 1:
        return 7, 0, 0, 1
    z28 = ((int(z25 / 26)) * ((25 * x55) + 1)) + ((monad[8] + 10) * x55)
    x61 = ((z28 % 26) + 15) != monad[9]
    if x61 == 1:
        return 8, 0, 0, 1
    z31 = (z28 * ((25 * x61) + 1)) + ((monad[9] + 3) * x61)
    x67 = ((z31 % 26) - 3) != monad[10]
    if x67 == 1:
        return 9, 0, 0, 1
    z34 = ((int(z31 / 26)) * ((25 * x67) + 1)) + ((monad[10] + 7) * x67)
    x73 = ((z34 % 26) - 1) != monad[11]
    if x73 == 1:
        return 10, 0, 0, 1
    z37 = ((int(z34 / 26)) * ((25 * x73) + 1)) + ((monad[11] + 7) * x73)
    x79 = ((z37 % 26) - 10) != monad[12]
    if x79 == 1:
        return 11, 0, 0, 1
    z40 = ((int(z37 / 26)) * ((25 * x79) + 1)) + ((monad[12] + 2) * x79)
    x85 = ((z40 % 26) - 16) != monad[13]
    if x85 == 1:
        return 12, 0, 0, 1
    return 0, 0, 0, (((int(z40 / 26)) * ((25 * x85) + 1)) + ((monad[13] + 2) * x85))


# Cache setup
shared_cache = {"": (0, 0, 0, 0)}
shared_monad = monad[:-1]
shrinking_cache = {}  # When we need to run the rest of the code

# Debug
step = 0
start_dt = time()

# TODO: MAYBE LOOK AT MOVING BY BIGGER STEPS, ASSUMING THAT Z SORT OF MOVES SLOWLY

# Loop through all monads
while True:
    step += 1

    # # Get or add shared monad section to shared_cache
    # shared_mem = get_or_save_shared_monad_mem(
    #     shared_monad, shared_cache, input_fns, maths_fns
    # )
    # # assert shared_mem == get_or_save_shared_monad_mem_old_1(
    # #     shared_monad, shared_cache, growing_fns
    # # )

    # # Now finish the calculation
    # start_index = len(shared_monad)
    # # mem = apply_shrinking_function(monad, shrinking_fns, shared_mem, start_index)
    # mem = apply_shrinking_function(
    #     monad, input_fns, shrinking_fns, shared_mem, start_index, shrinking_cache
    # )
    # # assert mem == apply_shrinking_function_old(
    # #     monad, shrinking_fns, shared_mem, start_index
    # # )

    mem = get_mem(monad)

    # print(monad, mem)

    if mem[3] == 0:
        print(f"--- LARGEST VALID MONAD: {monad} ---")
        exit()

    fail_index = mem[0]
    parts = [int(c) for c in monad]
    parts[fail_index] -= 1
    monad = "".join(map(str, parts))

    if "0" in monad:
        monad = reduce_monad(monad)

    # - COMMENT OUT WHEN HAPPY IT WORKS - #
    # Assert partial calculations are same as full calculation
    # assert mem == get_mem(monad)
    # ----------------------------------- #

    # new_monad = reduce_monad(monad)
    # shared_monad = get_shared_monad(monad, new_monad)
    # monad = new_monad

    # if step == 1:
    # if step == 100000:
    if step == 1000000:  # ~6.7s (~3.4s with no timeit)
        # if step == 10000000:  # ~70s (~34s with no timeit... ~9999997)
        # if step == 10000000000:  # (~9997?)
        print(f"Solution not found, next monad to try: {monad}")
        break

# print_logged_times()
total_time = time() - start_dt
print(f"\nTotal run time: {total_time:.3f}s\n")
# print_total_time(total_time)
