import aocd, re


def get_mem(monad):
    m = [-1 for _ in monad]
    monad = [int(c) for c in monad]
    m[3] = monad[2] + 4
    m[6] = monad[5] - 3
    m[8] = monad[7] + 6
    m[10] = monad[9]
    m[11] = monad[4] + 1
    m[12] = monad[1] - 2
    m[13] = monad[0] - 8
    return 0, m


# SMALLEST

m0 = 9
m1 = 3
m2 = 1
m3 = 5
m4 = 1
m5 = 4
m6 = 1
m7 = 1
m8 = 7
m9 = 1
m10 = 1
m11 = 2
m12 = 1
m13 = 1

monad = 93151411711211


# BIGGEST

m0 = 9
m1 = 9
m2 = 5
m3 = 9
m4 = 8
m5 = 9
m6 = 6
m7 = 3
m8 = 9
m9 = 9
m10 = 9
m11 = 9
m12 = 7
m13 = 1

monad = 99598963999971

# def get_mem(monad):
#     monad = [int(c) for c in monad]

#     # ALL UNWRAPS NEED TO HAPPEN

#     monad = [int(c) for c in monad]
#     z10 = ((((monad[0] + 8) * 26) + (monad[1] + 8)) * 26) + (monad[2] + 12)
#     if ((z10 % 26) - 8) != monad[3]:  # monad[3] = ((z10 % 26) - 8)
#         z13 = (int(z10 / 26) * 26) + (monad[3] + 10)
#     else:
#         z13 = int(z10 / 26)

#     z19 = (((z13 * 26) + (monad[4] + 2)) * 26) + (monad[5] + 8)
#     if ((z19 % 26) - 11) != monad[6]:  # monad[6] = ((z19 % 26) - 11)
#         z25 = (int(z19 / 26) * 26) + (monad[6] + 4)
#     else:
#         z25 = int(z19 / 26)
#     z25 = (z25 * 26) + (monad[7] + 9)

#     if ((z25 % 26) - 3) != monad[8]:  # monad[8] = ((z25 % 26) - 3)
#         z31 = (int(z25 / 26) * 26) + (monad[8] + 10)
#     else:
#         z31 = int(z25 / 26)
#     z31 = (z31 * 26) + (monad[9] + 3)

#     if ((z31 % 26) - 3) != monad[10]:  # monad[10] = ((z31 % 26) - 3)
#         z34 = (int(z31 / 26) * 26) + (monad[10] + 7)
#     else:
#         z34 = int(z31 / 26)

#     if ((z34 % 26) - 1) != monad[11]:  # monad[11] = ((z34 % 26) - 1)
#         z37 = (int(z34 / 26) * 26) + (monad[11] + 7)
#     else:
#         z37 = int(z34 / 26)

#     if ((z37 % 26) - 10) != monad[12]:  # monad[12] = ((z37 % 26) - 10)
#         z40 = (int(z37 / 26) * 26) + (monad[12] + 2)
#     else:
#         z40 = int(z37 / 26)

#     # z_final must be zero
#     # if ((z40 % 26) - 16) != monad[13]:
#     #     z_final = (int(z40 / 26) * 26) + (monad[13] + 2)
#     # else:
#     #     z_final = int(z40 / 26)
#     monad[13] = (z40 % 26) - 16
#     z_final = int(z40 / 26)

#     return 0, 0, 0, z_final


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
    d = d.copy()
    # print(code, "\n")
    for var in "wxyz":
        while d[var] > 0:
            full_var = f"{var}{d[var]}"

            # print_all = full_var == "x13"
            print_all = full_var == "z43"
            print_all = False

            if print_all:
                print(code, "\n")

            if print_all:
                print("full_var", full_var)

            all_calls = re.findall(rf"{full_var}(?!\d).?.?.?", code)
            num_calls = len(all_calls)

            if print_all:
                print("num_calls", num_calls)

            orig_str = f"\n    {full_var} = .*"

            orig = re.search(rf"{orig_str}", code)
            if print_all:
                print("orig", orig)

            replace = re.search(rf"{full_var}(\D)", code)
            if print_all:
                print("replace", replace)

            if all_calls and all([call[-3:] == " = " for call in all_calls]):
                # Remove original line
                code = re.sub(rf"    {full_var} = .*\n", "", code)
                continue

            if num_calls == 1:
                # Remove original line
                code = re.sub(rf"    {full_var} = .*\n", "", code)

            direct_equals = bool(re.search(rf" {full_var} = [\S]+\n", code))
            if print_all:
                print("direct_equals", direct_equals)

            if num_calls == 2 or direct_equals:
                # Get original variable definition
                v = re.search(rf"    {full_var} = (.*)\n", code)[1]
                if print_all:
                    print("var_use", re.search(rf"(?<!  ){full_var}(?=\D|$)", code))
                # Replace all non-instantiation vars with original
                code = re.sub(rf"(?<!  ){full_var}(?=\D|$)", rf"({v})", code)
            d[var] -= 1

    # Remove any empty if/else clauses
    code = re.sub(r"\n\s+if .*:\n\s+else:\n", "", code)

    # Pull out z_final into own line
    # code = re.sub(r"(return 0, 0, 0, )(\(.+)$", r"z_final = \2\n    \1z_final", code)
    code = re.sub(r"(return 0, 0, 0, )(\(.+)$", r"z1000 = \2\n    \1z1000", code)

    return code


