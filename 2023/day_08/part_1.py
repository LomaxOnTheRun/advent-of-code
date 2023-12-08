# Start time: 08:43
# End time: 08:58

import aocd

# data = """RL
#
# AAA = (BBB, CCC)
# BBB = (DDD, EEE)
# CCC = (ZZZ, GGG)
# DDD = (DDD, DDD)
# EEE = (EEE, EEE)
# GGG = (GGG, GGG)
# ZZZ = (ZZZ, ZZZ)"""

data = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

data = aocd.get_data(year=2023, day=8)

steps, maps_str = data.split("\n\n")

links = {}
for line in maps_str.splitlines():
    node, next_nodes = line.split(" = ")
    links[node] = next_nodes.strip("()").split(", ")

current_node = "AAA"
total_steps = 0
while current_node != "ZZZ":
    current_step = steps[total_steps % len(steps)]
    current_node = links[current_node][int(current_step == "R")]
    total_steps += 1

print(total_steps)
