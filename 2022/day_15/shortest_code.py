# 34 lines

import aocd


def reduce_radii_edges(edges, i):
    """Combine all overlapping beacon areas for a line."""
    # Edge pairs that are completely overlapped by the previous pair can be removed
    if edges[i + 1][1] <= edges[i][1]:
        edges.pop(i + 1)
        # We might need to re-combine this edge pair so recursively call the function
        if len(edges[i:]) > 1:
            reduce_radii_edges(edges, i)
    # Edge pairs that overlap or are directly adjacent (touching) can be combined
    elif edges[i + 1][0] <= edges[i][1] or edges[i][1] + 1 == edges[i + 1][0]:
        edges[i] = (edges[i][0], edges[i + 1][1])
        edges.pop(i + 1)


def get_radii_edges(sensors, y, min_xy, max_xy):
    """Get the edges of all beacons that intersect the given line."""
    radii_edges = []
    for (sx, sy), radius in sensors.items():
        # Calculate the edges of a sensor's area for the given line
        radius_start = max(sx - (radius - abs(sy - y)), min_xy)
        radius_end = min(sx + (radius - abs(sy - y)), max_xy)
        # Only include areas that actually overlap the line
        if radius_start < radius_end:
            radii_edges.append((radius_start, radius_end))
    radii_edges.sort()

    # Try to merge the last radius edges into the previous one
    for i in range(len(radii_edges) - 2, -1, -1):
        reduce_radii_edges(radii_edges, i)

    return radii_edges


sensors = {}
known_beacons = set()
for line in aocd.get_data(year=2022, day=15).split("\n"):
    # Parse data into tuples of ints
    sensor = (int(line.split(" ")[2][2:-1]), int(line.split(" ")[3][2:-1]))
    beacon = (int(line.split(" ")[8][2:-1]), int(line.split(" ")[9][2:]))
    # We only need the beacon and its radius
    sensors[sensor] = abs(beacon[0] - sensor[0]) + abs(beacon[1] - sensor[1])
    # We'll need to remove known beacons for part 1
    known_beacons.add(beacon)


# Part 1
radii_edges = get_radii_edges(sensors, 2000000, -1e10, 1e10)
beacons_in_line = len([beacon for beacon in known_beacons if beacon[1] == 2000000])
print(sum([edges[1] - edges[0] + 1 for edges in radii_edges]) - beacons_in_line)

# Part 2
for y in range(4000000 + 1):
    if len(radii_edges := get_radii_edges(sensors, y, 0, 4000000)) == 2:
        print(((radii_edges[0][1] + 1) * 4000000) + y)
        break