def reduce_code(code):

    # print(code)

    # (wxyz) => wxyz
    code = re.sub(r"\((.\d+)\)", r"\1", code)
    # (\d+) => \d+
    code = re.sub(r"\((\d+)\)", r"\1", code)
    # wxyz * 0 => 0
    code = re.sub(r"\w\d+ \* 0", "0", code)
    # (0 * wxyz) => 0
    code = re.sub(r"\(0 \* \w\d+\)", "0", code)
    # (wxyz + 0) => wxyz
    code = re.sub(r"\((.\d+) \+ 0\)", r"\1", code)
    # (0 + wxyz) => wxyz
    code = re.sub(r"\(0 \+ (.\d+)\)", r"\1", code)
    # 0 + wxyz => wxyz
    code = re.sub(r" 0 \+ (\w\d+\D)", r" \1", code)
    # int(wxyz / 1) => wxyz
    code = re.sub(r"int\((\w?\d+) / 1\)", r"\1", code)
    # int(wxyz) => wxyz
    code = re.sub(r"int\((\w\d+)\)", r"\1", code)
    # x + -y => x - y
    code = re.sub(r" \+ -", " - ", code)
    # (0 % x) => 0
    code = re.sub(r"\(0 % ([^\)]+)\)", "0", code)
    # (... == xwyz) == 0
    code = re.sub(r"\((.*) == (\w\d+)\) == 0", r"\1 != \2", code)
    # (0 * ((...))) => 0
    code = re.sub(r"\(0 \* \(\([^\(\)]*\)[^\(\)]*\)\)", "0", code)
    # 0 + ... => ...
    code = re.sub(r" = 0 \+ ([^\n]*)\n", r" = \1\n", code)
    # . == . => 1
    code = re.sub(r"(\w?\d+) == \1", "1", code)
    # ... * 1\n => ...\n
    code = re.sub(r"(.*) \* 1\n", r"\1\n", code)
    # (0 + int(monad[.])) => int(monad[.])
    code = re.sub(r"\(0 \+ (monad\[\d+])\)", r"\1", code)
    # ... == monad[.]) == 0 => ... != monad[.])
    code = re.sub(r"(.*) == monad\[(\d+)\]\) == 0", r"\1 != monad[\2])", code)
    # ... * 1) => ...)
    code = re.sub(r"(.*) \* 1\)", r"\1)", code)
    # (... != monad[.]) => ... != monad[.]
    code = re.sub(r" = \((.*) != monad\[(\d+)\]\)\n", r" = \1 != monad[\2]\n", code)
    # =wxyz => = wxyz
    code = re.sub(r"=([^= ])", r"= \1", code)
    # (monad[.]) => monad[.]
    code = re.sub(r"\((monad\[\d+\])\)", r"\1", code)
    # ((monad[.] + .)) => (monad[.] + .)
    code = re.sub(r"\((\(monad\[\d+\] \+ \w?\d+\))\)", r"\1", code)
    # (int(wxyz / \d+)) => int(wxyz / \d+)
    code = re.sub(r"\((int\(\w\d+\ / \d+\))\)", r"\1", code)
    #  ) => ) (space is removed)
    code = re.sub(r" \)", ")", code)
    # int(.) + 0 => int(.)
    code = re.sub(r"(int\([^\)]+\)) \+ 0", r"\1", code)

    return code


