# Start time: 7:24am
# End time: 7:45am

import aocd

data = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

data = aocd.get_data(year=2021, day=14)

chain, pairs = data.split("\n\n")
pairs = [pair for pair in pairs.split("\n")]
pairs = {p.split(" -> ")[0]: p.split(" -> ")[1] for p in pairs}

for _ in range(10):
    chain_parts = [chain[i : i + 2] for i in range(len(chain) - 1)]
    new_chain_parts = []
    for part in chain_parts:
        if part in pairs:
            new_part = f"{part[0]}{pairs[part]}{part[1]}"
        else:
            new_part = f"{part[0]}{part[1]}{part[1]}"
        new_chain_parts.append(new_part)

    new_chain_parts[-1] += "_"
    chain = "".join([part[:-1] for part in new_chain_parts])

counts = [chain.count(letter) for letter in set(chain)]
print(max(counts) - min(counts))
