# 6 lines

import aocd

data = aocd.get_data(year=2022, day=3)

# Part 1
bags = [(bag[: len(bag) // 2], bag[len(bag) // 2 :]) for bag in data.split()]
print(sum([(ord(({*left} & {*right}).pop()) - 96) % 58 for left, right in bags]))

# Part 2
groups = zip(*[[{*bag} for bag in data.split()[i::3]] for i in (0, 1, 2)])
print(sum([(ord((b1 & b2 & b3).pop()) - 96) % 58 for b1, b2, b3 in groups]))


# Still kind of neat...

# # Part 1
# bags = [(bag[: len(bag) // 2], bag[len(bag) // 2 :]) for bag in data.split()]
# items = [(set(left) & set(right)).pop() for left, right in bags]
# print(sum([(ord(item) - 96) % 58 for item in items]))

# # Part 2
# groups = zip(*[data.split()[i::3] for i in (0, 1, 2)])
# items = [(set(bag_1) & set(bag_2) & set(bag_3)).pop() for bag_1, bag_2, bag_3 in groups]
# print(sum([(ord(item) - 96) % 58 for item in items]))
