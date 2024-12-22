# Start time: 13:08
# End time: 14:48

import aocd

# data = """1
# 10
# 100
# 2024"""

# data = """123"""

# data = """1
# 2
# 3
# 2024"""

data = aocd.get_data(year=2024, day=22)


def evolve(num):
    num = (num ^ (num << 6)) % 16777216
    num = (num ^ (num >> 5)) % 16777216
    num = (num ^ (num << 11)) % 16777216
    return num


def get_evolutions(num, num_evolutions=2000):
    evolutions = [num]
    for i in range(num_evolutions):
        num = evolve(num)
        evolutions.append(num)
    return evolutions


def get_prices_for_diff_sequences(initial_num):
    prices_for_diff_sequences = {}
    nums = get_evolutions(initial_num)
    prices, diffs = [], []
    for i, num in enumerate(nums):
        price = num % 10
        prices.append(price)
        if i > 0:
            diff = price - prices[i - 1]
            diffs.append(diff)
        if i > 4:
            diff_sequence = tuple(diffs[i - 4 : i])
            if diff_sequence in prices_for_diff_sequences:
                continue
            prices_for_diff_sequences[diff_sequence] = price
    return prices, diffs, prices_for_diff_sequences


def get_bananas_for_diff(diff):
    bananas = 0
    for num in initial_nums:
        prices_for_diff_sequences = PRICES_FOR_DIFF_SEQUENCES[num]
        bananas += prices_for_diff_sequences.get(diff, 0)
    return bananas


initial_nums = [int(line) for line in data.split()]

PRICES, DIFFS, PRICES_FOR_DIFF_SEQUENCES = {}, {}, {}
diffs_for_9s = set()
for num in initial_nums:
    prices, diffs, prices_for_diff_sequences = get_prices_for_diff_sequences(num)
    PRICES[num] = prices
    DIFFS[num] = diffs
    PRICES_FOR_DIFF_SEQUENCES[num] = prices_for_diff_sequences

    for diff, price in prices_for_diff_sequences.items():
        if price == 9:
            diffs_for_9s.add(diff)

max_bananas = 0
for diff in diffs_for_9s:
    bananas = get_bananas_for_diff(diff)
    max_bananas = max(max_bananas, bananas)
print(max_bananas)
