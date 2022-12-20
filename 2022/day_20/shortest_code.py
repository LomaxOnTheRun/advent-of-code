# 15 lines

import aocd


def mix(nums: list[int], moves: list[int]) -> None:
    # Go through all numbers
    for i in range(len(nums)):
        # Get new index for num (always at very end instead of very start)
        new = (moves.index(i) + nums[moves.index(i)]) % (len(nums) - 1) or len(nums)
        # Move the num and the related position tracker to the correct place
        nums.insert(new, nums.pop(moves.index(i)))
        moves.insert(new, moves.pop(moves.index(i)))


def create_nums_and_moves_lists(key: int = 1) -> tuple[list[int], list[int]]:
    # Convert data to ints and multiply by key (if given)
    nums = [int(num) * key for num in aocd.get_data(year=2022, day=20).split()]
    # The second list keeps track of the initial positions of each number
    return nums, list(range(len(nums)))


# Part 1
nums, moves = create_nums_and_moves_lists()
mix(nums, moves)
print(sum([nums[(dx + nums.index(0)) % len(nums)] for dx in (1000, 2000, 3000)]))

# Part 2
nums, moves = create_nums_and_moves_lists(key=811589153)
[mix(nums, moves) for _ in range(10)]
print(sum([nums[(dx + nums.index(0)) % len(nums)] for dx in (1000, 2000, 3000)]))
