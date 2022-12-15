# Start time: 07:09
# End time: 08:15

import aocd

data = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""
(min_xy, max_xy) = (0, 20)

data = aocd.get_data(year=2022, day=15)
(min_xy, max_xy) = (0, 4000000)

sensors = {}
known_beacons = set()
for line in data.split("\n"):
    _, _, sensor_x, sensor_y, _, _, _, _, beacon_x, beacon_y = line.split(" ")
    sensor = (int(sensor_x[2:-1]), int(sensor_y[2:-1]))
    beacon = (int(beacon_x[2:-1]), int(beacon_y[2:]))
    sensors[sensor] = abs(beacon[0] - sensor[0]) + abs(beacon[1] - sensor[1])
    known_beacons.add(beacon)


def reduce_radii(radius_edges, i):
    if len(radius_edges[i:]) < 2:
        return radius_edges
    prev, next = radius_edges[i : i + 2]
    if prev[0] <= next[0] and next[1] <= prev[1]:
        radius_edges.pop(i + 1)
        radius_edges = reduce_radii(radius_edges, i)
    elif next[0] <= prev[1] and prev[1] <= next[1]:
        radius_edges.pop(i)
        radius_edges.pop(i)
        radius_edges.insert(i, (prev[0], next[1]))
    elif prev[1] + 1 == next[0]:
        radius_edges.pop(i)
        radius_edges.pop(i)
        radius_edges.insert(i, (prev[0], next[1]))

    return radius_edges


coord = (0, 0)
for line_y in range(max_xy + 1):
    # if line_y % 100000 == 0:
    #     print(line_y)
    radius_edges = []
    for (sensor_x, sensor_y), radius in sensors.items():
        dy = abs(sensor_y - line_y)
        radius_start = max(sensor_x - (radius - dy), min_xy)
        radius_end = min(sensor_x + (radius - dy), max_xy)
        if radius_start < radius_end:
            radius_edges.append((radius_start, radius_end))

    radius_edges.sort()

    for i in range(len(radius_edges) - 2, -1, -1):
        radius_edges = reduce_radii(radius_edges, i)

    if len(radius_edges) == 2:
        coord = (radius_edges[0][1] + 1, line_y)
        break


print((coord[0] * 4000000) + coord[1])
