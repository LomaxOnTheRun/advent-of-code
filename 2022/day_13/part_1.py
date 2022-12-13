# Start time: 06:41
# End time: 07:06

import aocd

data = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

data = aocd.get_data(year=2022, day=13)

CORRECT_ORDER = "CORRECT_ORDER"
INCORRECT_ORDER = "INCORRECT_ORDER"


def compare(left, right):
    if type(left) == int and type(right) == list:
        if outcome := compare([left], right):
            return outcome

    if type(left) == list and type(right) == int:
        if outcome := compare(left, [right]):
            return outcome

    if type(left) == type(right) == int:
        if left < right:
            return CORRECT_ORDER
        elif left > right:
            return INCORRECT_ORDER

    if type(left) == type(right) == list:
        for i in range(min(len(left), len(right))):
            if outcome := compare(left[i], right[i]):
                return outcome
        if len(left) < len(right):
            return CORRECT_ORDER
        elif len(left) > len(right):
            return INCORRECT_ORDER


indices = []
for i, pair in enumerate(data.split("\n\n")):
    left, right = [eval(side) for side in pair.split()]
    outcome = compare(left, right)
    if outcome == CORRECT_ORDER:
        indices.append(i + 1)

print(sum(indices))
