# Start time: 13:08
# End time: 13:15

import aocd
import re

data = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

data = aocd.get_data(year=2024, day=3)

vals = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data)
print(sum([int(v1) * int(v2) for v1, v2 in vals]))
