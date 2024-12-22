# Start time: 12:30
# End time: 12:59

import aocd

data = """1
10
100
2024"""

# data = """123"""

data = aocd.get_data(year=2024, day=22)


def mul_64(num):
    return num << 6


def mul_2048(num):
    return num << 11


def div_32(num):
    return num >> 5


def mix(num, val):
    return num ^ val


def prune(num):
    return num % 16777216


def evolve(num):
    # Step 1
    val = mul_64(num)
    num = mix(num, val)
    num = prune(num)
    # Step 2
    val = div_32(num)
    num = mix(num, val)
    num = prune(num)
    # Step 3
    val = mul_2048(num)
    num = mix(num, val)
    num = prune(num)
    return num


total = 0
for num in [int(line) for line in data.split()]:
    for i in range(2000):
        num = evolve(num)
    total += num
print(total)
