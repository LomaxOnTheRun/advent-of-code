# Start time: 11:01
# End time: 11:40

import aocd

data = """125 17"""

data = aocd.get_data(year=2024, day=11)

stones = data.split()
for i in range(25):
    new_stones = []
    for stone in stones:
        if stone == "0":
            new_stones += ["1"]
        elif len(stone) % 2 == 0:
            for new_stone in (stone[: len(stone) // 2], stone[len(stone) // 2 :]):
                new_stone = new_stone.lstrip("0")
                new_stones += [new_stone if new_stone else "0"]
        else:
            new_stones += [str(int(stone) * 2024)]

    stones = new_stones

print(len(stones))
