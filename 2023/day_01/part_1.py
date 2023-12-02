# Start time: 15:00
# End time: 15:10

import aocd

data = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

data = aocd.get_data(year=2023, day=1)

sum = 0
for line in data.split():
    line = line.strip("abcdefghijklmnopqrstuvwxyz")
    number = int(line[0] + line[-1])
    sum += number

print(sum)
