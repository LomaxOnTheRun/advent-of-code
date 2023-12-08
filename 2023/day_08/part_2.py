# Start time: 08:58
# End time: 14:01

import aocd

data = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

data = aocd.get_data(year=2023, day=8)

steps, maps_str = data.split("\n\n")

links = {}
for line in maps_str.splitlines():
    node, next_nodes = line.split(" = ")
    links[node] = next_nodes.strip("()").split(", ")

start_nodes = [node for node in links if node[-1] == "A"]
cycle_lengths = {}

current_nodes = [node for node in links if node[-1] == "A"]
total_steps = 0
while len(cycle_lengths) != len(start_nodes):
    current_step = steps[total_steps % len(steps)]
    total_steps += 1

    current_nodes = [
        links[current_node][int(current_step == "R")] for current_node in current_nodes
    ]

    for i, current_node in enumerate(current_nodes):
        start_node = start_nodes[i]
        if current_node[-1] == "Z":
            if start_node in cycle_lengths:
                continue

            cycle_lengths[start_node] = total_steps

total = 1
for cycle_length in cycle_lengths.values():
    total *= cycle_length


def prime_numbers(max_num: int) -> list[int]:
    prime_numbers = []
    for i in range(2, max_num + 1):
        for prime_number in prime_numbers:
            if i % prime_number == 0:
                break
        else:
            prime_numbers.append(i)

    return prime_numbers


all_primes = []
for cycle_length in cycle_lengths.values():
    primes = {num: 0 for num in prime_numbers(cycle_length)}
    while cycle_length > 1:
        for prime in primes:
            if cycle_length % prime == 0:
                primes[prime] += 1
                cycle_length //= prime
    primes = {num: val for num, val in primes.items() if val > 0}
    all_primes.append(primes)

max_primes = {}
for primes in all_primes:
    for val, num_vals in primes.items():
        if val not in max_primes:
            max_primes[val] = num_vals
            continue

        if val > max_primes[val]:
            max_primes[val] = num_vals
            continue

total = 1
for val, num_vals in max_primes.items():
    total *= val * num_vals
print(total)
