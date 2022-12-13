# Start time: 07:06
# End time: 07:18

import aocd, functools

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


def is_correct_order(left, right):
    if type(left) == int and type(right) == list:
        if outcome := is_correct_order([left], right):
            return outcome

    if type(left) == list and type(right) == int:
        if outcome := is_correct_order(left, [right]):
            return outcome

    if type(left) == type(right) == int:
        if left < right:
            return -1
        elif left > right:
            return 1

    if type(left) == type(right) == list:
        for i in range(min(len(left), len(right))):
            if outcome := is_correct_order(left[i], right[i]):
                return outcome
        if len(left) < len(right):
            return -1
        elif len(left) > len(right):
            return 1


pairs = [eval(packet) for packet in data.split()] + [[[2]], [[6]]]

pairs = sorted(pairs, key=functools.cmp_to_key(is_correct_order))

print((pairs.index([[2]]) + 1) * (pairs.index([[6]]) + 1))
