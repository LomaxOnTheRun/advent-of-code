# Start time: 7:23am
# End time: 7:35am

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

corrupt_values = {")": 3, "]": 57, "}": 1197, ">": 25137}
incomplete_values = {"(": 1, "[": 2, "{": 3, "<": 4}

corrupt_score = 0
incomplete_scores = []
for line in data.split("\n"):
    current = ""
    corrupt = False
    for c in line:
        if c in open_set:
            current += c
        elif c == pairs[current[-1]]:
            current = current[:-1]
        else:
            corrupt_score += corrupt_values[c]
            corrupt = True
            break
    if corrupt:
        continue

    incomplete_score = 0
    for c in current[::-1]:
        incomplete_score = (incomplete_score * 5) + incomplete_values[c]
    incomplete_scores.append(incomplete_score)


print(sorted(incomplete_scores)[int(len(incomplete_scores) / 2)])
