import aocd, re, functools as ft

data = aocd.get_data(year=2021, day=10)

# Values for both parts
vals = {")": 3, "]": 57, "}": 1197, ">": 25137, "(": 1, "[": 2, "{": 3, "<": 4, " ": 0}
# Reduce a line multiple times to remove all valid matching pairs
rl = lambda lin: ft.reduce(lambda l, _: re.sub(r"(\(\)|\[\]|{}|<>)", "", l), lin, lin)
# Get the corrupt score for a line
corr = lambda line: vals[re.sub(r"[([{<]", "", rl(line) + " ")[0]]

# Part 1
# Sum all of the corrupted scores
print(sum([corr(line) for line in data.split("\n") if corr(line)]))

# Part 2
# Get values for the brackets that need to be closed
inc_vals = lambda line: [vals[c] for c in re.sub(r"[)\]}>]", "", rl(line))[::-1]]
# Calculate the incomplete score
calc = lambda rest: sum([rest[i] * pow(5, len(rest) - i - 1) for i in range(len(rest))])
# Get all the incomplete scores
incs = [calc(inc_vals(line)) for line in data.split("\n") if not corr(line)]
# Get the median score
print(sorted(incs)[int(len(incs) / 2)])
