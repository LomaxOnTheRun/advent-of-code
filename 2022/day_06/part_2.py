# Start time: 06:42
# End time:

import aocd

data = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""
# data = """bvwbjplbgvbhsrlpgdmjqwftvncz"""
# data = """nppdvjthqldpwncqszvftbrmjlhg"""
# data = """nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"""
# data = """zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"""

data = aocd.get_data(year=2022, day=6)

for i, char in enumerate(data[14:]):
    if len(set(data[i : i + 14])) == 14:
        print(i + 14)
        break
