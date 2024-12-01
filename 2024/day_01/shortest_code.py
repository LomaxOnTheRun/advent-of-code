import aocd

data = aocd.get_data(year=2024, day=1)

left, right = [sorted(data.split()[i::2]) for i in (0, 1)]

# Part 1
print(sum(abs(int(l) - int(r)) for l, r in zip(left, right)))

# Part 2
print(sum(int(l) * right.count(l) for l in left))
