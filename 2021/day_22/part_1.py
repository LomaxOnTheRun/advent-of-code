import aocd

data = aocd.get_data(year=2021, day=22)

data = [line.split(" ") for line in data.split("\n")]
for line in data:
    line[1] = [coord[2:] for coord in line[1].split(",")]
    line[1] = [tuple(map(int, coord.split(".."))) for coord in line[1]]

on_set = set()
for on_off, (dx, dy, dz) in data:
    for x in range(dx[0], dx[1] + 1):
        if x < -50 or x > 50:
            continue

        for y in range(dy[0], dy[1] + 1):
            if y < -50 or y > 50:
                continue

            for z in range(dz[0], dz[1] + 1):
                if z < -50 or z > 50:
                    continue

                if on_off == "on":
                    on_set.add((x, y, z))

                elif on_off == "off" and (x, y, z) in on_set:
                    on_set.remove((x, y, z))

print(len(on_set))
