# Start time: 14:30
# End time: 15:23

import aocd

data = """1
2
-3
3
-2
0
4"""

data = aocd.get_data(year=2022, day=20)

nums = [int(num) for num in data.split()]
len_nums = len(nums)
move_indices = list(range(len_nums))

for i in range(len_nums):
    old_nums_index = move_indices.index(i)
    num = nums.pop(old_nums_index)
    move_index = move_indices.pop(old_nums_index)

    new_nums_index = (old_nums_index + num) % (len_nums - 1)

    if new_nums_index == 0:
        nums.append(num)
        move_indices.append(move_index)
    else:
        nums.insert(new_nums_index, num)
        move_indices.insert(new_nums_index, move_index)

zero_index = nums.index(0)
print(sum([nums[(offset + zero_index) % len_nums] for offset in (1000, 2000, 3000)]))
