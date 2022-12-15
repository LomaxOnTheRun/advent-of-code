# Start time: 06:40
# End time: 07:09

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

data = aocd.get_data(year=2022, day=15)

sensors = {}
beacons = set()
for line in data.split("\n"):
    _, _, sensor_x, sensor_y, _, _, _, _, beacon_x, beacon_y = line.split(" ")
    sensor = (int(sensor_x[2:-1]), int(sensor_y[2:-1]))
    beacon = (int(beacon_x[2:-1]), int(beacon_y[2:]))
    sensors[sensor] = abs(beacon[0] - sensor[0]) + abs(beacon[1] - sensor[1])
    beacons.add(beacon)

line_y = 2000000

no_beacons = set()
for (sensor_x, sensor_y), radius in sensors.items():
    diff_y = abs(sensor_y - line_y)
    for x in range(sensor_x - (radius - diff_y), sensor_x + (radius - diff_y) + 1):
        no_beacons.add((x, line_y))

print(len(no_beacons - beacons))


# 6221085 is too high
