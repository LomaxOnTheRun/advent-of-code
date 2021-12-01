last_value = 9999999999
num_increases = 0

with open("input.txt") as input_file:
    for value in input_file:
        if int(value) > last_value:
            num_increases += 1
        last_value = int(value)


print(num_increases)
