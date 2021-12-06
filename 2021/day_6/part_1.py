import aocd

# data = """3,4,3,1,2"""

data = aocd.get_data(year=2021, day=6)

old = [int(age) for age in data.split(",")]
for _ in range(80):
    new = [age - 1 if age > 0 else 6 for age in old]
    new += [8] * old.count(0)
    if _ == 79:
        print(len(new))
    old = new
