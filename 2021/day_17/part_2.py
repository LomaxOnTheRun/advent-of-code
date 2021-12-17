import aocd

data = """target area: x=20..30, y=-10..-5"""

data = aocd.get_data(year=2021, day=17)

_, _, x_target, y_target = data.split(" ")
x_min, x_max = map(int, x_target[2:-1].split(".."))
y_min, y_max = map(int, y_target[2:].split(".."))

in_target = lambda x, y: x_min <= x <= x_max and y_min <= y <= y_max
overshot = lambda x, y: x > x_max or y < y_min
tri = lambda x: int((x * (x + 1)) / 2)

# Find the smallest dx possible
min_dx = 0
while tri(min_dx) < x_min:
    min_dx += 1

# Max dx is first step being at far edge of target
max_dx = x_max

# Find the smallest step from 0 to the target
min_dy = y_min

# Find the biggest step from 0 to the bottom of the target
max_dy = -(y_min + 1)

# For each possible dx and dy, run through the trajectory to see if it hits
successes = []
for initial_dx in range(min_dx, max_dx + 1):
    for initial_dy in range(min_dy, max_dy + 1):
        dx, dy = initial_dx, initial_dy
        x, y = 0, 0
        while not overshot(x, y):
            x += dx
            y += dy
            dx = max(dx - 1, 0)
            dy -= 1
            if in_target(x, y):
                successes.append((initial_dx, initial_dy))
                break

print(len(successes))
