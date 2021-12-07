# Start time: 7:15am
# End time: 7:24

import aocd

# data = """16,1,2,0,4,2,7,1,2,14"""

data = aocd.get_data(year=2021, day=7)

data = [int(x) for x in data.split(",")]

diffs = {best_x: sum([abs(x - best_x) for x in data]) for best_x in range(max(data))}

print(min(diffs.values()))
