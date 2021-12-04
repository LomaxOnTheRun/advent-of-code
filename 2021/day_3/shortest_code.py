import aocd, re

data = f"\n{aocd.get_data(year=2021, day=3)}"

most = lambda d, n: int(len(re.findall(f"\n.{{{n}}}1", d)) > (d.count("\n") / 2))

# Part 1
γ = int("".join([str(most(data, n)) for n in range(len(data.split("\n")[1]))]), 2)
ε = int("".join([str(1 - most(data, n)) for n in range(len(data.split("\n")[1]))]), 2)
print(γ * ε)
