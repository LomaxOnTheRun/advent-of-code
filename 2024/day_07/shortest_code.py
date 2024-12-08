import aocd


def test(curr: int, exp: int, nums: list[int], part: bool):
    if not nums:
        return curr == exp
    if test(curr + nums[0], exp, nums[1:], part):
        return True
    if test(curr * nums[0], exp, nums[1:], part):
        return True
    return test(int(f"{curr}{nums[0]}"), exp, nums[1:], part) if part else False


sums = [0, 0]
for line in aocd.get_data(year=2024, day=7).splitlines():
    nums = [int(num.strip(":")) for num in line.split()]
    sums = [sums[i] + nums[0] * test(0, nums[0], nums[1:], bool(i)) for i in (0, 1)]

print(f"{sums[0]}\n{sums[1]}")
