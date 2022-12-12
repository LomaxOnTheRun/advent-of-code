# Start time: 07:31
# End time: 08:10

import aocd

data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

data = aocd.get_data(year=2022, day=11)

items = {}
worry_ops = {}
next_ops = {}
next_ops_str = {}
stress_divide = 1

for monkey_id, monkey in enumerate(data.split("\n\n")):
    lines = monkey.split("\n")
    items[monkey_id] = eval(f"[{lines[1][18:]}]")
    worry_ops[monkey_id] = eval(f"lambda old: {lines[2][19:]}")
    next_ops[monkey_id] = eval(
        f"lambda item: {int(lines[5][30:])} if item % {int(lines[3][21:])} else {int(lines[4][29:])}"
    )
    if stress_divide % int(lines[3][21:]):
        stress_divide *= int(lines[3][21:])

inspections = [0] * len(items)
for round in range(10000):
    for monkey_id in range(len(items)):
        while items[monkey_id]:
            inspections[monkey_id] += 1
            item = items[monkey_id].pop(0)
            new_worry = worry_ops[monkey_id](item) % stress_divide
            next_monkey = next_ops[monkey_id](new_worry)
            items[next_monkey].append(new_worry)

print(sorted(inspections)[-1] * sorted(inspections)[-2])
