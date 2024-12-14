# Start time: 11:28
# End time: 12:12

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
        self.prize_x = int(prize_x)
        self.prize_y = int(prize_y)

    def __repr__(self):
        return f"Machine: A({self.ax}, {self.ay}) B({self.bx}, {self.by}), P({self.prize_x}, {self.prize_y})"

    def get_all_prices(self):
        prices = []
        for num_b in range(max(self.prize_x // self.bx, self.prize_y // self.by)):
            num_a = (self.prize_x - (num_b * self.bx)) / self.ax
            if int(num_a) != num_a:
                continue
            if int(num_a) != (self.prize_y - (num_b * self.by)) / self.ay:
                continue
            prices.append((3 * int(num_a)) + num_b)
        return prices

    def get_cheapest_price(self):
        prices = self.get_all_prices()
        return min(prices) if prices else 0


machines = []
for machine in data.split("\n\n"):
    match = re.match(r".*X+(.*), Y+(.*)\n.*X+(.*), Y+(.*)\n.*X=(.*), Y=(.*)$", machine)
    machines.append(Machine(*match.groups()))

total = 0
for m in machines:
    cheapest = m.get_cheapest_price()
    total += cheapest
print(total)
