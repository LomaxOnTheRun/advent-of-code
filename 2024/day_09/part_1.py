import aocd

data = """2333133121414131402"""
# data = """23331331214141314021111"""
# data = """12345"""
# data = "1111111111111111111111111111"

data = aocd.get_data(year=2024, day=9)

files = [int(x) * [i] for i, x in enumerate(data[::2])]
spaces = [int(x) for x in data[1::2]]

selif = list(reversed([x for y in files for x in y]))

filled_spaces = []
for space in spaces:
    nums = selif[:space]
    filled_spaces.append(nums)
    selif = selif[space:]
filled_spaces.append(selif)

zipped = [x for z in zip(files, filled_spaces) for y in z for x in y]
zipped = zipped[: len(zipped) // 2]

checksum = sum(i * x for i, x in enumerate(zipped))
print(checksum)
