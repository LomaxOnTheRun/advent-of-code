import re

ops_str_1 = """def run_ops_1(w, x, y, z):
    x *= 0
    x += z
    x %= 26
    z = int(z / 1)
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

ops_str_2 = """def run_ops_2(w, x, y, z):
    x = (z % 26) + 11
    x = int(x == w)
    x = int(x == 0)
    y = (25 * x) + 1
    z *= y
    y = (w + 8) * x
    z += y
    return w, x, y, z
"""

ops_str_3 = """def run_ops_3(w, x, y, z):
    x = x * 0
    x = x + z
    x = x % 26
    z = int(z / 1)
    x = x + 11
    x = int(x == w)
    x = int(x == 0)
    y = y * 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = y * 0
    y = y + w
    y = y + 8
    y = y * x
    y = y * x
    y = y * x
    y = y * x
    y = y * x
    y = y * x
    z = z + y
    y = int(y / 1)
    return w, x, y, z
"""

exec(ops_str_1, globals())
exec(ops_str_2, globals())
exec(ops_str_3, globals())
# exec(ops_str_4, globals())

runs = 10
for w in range(runs):
    for x in range(runs):
        for y in range(runs):
            for z in range(runs):
                mem_1 = run_ops_1(0, 0, 0, 0)
                mem_2 = run_ops_2(0, 0, 0, 0)
                mem_3 = run_ops_3(0, 0, 0, 0)
                # mem_4 = run_ops_4(0, 0, 0, 0)
                # assert mem_1 == mem_2 == mem_3 == mem_4
                assert mem_1 == mem_2 == mem_3


def create_unique_var_names(code):
    d = {"w": 0, "x": 0, "y": 0, "z": 0}
    lines = [line for line in code.split("\n")]
    for index, line in enumerate(lines):
        # Replace signature
        if index == 0:
            for var in "wxyz":
                lines[0] = lines[0].replace(var, f"{var}0")
            continue

        # Create unique var names
        for var in "wxyz":
            if var in line:
                line = line.replace(f" {var} =", f" {var}{d[var] + 1} =")
                line = re.sub(rf"{var}([^\d]+|$)", rf"{var}{d[var]}\1", line)
                if f" {var}{d[var] + 1} = " in line:
                    d[var] += 1
        lines[index] = line
    return "\n".join(lines), d


def combine_vars(code, d):
    for var in "wxyz":
        while d[var] > 0:
            if len(re.findall(rf"{var}{d[var]}(\D|$)", code)) == 2:
                # Get original variable definition
                v = re.search(rf"    {var}{d[var]} = (.*)", code)[1]
                # Remove original line
                code = re.sub(rf"\n.* {var}{d[var]} = .*", "", code)
                # Place original defenition into only other calling place
                code = re.sub(rf"{var}{d[var]}( |,|$)", rf"({v})\1", code)
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
    # (wxyz) => wxyz
    code = re.sub(r"\((.\d+)\)", r"\1", code)
    return code


unique_code, d = create_unique_var_names(ops_str_3)
print("- unique -")
print(unique_code)
print()
short_code = combine_vars(unique_code, d)
print("- combined -")
print(short_code)
print()
reduced_code = reduce_code(short_code)
print("- reduced -")
print(reduced_code)

# exec(short_code, globals())
exec(reduced_code, globals())
print(run_ops_3(0, 0, 0, 0))
