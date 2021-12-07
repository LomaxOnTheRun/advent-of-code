# Start time: 7:24am
# End time: 7:27am

import aocd

# data = """16,1,2,0,4,2,7,1,2,14"""

data = aocd.get_data(year=2021, day=7)

data = [int(x) for x in data.split(",")]

tri = lambda x: (x * (x + 1)) / 2

diffs = {mid: sum([tri(abs(x - mid)) for x in data]) for mid in range(max(data))}

print(int(min(diffs.values())))
