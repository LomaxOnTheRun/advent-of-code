import aocd

# data = """3,4,3,1,2"""

data = aocd.get_data(year=2021, day=6)

fish = {pc: list(map(int, data.split(","))).count(pc) for pc in range(9)}
for day in range(256):
    fish = {pc: fish.get(pc + 1, 0) + fish[0] * (pc in (6, 8)) for pc in range(9)}
    print(sum(fish.values())) if day in (79, 255) else None
