# Start time 1: 7:45am
# End time 1: 8:22am
import aocd, re

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
pairs = [pair.split(" -> ") for pair in pairs.split("\n")]
pairs = {a + c: (a + b, b + c) for (a, c), b in pairs}

# Create a dict showing number of pairs in the chain
chain_dict = {}
for i in range(len(chain) - 1):
    pair = chain[i : i + 2]
    chain_dict[pair] = chain_dict.get(pair, 0) + 1

for _ in range(40):
    # Create a new dict for the expanded chain
    new_chain_dict = {}
    for pair, num in chain_dict.items():
        for new_pair in pairs[pair]:
            new_chain_dict[new_pair] = new_chain_dict.get(new_pair, 0) + num
    chain_dict = new_chain_dict

# Count difference of counts
counts = {chain[0]: 1, chain[-1]: 1}  # We're double counting all but the ends
for pair, num in chain_dict.items():
    for element in pair:
        counts[element] = counts.get(element, 0) + num

counts = {element: int(num / 2) for element, num in counts.items()}

print(max(counts.values()) - min(counts.values()))
