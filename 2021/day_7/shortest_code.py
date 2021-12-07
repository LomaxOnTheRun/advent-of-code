import aocd

data = [int(x) for x in aocd.get_data(year=2021, day=7).split(",")]

tri = lambda x: int((x * (x + 1)) / 2)
print(min([sum([abs(x - mid) for x in data]) for mid in range(max(data))]))
print(min([sum([tri(abs(x - mid)) for x in data]) for mid in range(max(data))]))

# fuel = lambda type: (lambda x: int((x * (x + 1)) / 2)) if type else (lambda x: x)
# sums = lambda xs, fuel: [sum([fuel(abs(x - m)) for x in xs]) for m in range(max(xs))]
# print(f"{min(sums(data, fuel(0)))}\n{min(sums(data, fuel(1)))}")
