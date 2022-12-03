# Start time: 06:48
# End time: 06:55

import aocd

data = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

# data = aocd.get_data(year=2022, day=3)


total_priority = 0
group = []
for index, bag in enumerate(data.split()):
    if index % 3 == 0:
        group = []
    group.append(bag)

    if index % 3 == 2:
        badge = list(set(group[0]) & set(group[1]) & set(group[2]))[0]

        priority = ord(badge) - 96
        if priority < 0:
            priority += 58

        total_priority += priority

print(total_priority)
