# Start time: 07:25
# End time: 09:00

import aocd, re

data = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

data = aocd.get_data(year=2022, day=21)

jobs = {}
for line in data.split("\n"):
    name = line[:4]
    job = line[6:]
    if name == "humn":
        jobs[name] = "?"
    elif " " in job:
        jobs[name] = f"({job})"
    else:
        jobs[name] = job


left, right = jobs["root"][1:-1].split(" + ")
jobs.pop("root")

while re.search("[a-z]{4}", left + right):
    for name, job in jobs.items():
        left = left.replace(name, job)
        right = right.replace(name, job)

right = int(eval(right))

inners = True
while inners:
    inners = re.findall("\([^?\(\)]+\)", left)
    for inner in inners:
        left = left.replace(inner, str(int(eval(inner))))

while left != "?":
    if left[0] == "(" and left[-1] == ")":
        left = left[1:-1]

    if left[-1] not in [")", "?"]:
        left_parts = left.split(" ")
        if left_parts[-2] == "+":
            right -= int(left_parts[-1])
        if left_parts[-2] == "-":
            right += int(left_parts[-1])
        if left_parts[-2] == "/":
            right *= int(left_parts[-1])
        if left_parts[-2] == "*":
            right /= int(left_parts[-1])
        right = right
        left = " ".join(left_parts[:-2])

    elif left[0] != "(":
        left_parts = left.split(" ")
        if left_parts[1] == "+":
            right -= int(left_parts[0])
        if left_parts[1] == "-":
            # right += int(left_parts[0])
            right = int(left_parts[0]) - right
        if left_parts[1] == "*":
            right /= int(left_parts[0])
        right = right
        left = " ".join(left_parts[2:])

print(int(right))
