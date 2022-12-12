# 22 lines

import aocd


def get_monkey_args(part):
    items, worry_ops, next_ops = [], [], []
    stress_divide = 1

    for monkey in aocd.get_data(year=2022, day=11).split("\n\n"):
        _, l1, l2, l3, l4, l5 = monkey.split("\n")
        # Starting items / worry
        items.append(eval(f"[{l1[18:]}]"))
        # Lambda functions to calculate new worry level (per monkey)
        worry_ops.append(eval(f"lambda old: ({l2[19:]})" + (" // 3" * (part == 1))))
        # Lambda functions to calculate next monkey to pass to (per monkey)
        next_ops.append(eval(f"lambda i: {l5[30:]} if i % {l3[21:]} else {l4[29:]}"))
        # We can divide the total stress by the product of all divide checks
        stress_divide *= int(l3[21:])

    return items, worry_ops, next_ops, stress_divide


def monkey_business_level(items, worry_ops, next_ops, stress_divide, rounds):
    inspections = [0] * len(items)
    for _ in range(rounds):
        for monkey in range(len(items)):
            while items[monkey]:
                # Keep track of each monkey's inspections
                inspections[monkey] += 1
                # Calculate the new worry level
                new_worry = worry_ops[monkey](items[monkey].pop(0)) % stress_divide
                # Claculate the next monkey to pass the item to
                items[next_ops[monkey](new_worry)].append(new_worry)

    # Monkey business level
    return sorted(inspections)[-1] * sorted(inspections)[-2]


# Part 1
print(monkey_business_level(*get_monkey_args(part=1), rounds=20))

# Part 2
print(monkey_business_level(*get_monkey_args(part=2), rounds=10000))
