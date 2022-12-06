# Start time: 06:36
# End time: 06:42

import aocd

data = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""
data = """bvwbjplbgvbhsrlpgdmjqwftvncz"""
data = """nppdvjthqldpwncqszvftbrmjlhg"""
data = """nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"""
data = """zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"""

data = aocd.get_data(year=2022, day=6)

for i, char in enumerate(data[4:]):
    if len(set(data[i : i + 4])) == 4:
        print(i + 4)
        break
