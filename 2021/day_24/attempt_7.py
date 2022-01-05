import aocd


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
    assert shrinking_fns[0](*input_vars) == full_fn(*input_vars)
    input_fns = create_input_functions(EXAMPLE_DATA)
    maths_fns = create_maths_functions(EXAMPLE_DATA)
    monad_in_out = [
        (0, "1234", (0, 0, 0, 0), (8, 4, 6, 8)),
        (1, "1234", (2, 0, 0, 0), (8, 4, 6, 8)),
        (2, "1234", (8, 4, 0, 0), (8, 4, 6, 8)),
        (3, "1234", (8, 4, 6, 0), (8, 4, 6, 8)),
    ]
    for index, monad, ex_in, ex_out in monad_in_out:
        mem_1 = apply_functions(monad, input_fns, maths_fns, ex_in, index)
        mem_2 = apply_shrinking_function(monad, shrinking_fns, ex_in, index)
        assert mem_1 == ex_out
        assert mem_2 == ex_out


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


# @timeit
def create_function(data, fn_name, inp_index=0):
    # function_str = f"@timeit\ndef {fn_name}(monad, w=0, x=0, y=0, z=0):\n"
    function_str = f"def {fn_name}(monad, w=0, x=0, y=0, z=0):\n"

    OP = {
        "add": "{0} + {1}",
        "mul": "{0} * {1}",
        "div": "int({0} / {1})",
        "mod": "{0} % {1}",
        "eql": "int({0} == {1})",
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

    exec(function_str, globals())

    return globals()[fn_name]


# @timeit
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


# @timeit
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


# @timeit
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


# @timeit
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


# @timeit
# def apply_functions(monad, input_fns, math_fns, mem=(0, 0, 0, 0), start_index=0):
#     for index in range(start_index, len(monad)):
#         mem = input_fns[index](monad, *mem)
#         mem = math_fns[index](monad, *mem)
#     return mem


# @timeit
# def apply_functions_grow(monad, input_fns, math_fns, mem=(0, 0, 0, 0), start_index=0):
#     return apply_functions(monad, input_fns, math_fns, mem, start_index)


# @timeit
# def apply_functions_shrink(monad, input_fns, math_fns, mem=(0, 0, 0, 0), start_index=0):
#     return apply_functions(monad, input_fns, math_fns, mem, start_index)


@timeit
def apply_growing_function(shared_monad, growing_fns, mem=(0, 0, 0, 0)):
    return growing_fns[len(shared_monad) - 1](shared_monad, *mem)


@timeit
def apply_shrinking_function(monad, shrinking_fns, shared_mem, start_index=0):
    return shrinking_fns[start_index](monad, *shared_mem)


@timeit
def reduce_monad(monad, monad_len=14):
    while monad[-1] == "1":
        monad = monad[:-1]
    monad = str(int(monad) - 1)
    if len(monad) < monad_len:
        monad += NINES[monad_len - len(monad)]
    return monad


@timeit
def get_shared_monad(old_monad, new_monad):
    shared_monad = new_monad[:-1]
    len_shared_monad = len(shared_monad)
    while old_monad[:len_shared_monad] != shared_monad:
        shared_monad = shared_monad[:-1]
        len_shared_monad -= 1
    return shared_monad


# @timeit
# def get_or_save_shared_monad_mem_old_1(shared_monad, shared_cache, growing_fns):
#     mem = shared_cache.get(shared_monad)
#     if mem is None:
#         mem = apply_growing_function(shared_monad, growing_fns)
#         # assert mem == apply_functions_grow(shared_monad, input_fns, maths_fns)
#         shared_cache[shared_monad] = mem
#     return mem


# @timeit
# def get_or_save_shared_monad_mem_old_2(shared_monad, shared_cache, input_fns, maths_fns):
#     # print("shared_monad", shared_monad)
#     for i in range(len(shared_monad)):
#         partial = shared_monad[: i + 1]
#         # print("partial", partial)
#         if partial not in shared_cache:
#             # print(f"PARTIAL NOT IN CACHE: {partial}")
#             last_partial = partial[:-1]
#             mem = shared_cache[last_partial]
#             mem = input_fns[len(last_partial)](partial, *mem)
#             mem = maths_fns[len(last_partial)](partial, *mem)
#             shared_cache[partial] = mem
#     # print(shared_cache)
#     return shared_cache[shared_monad]


@timeit
def get_or_save_shared_monad_mem(shared_monad, shared_cache, input_fns, maths_fns):
    # print("shared_monad", shared_monad)
    max_index = len(shared_monad)
    partial = shared_monad[:max_index]
    # Roll back to smallest known cache
    while partial not in shared_cache:
        max_index -= 1
        partial = shared_monad[:max_index]
        # print("max_index", max_index)

    # print("BUILDING BACK UP")

    # Now recreate missing caches
    while max_index < len(shared_monad):
        max_index += 1
        # print("max_index", max_index)
        partial = shared_monad[:max_index]
        # print("partial", partial)
        # print(f"PARTIAL NOT IN CACHE: {partial}")
        last_partial = partial[:-1]
        mem = shared_cache[last_partial]
        mem = input_fns[len(last_partial)](partial, *mem)
        mem = maths_fns[len(last_partial)](partial, *mem)
        shared_cache[partial] = mem

    # print(shared_cache)
    return shared_cache[shared_monad]


NINES = {x: "9" * x for x in range(1, 14)}


function_creation_example()
input_functions_creation_example()
maths_functions_creation_example()
shrinking_functions_creation_example()
growing_functions_creation_example()
apply_functions_example()
reduce_monad_examples()
shared_monad_examples()

# exit()

# Setup
data = aocd.get_data(year=2021, day=24)
get_mem = create_function(data, "get_mem")
input_fns = create_input_functions(data)
maths_fns = create_maths_functions(data)
growing_fns = create_growing_functions(data)
shrinking_fns = create_shrinking_functions(data)
monad = "99999999999999"

# Cache setup
shared_cache = {"": (0, 0, 0, 0)}
shared_monad = monad[:-1]

# Debug
step = 0
start_dt = time()

# Loop through all monads
while True:
    step += 1

    # Get or add shared monad section to shared_cache
    shared_mem = get_or_save_shared_monad_mem(
        shared_monad, shared_cache, input_fns, maths_fns
    )
    # assert shared_mem == get_or_save_shared_monad_mem_old_1(
    #     shared_monad, shared_cache, growing_fns
    # )

    # Now finish the calculation
    start_index = len(shared_monad)
    mem = apply_shrinking_function(monad, shrinking_fns, shared_mem, start_index)
    # assert mem == apply_functions_shrink(
    #     monad, input_fns, maths_fns, shared_mem, start_index
    # )

    if mem[3] == 0:
        print(f"--- LARGEST VALID MONAD: {monad} ---")

    # - COMMENT OUT WHEN HAPPY IT WORKS - #
    # Assert partial calculations are same as full calculation
    # assert mem == get_mem(monad)
    # ----------------------------------- #

    new_monad = reduce_monad(monad)
    shared_monad = get_shared_monad(monad, new_monad)
    monad = new_monad

    # if step == 1000000:  # ~7.5s
    # if step == 10000000:  # ~75s
    if step == 100000000:
        print(f"Solution not found, next monad to try: {monad}")
        break

print_logged_times()
total_time = time() - start_dt
print(f"\nTotal run time: {total_time:.3f}s")
print_total_time(total_time)
