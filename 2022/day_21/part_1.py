# Start time: 07:11
# End time: 07:25

import aocd

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

numbers = {}
operations = {}
for line in data.split("\n"):
    name = line[:4]
    job = line[6:].split()

    if len(job) == 1:
        numbers[name] = int(job[0])
    else:
        monkeys = (job[0], job[2])
        op = job[1]
        operations[name] = (monkeys, op)

while "root" not in numbers:
    for name, ((monkey_1, monkey_2), op) in operations.items():
        if monkey_1 in numbers and monkey_2 in numbers:
            number = eval(f"{numbers[monkey_1]} {op} {numbers[monkey_2]}")
            del operations[name]
            numbers[name] = int(number)
            break

print(numbers["root"])
