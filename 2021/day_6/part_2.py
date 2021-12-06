import aocd

# data = """3,4,3,1,2"""

data = aocd.get_data(year=2021, day=6)

old = {age: 0 for age in range(9)}
for age in data.split(","):
    old[int(age)] += 1

for day in range(256):
    new = {age: 0 for age in range(9)}

    # Move closer to birth
    for age in range(1, 9):
        new[age - 1] = old[age]
    # Calculate births
    new[6] += old[0]
    new[8] += old[0]

    if day == 255:
        print(sum(new.values()))
    old = new
