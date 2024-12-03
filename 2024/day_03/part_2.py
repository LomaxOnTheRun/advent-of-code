# Start time: 13:15
# End time: 13:51

import aocd
import re

data = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
data = "mul(1,1)don't()mul(1,2)don't()mul(1,3)do()mul(1,4)don't()mul(1,5)"

data = aocd.get_data(year=2024, day=3)

data = data.replace("\n", "")
data = re.sub(r"don't\(\).*?do\(\)", "", data)
data = re.sub(r"don't\(\).*?$", "", data)
vals = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data)
print(sum([int(v1) * int(v2) for v1, v2 in vals]))

# 66427443 is too low
# 94286334 is too high
# 110824057 is too high