def custom_logic(code):

    # 10+ == monad[.] => 0
    code = re.sub(r"\(\d\d == monad\[\d+\]", r"(0", code)
    # 10+ != monad[.] => 1
    code = re.sub(r"\(\d\d != monad\[\d+\]", r"(1", code)

    # (wxyz % 26) + 10+ will always be bigger than monad[.]
    code = re.sub(r"\(\(\w\d+ % 26\) \+ \d\d\) != monad\[\d+\]", r"1", code)
    code = re.sub(r"\(\(\w\d+ % 26\) \+ \d\d\) == monad\[\d+\]", r"0", code)

    # 25 + 1 = 26
    code = re.sub(r"(?<![\w\d])25 \+ 1(?![\w\d])", "26", code)
    # 0 + 1 = 1
    code = re.sub(r"(?<![\w\d])0 \+ 1(?![\w\d])", "1", code)
    # ((monad[.] +- .) * 0) = 0
    code = re.sub(r"\(\(monad\[\d+\] [\+-] \d+\) \* 0\)", "0", code)

    # wxyz = ... + 0 => wxyz = ...
    code = re.sub(r"(\w\d+ = .*) \+ 0\n", r"\1\n", code)

    # Split into if/else lines
    inner = r"\((.*) \* \(\(25 \* (\w\d+)\) \+ 1\)\) \+ \(\((monad\[\d+\] [\+-] \d+)\) \* \3\)"
    start = rf"(\w\d+) = {inner}\n"
    end = r"""if \3:
        \1 = (\2 * ((25 * 1) + 1)) + ((\4) * 1)
    else:
        \1 = (\2 * ((25 * 0) + 1)) + ((\4) * 0)\n\n"""
    code = re.sub(start, end, code)

    # Split a more complex line
    # z25 = (((int(z19 / 26) * ((25 * x43) + 1)) + ((monad[6] + 4) * x43)) * 26) + (monad[7] + 9)
    start = rf"(\w\d+) = \(\({inner}\) \* 26\) \+ (.*)\n"
    end = r"""if \3:
        \1 = (\2 * ((25 * 1) + 1)) + ((\4) * 1)
    else:
        \1 = (\2 * ((25 * 0) + 1)) + ((\4) * 0)
    \1 = (\1 * 26) + \5\n\n"""
    code = re.sub(start, end, code)

    # We need to divide by 26 as much as possible, so pick those if/else paths
    start = r"""if \((.*) != monad\[(\d+)\]\):\n.*\n\s+else:\n\s+(.*)"""
    end = r"m[\2] = \1\n    \3"
    code = re.sub(start, end, code)

    # Hack to make if/else work for final line
    code = re.sub(r"z1000 = \(\((.*)\)\)", r"z1000 = (\1)", code)

    # Squash reassingment lines into one
    start = r"(\w\d+) = (.*)\n\s+\1 = \(\1 (.*)\n"
    end = r"\1 = ((\2) \3\n"
    code = re.sub(start, end, code)

    return code


def custom_logic_2(code):

    # print("1: ----------------------")

    # Remove empty lines
    code = re.sub(r"\n *\n", "\n", code)

    # Hack
    code = re.sub(r"(z3[47]) = \(\((.*)\)\)\n", r"\1 = (\2)\n", code)

    # Split line into divisor and remainder wherever they're used
    start = r"(\w\d+) = \((.*) \* 26\) \+ (.*)\n"
    start += r"\s+(m\[\d+\]) = \(\(\1 % 26\) (- \d+)\)\n"
    start += r"(\s+\w\d+) = (\(?)int\(\1 / 26\)(.*)"
    # m = re.search(start, code)
    # if m:
    #     print()
    #     for i in range(9):
    #         print(i, m[i])
    #     print()
    end = r"\4 = \3 \5\n\6 = \7\2\8"
    code = re.sub(start, end, code)

    # print(f"\n{code}\n")

    # print("2: ----------------------")

    # Do it again, but for a more complex bit of logic
    # z25 = (((int(z10 / 26) * 26) + (monad[4] + 2)) * 26) + (monad[7] + 9)
    # m[8] = ((z25 % 26) - 3)
    # m[10] = (monad[9] + 3) - 3
    # z34 = int(z25 / 26)
    # start = r"(\w\d+) = \((.*) \* 26\) \+ (.*)\n"
    start = r"(\w\d+) = \((.*) \* 26\) \+ (.*)\n"
    start += r"\s+(m\[\d+\]) = \(\(\1 % 26\) (- \d+)\)\n"
    start += r"((.*\n)*)"  # Possibly many lines
    start += r"(\s+\w\d+) = (\(?)int\(\1 / 26\)(.*)"
    # m = re.search(start, code)
    # if m:
    #     print()
    #     for i in range(10):
    #         print(i, m[i])
    #     print()
    # end = r"\4 = \3 \5\6\7 = \8\2\9"
    end = r"\4 = \3 \5\n\6\8 = \9\2\10"
    code = re.sub(start, end, code)

    # print(f"\n{code}\n")

    return code


