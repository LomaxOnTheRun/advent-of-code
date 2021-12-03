import aocd

data = aocd.get_data(year=2021, day=3).split("\n")

gamma = ""
epsilon = ""

for bit in range(len(data[0])):
    num_0 = 0
    num_1 = 0
    for line in data:
        if line[bit] == "0":
            num_0 += 1
        else:
            num_1 += 1

    if num_0 > num_1:
        gamma += "0"
        epsilon += "1"
    else:
        gamma += "1"
        epsilon += "0"

print(int(gamma, 2) * int(epsilon, 2))
