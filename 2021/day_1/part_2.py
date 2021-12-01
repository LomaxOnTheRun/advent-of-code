last_values = []
num_increases = 0

with open("input.txt") as input_file:
    for value in input_file:
        last_values.append(int(value))
        if len(last_values) > 4:
            last_values.pop(0)
        if sum(last_values[1:4]) > sum(last_values[0:3]):
            num_increases += 1

print(num_increases)
