import aocd, re

example_explosions = [
    ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
    ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
    ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
    ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"),
    ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"),
    ("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[7,[[8,4],9]]],[1,1]]"),
    ("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[15,[0,13]]],[1,1]]"),
    ("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]", "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"),
]

example_splits = [
    ("[[[[0,7],4],[15,[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"),
    ("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"),
]

example_adds = [
    (["[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]"], "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"),
    (["[1,1]", "[2,2]", "[3,3]", "[4,4]"], "[[[[1,1],[2,2]],[3,3]],[4,4]]"),
    (["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]"], "[[[[3,0],[5,3]],[4,4]],[5,5]]"),
    (
        ["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]", "[6,6]"],
        "[[[[5,0],[7,4]],[5,5]],[6,6]]",
    ),
    (
        [
            "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
            "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
            "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
            "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
            "[7,[5,[[3,8],[1,4]]]]",
            "[[2,[2,2]],[8,[8,1]]]",
            "[2,9]",
            "[1,[[[9,3],9],[[9,0],[0,7]]]]",
            "[[[5,[7,4]],7],1]",
            "[[[[4,2],2],6],[8,7]]",
        ],
        "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
    ),
    (
        [
            "[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]",
            "[[[5,[2,8]],4],[5,[[9,9],0]]]",
            "[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]",
            "[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]",
            "[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]",
            "[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]",
            "[[[[5,4],[7,7]],8],[[8,3],8]]",
            "[[9,3],[[9,9],[6,[4,9]]]]",
            "[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]",
            "[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]",
        ],
        "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]",
    ),
]

example_magnitudes = [
    ("[[1,2],[[3,4],5]]", 143),
    ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
    ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
    ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
    ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
    ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
    ("[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]", 4140),
]

data = aocd.get_data(year=2021, day=18)


def explode(num_str):
    # Find first inner number to explode
    depth = 0
    found = False
    for i, c in enumerate(num_str):
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
        elif depth > 4:
            found = True
            break

    if not found:
        return num_str

    # Positions of inner number, inc. brackets
    start = i - 1
    end = start + num_str[start:].index("]") + 1
    left, right = map(int, num_str[start + 1 : end - 1].split(","))

    # Update pre-start string
    pre_start = num_str[:start]
    if prev_num := (re.findall("\d+", pre_start) or [None])[-1]:
        pre_list = pre_start.rsplit(prev_num, 1)
        pre_list.insert(1, str(int(prev_num) + left))
        pre_start = "".join(pre_list)

    # Update post-end string
    post_end = num_str[end:]
    if next_num := (re.findall("\d+", num_str[end:]) or [None])[0]:
        post_list = post_end.split(next_num, 1)
        post_list.insert(1, str(int(next_num) + right))
        post_end = "".join(post_list)

    return pre_start + "0" + post_end


def split(num_str):
    # Find first inner number to split
    match = re.search("\d\d+", num_str)

    if not match:
        return num_str

    # Split value
    num = int(match[0])
    new_num = f"[{int(num / 2)},{num - int(num / 2)}]"

    return num_str.replace(match[0], new_num, 1)


def add(num_str_1, num_str_2):
    num_str = f"[{num_str_1},{num_str_2}]"
    while True:
        # Try to explode
        new_num_str = explode(num_str)
        if new_num_str != num_str:
            num_str = new_num_str
            continue

        # Try to split
        new_num_str = split(num_str)
        if new_num_str != num_str:
            num_str = new_num_str
            continue

        return new_num_str


def sum_list(num_list):
    sum_str = num_list[0]
    for num_str in num_list[1:]:
        sum_str = add(sum_str, num_str)
    return sum_str


def magnitude(num_str: str):
    while True:
        # Find first inner number to split
        match = re.search("\[\d+,\d+\]", num_str)
        if not match:
            break

        left, right = map(int, match[0][1:-1].split(","))
        new_num = str((3 * left) + (2 * right))
        num_str = num_str.replace(match[0], new_num)

    return int(num_str)


# Explode tests
for before, after in example_explosions:
    assert explode(before) == after

# Split tests
for before, after in example_splits:
    assert split(before) == after

# Add tests
for split_data, solution in example_adds:
    assert sum_list(split_data) == solution

# Magnitude tests
for num_str, solution in example_magnitudes:
    assert magnitude(num_str) == solution

print(magnitude(sum_list(data.split("\n"))))
