# Start time: 06:49
# End time: 07:32

import aocd, math

data = """Time:      7  15   30
Distance:  9  40  200"""

data = aocd.get_data(year=2023, day=6)

times, dists = data.splitlines()
times = [int(x) for x in times.split()[1:]]
dists = [int(x) for x in dists.split()[1:]]

num_options = 1
for time, dist in zip(times, dists):
    min_press = int((time - math.sqrt((time * time) - (4 * dist))) / 2) + 1
    max_press = int((time + math.sqrt((time * time) - (4 * dist))) / 2)

    if min_press * (time - min_press) <= dist:
        min_press += 1

    if max_press * (time - max_press) <= dist:
        max_press -= 1

    num_options *= max_press - min_press + 1

print(num_options)