def custom_logic_3(code):

    # Hacky way of doing maths
    code = re.sub(r"\((monad\[\d+\]) \+ 12\) - 8", r"\1 + 4", code)
    code = re.sub(r"\((monad\[\d+\]) \+ 8\) - 11", r"\1 - 3", code)
    code = re.sub(r"\((monad\[\d+\]) \+ 9\) - 3", r"\1 + 6", code)
    code = re.sub(r"\((monad\[\d+\]) \+ 3\) - 3", r"\1", code)
    code = re.sub(r"\((monad\[\d+\]) \+ 2\) - 1", r"\1 + 1", code)
    code = re.sub(r"\((monad\[\d+\]) \+ 8\) - 10", r"\1 - 2", code)

    return code


def simplify_code(code, show_steps=False):
    code, d = create_unique_var_names(code)
    # We only care about z
    code = re.sub(r"return .*, (.+)$", r"return 0, 0, 0, \1", code)
    if show_steps:
        print(f"unique:\n\n{code}\n")

    # Run combine and simplify in a loop until no changes
    loops = 0
    while True:
        loops += 1

        # if loops == 4:
        #     show_steps = True
        #     print(f"original:\n\n{code}\n")

        old_code = "" + code
        code = combine_vars(code, d)
        if show_steps:
            print(f"combine:\n\n{code}\n")

        # if loops == 4:
        #     break

        code = reduce_code(code)
        if show_steps:
            print(f"reduce:\n\n{code}\n")

        # if loops == 4:
        #     break

        code = custom_logic(code)
        if show_steps:
            print(f"logic:\n\n{code}\n")

        if code == old_code:
            break

        # DEBUG
        # if loops == 4:
        #     break

    loops = 0
    while True:
        loops += 1
        old_code = "" + code

        code = custom_logic_2(code)

        if code == old_code:
            break

        # print(code)

        # if loops == 2:
        #     break

    code = custom_logic_3(code)

    code = code.split("\n")
    # code[-1] = "    return z_final, m"
    code[-1] = "    return z1000, m"
    code = "\n".join(code)

    return code


def create_function(data, fn_name, inp_index=0, show_code=False, show_steps=False):
    # function_str = f"def {fn_name}(monad, w=0, x=0, y=0, z=0):\n"
    function_str = f"def {fn_name}(monad):\n"
    function_str += "    m = [-1 for _ in monad]\n"
    function_str += "    monad = [int(c) for c in monad]\n"
    function_str += "    w = 0\n"
    function_str += "    x = 0\n"
    function_str += "    y = 0\n"
    function_str += "    z = 0\n"

    OP = {
        "add": "{0} + {1}",
        "mul": "{0} * {1}",
        "div": "int({0} / {1})",
        "mod": "{0} % {1}",
        "eql": "{0} == {1}",
    }

    for line in data.strip().split("\n"):
        name, ab = line.strip().split(" ", 1)
        if name == "inp":
            # function_str += f"    {ab} = int(monad[{inp_index}])\n"
            function_str += f"    {ab} = monad[{inp_index}]\n"
            inp_index += 1
        else:
            a, b = ab.split(" ")
            function_str += f"    {a} = " + OP[name].format(a, b) + "\n"
    function_str += "    return w, x, y, z"

    function_str = simplify_code(function_str, show_steps=show_steps)
    if show_code:
        print(function_str, "\n")

    exec(function_str, globals())

    return globals()[fn_name]


data = aocd.get_data(year=2021, day=24)

# get_mem = create_function(data, "get_mem", show_code=False, show_steps=False)
get_mem = create_function(data, "get_mem", show_code=True, show_steps=False)

# Run it to make sure the code is runs
print(*get_mem("0" * 14))

# Make sure I'm still getting the correct answer
# assert get_mem("0" * 14)[3] == 98884034
# assert get_mem("1" * 14)[3] == 111240665
# assert get_mem("2" * 14)[3] == 123597296
# assert get_mem("3" * 14)[3] == 135953927
# assert get_mem("4" * 14)[3] == 148310558
# assert get_mem("5" * 14)[3] == 160667189
# assert get_mem("6" * 14)[3] == 173023820
# assert get_mem("7" * 14)[3] == 185380451
# assert get_mem("8" * 14)[3] == 197737082
# assert get_mem("9" * 14)[3] == 210093713
