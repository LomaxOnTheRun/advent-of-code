# Start time: 12:12
# End time: 12:37

import aocd, re

data = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

data = aocd.get_data(year=2024, day=13)


class Machine:
    def __init__(self, ax, ay, bx, by, prize_x, prize_y):
        self.ax = int(ax)
        self.ay = int(ay)
        self.bx = int(bx)
        self.by = int(by)
        self.prize_x = int(prize_x) + 10000000000000
        self.prize_y = int(prize_y) + 10000000000000

    def __repr__(self):
        return f"Machine: A({self.ax}, {self.ay}) B({self.bx}, {self.by}), P({self.prize_x}, {self.prize_y})"

    def get_cheapest_price(self):
        top = (self.prize_x * self.by) - (self.prize_y * self.bx)
        bottom = (self.ax * self.by) - (self.ay * self.bx)
        if top % bottom != 0:
            return 0
        num_a = top // bottom
        num_b = (self.prize_x - (num_a * self.ax)) // self.bx
        return (3 * num_a) + num_b


machines = []
for machine in data.split("\n\n"):
    match = re.match(r".*X+(.*), Y+(.*)\n.*X+(.*), Y+(.*)\n.*X=(.*), Y=(.*)$", machine)
    machines.append(Machine(*match.groups()))

total = 0
for m in machines:
    cheapest = m.get_cheapest_price()
    total += cheapest
print(total)
