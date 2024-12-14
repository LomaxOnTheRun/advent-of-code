# Start time: 10:44
# End time: 11:20

import aocd, re, dataclasses

# data = """p=0,4 v=3,-3
# p=6,3 v=-1,-3
# p=10,3 v=-1,2
# p=2,0 v=2,-1
# p=0,0 v=1,3
# p=3,0 v=-2,-2
# p=7,6 v=-1,-3
# p=3,0 v=-1,-2
# p=9,3 v=2,3
# p=7,3 v=-1,2
# p=2,4 v=2,-3
# p=9,5 v=-3,-3"""
# WIDTH, HEIGHT = 11, 7

data = aocd.get_data(year=2024, day=14)
WIDTH, HEIGHT = 101, 103


@dataclasses.dataclass
class Robot:
    x: int
    y: int
    dx: int
    dy: int

    def step(self):
        self.x = (self.x + self.dx) % WIDTH
        self.y = (self.y + self.dy) % HEIGHT

    def __repr__(self):
        return f"Robot: p({self.x}, {self.y}) v({self.dx}, {self.dy})"


robots = []
for line in data.splitlines():
    match = re.match(r"p=(.+),(.*) v=(.*),(.*)$", line)
    x, y, dx, dy = match.groups()
    robots.append(Robot(int(x), int(y), int(dx), int(dy)))


def print_robots(robots):
    for y in range(HEIGHT):
        line = ""
        for x in range(WIDTH):
            char = "."
            for robot in robots:
                if robot.x == x and robot.y == y:
                    char = "X"
                    break
            line += char
        print(line)


def is_xmas_tree(robots):
    robots_xy = {(robot.x, robot.y) for robot in robots}

    # Look for top of tree
    for x, y in robots_xy:
        for i in range(1, 3):
            if not (x - i, y + i) in robots_xy:
                return False
            if not (x + i, y + i) in robots_xy:
                return False
        return True
    return False


step = 0
while True:
    step += 1
    for robot in robots:
        robot.step()

    if is_xmas_tree(robots):
        break

print(step)
