import aocd

data = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

data = aocd.get_data(year=2024, day=5)

orders_str, updates_str = data.split("\n\n")

reversed_rules = set()
for order_str in orders_str.split():
    x = int(order_str.split("|")[0])
    y = int(order_str.split("|")[1])
    reversed_rules.add((y, x))

updates = []
for line in updates_str.split():
    updates.append([int(x) for x in line.split(",")])

total = 0
for update in updates:
    update_pairs = set()
    for i in range(len(update)):
        for j in range(i + 1, len(update)):
            update_pairs.add((update[i], update[j]))

    if not update_pairs & reversed_rules:
        continue

    while rules := update_pairs & reversed_rules:
        y, x = rules.pop()
        xi, yi = update.index(x), update.index(y)
        update[yi] = x
        update[xi] = y
        update_pairs = set()
        for i in range(len(update)):
            for j in range(i + 1, len(update)):
                update_pairs.add((update[i], update[j]))
    total += update[len(update) // 2]

print(total)
