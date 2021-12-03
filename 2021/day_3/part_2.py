import aocd

data = aocd.get_data(year=2021, day=3).split("\n")

num_bits = len(data[0])

o2_data = [line for line in data]
for bit in range(num_bits):
    num_0 = 0
    num_1 = 0
    for line in o2_data:
        if line[bit] == "0":
            num_0 += 1
        else:
            num_1 += 1

    if num_0 > num_1:
        if len(o2_data) > 1:
            o2_data = [line for line in o2_data if line[bit] == "0"]
    else:
        if len(o2_data) > 1:
            o2_data = [line for line in o2_data if line[bit] == "1"]

co2_data = [line for line in data]
for bit in range(num_bits):
    num_0 = 0
    num_1 = 0
    for line in co2_data:
        if line[bit] == "0":
            num_0 += 1
        else:
            num_1 += 1

    if num_0 > num_1:
        if len(co2_data) > 1:
            co2_data = [line for line in co2_data if line[bit] == "1"]
    else:
        if len(co2_data) > 1:
            co2_data = [line for line in co2_data if line[bit] == "0"]

o2 = o2_data[0]
co2 = co2_data[0]

print(int(o2, 2) * int(co2, 2))
