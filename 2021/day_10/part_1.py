# Start time: 7:10am
# End time: 7:23am

import aocd

data = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

data = aocd.get_data(year=2021, day=10)

open_set = "([{<"
close_dict = ")]}>"
pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
score = {")": 3, "]": 57, "}": 1197, ">": 25137}

sum = 0
for line in data.split("\n"):
    current = ""
    for c in line:
        if c in open_set:
            current += c
        elif c == pairs[current[-1]]:
            current = current[:-1]
        else:
            sum += score[c]
            break

print(sum)
