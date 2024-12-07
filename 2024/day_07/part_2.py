# Start time: 14:29
# End time: 14:53

import aocd

data = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

data = aocd.get_data(year=2024, day=7)

calcs = {}
for line in data.splitlines():
    total, nums = line.split(": ")
    calcs[int(total)] = [int(num) for num in nums.split()]


def is_total_expected(current, expected, nums):
    if not nums:
        return current == expected

    if is_total_expected(current + nums[0], expected, nums[1:]):
        return True
    if is_total_expected(current * nums[0], expected, nums[1:]):
        return True
    return is_total_expected(int(str(current) + str(nums[0])), expected, nums[1:])


totals_sum = 0
for total, nums in calcs.items():
    if is_total_expected(0, total, nums):
        totals_sum += total
        continue

print(totals_sum)
