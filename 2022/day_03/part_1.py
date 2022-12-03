# Start time: 06:35
# End time: 06:48

import aocd

data = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

data = aocd.get_data(year=2022, day=3)


def get_item_priority(left, right):
    for item in left:
        if item in right:
            priority = ord(item) - 96
            if priority < 0:
                priority += 58
            return priority


total_priority = 0
for bag in data.split():
    left = bag[: int(len(bag) / 2)]
    right = bag[int(len(bag) / 2) :]
    total_priority += get_item_priority(left, right)

print(total_priority)
