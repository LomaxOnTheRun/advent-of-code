import aocd, re

data = aocd.get_data(year=2024, day=3)

# Part 1
print(sum(int(x) * int(y) for x, y in re.findall(r"mul\((\d+),(\d+)\)", data)))

# Part 2
data = re.sub(r"don't\(\).*?((do\(\))|$)", "", data.replace("\n", ""))
print(sum(int(x) * int(y) for x, y in re.findall(r"mul\((\d+),(\d+)\)", data)))
