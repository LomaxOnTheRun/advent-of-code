# Start time: 15:00
# End time: 15:10

import aocd

data = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

data = aocd.get_data(year=2023, day=1)

def check_for_number(line: str, number: str) -> bool:
    return line.startswith(number)

numbers_int = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
numbers_str = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

sum = 0
for line in data.split():
    found_numbers = []
    for x in range(len(line)):
        line_segment = line[x:]
        for number in range(10):
            if check_for_number(line_segment, numbers_int[number]):
                found_numbers.append(number)
                break
            if check_for_number(line_segment, numbers_str[number]):
                found_numbers.append(number)
                break
    number = int(str(found_numbers[0]) + str(found_numbers[-1]))
    sum += number

print(sum)
