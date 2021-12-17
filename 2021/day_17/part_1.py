import aocd

data = """target area: x=20..30, y=-10..-5"""

data = aocd.get_data(year=2021, day=17)

_, _, x_target, y_target = data.split(" ")
x_min, _ = map(int, x_target[2:-1].split(".."))
y_min, _ = map(int, y_target[2:].split(".."))

tri = lambda x: int((x * (x + 1)) / 2)

# Find the smallest dx possible
dx = 0
while tri(dx) < x_min:
    dx += 1

# Find the biggest step from 0 to the bottom of the target
dy = -(y_min + 1)

print(tri(dy))
