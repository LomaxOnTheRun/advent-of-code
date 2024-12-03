import aocd


totals = [0, 0]
for rep in aocd.get_data(year=2024, day=2).splitlines():
    perms = [[int(x) for x in rep.split()] for _ in range(rep.count(" ") + 2)]
    [rep.pop(i) for i, rep in enumerate(perms[:-1])]
    perms_diffs = [{rep[i] - rep[i + 1] for i in range(len(rep) - 1)} for rep in perms]
    for pt, ds in ((0, [perms_diffs[-1]]), (1, perms_diffs)):
        totals[pt] += any(d.issubset({1, 2, 3}) or d.issubset({-1, -2, -3}) for d in ds)

# Parts 1 and 2
print(f"{totals[0]}\n{totals[1]}")
