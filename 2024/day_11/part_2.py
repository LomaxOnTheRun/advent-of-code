import aocd

data = """125 17"""

data = aocd.get_data(year=2024, day=11)


# {
#     stone: {
#         depth: [stones]
#     }
# }
SEEN: dict[str, dict[int, list[str]]] = {}

# {
#     stone {
#         depth: num_stones
#     }
# }
SEEN_NUM: dict[str, dict[int, int]] = {}


def get_seen(
    stone: str, current_depth: int, max_depth: int
) -> tuple[int, list[str]] | tuple[None, None]:
    dd = max_depth - current_depth
    if stone not in SEEN:
        return None, None

    seen_stone = SEEN[stone]
    for depth in range(dd, 0, -1):
        if depth in seen_stone:
            return current_depth + depth, seen_stone[depth]
    return None, None


def get_seen_num(stone: str, current_depth: int, max_depth: int) -> int | None:
    if stone not in SEEN_NUM:
        return None
    return SEEN_NUM[stone].get(max_depth - current_depth)


def get_num_next_stones(stone: str, current_depth: int, max_depth: int) -> int:
    # Check if next stones already seen
    next_depth, next_stones = get_seen(stone, current_depth, max_depth)
    if seen_num := get_seen_num(stone, current_depth, max_depth):
        return seen_num

    # Otherwise calculate next stones
    if not next_stones:
        next_stones: list[str]
        if stone == "0":
            next_stones = ["1"]
        elif (len_stone := len(stone)) % 2 == 0:
            left, right = stone[: len_stone // 2], stone[len_stone // 2 :]
            left, right = left.lstrip("0"), right.lstrip("0")
            next_stones = [left if left else "0", right if right else "0"]
        else:
            next_stones = [str(int(stone) * 2024)]

        # Add to dict
        if stone not in SEEN:
            SEEN[stone] = {}
        SEEN[stone][1] = next_stones

        next_depth = current_depth + 1

    # If max_depth reached
    if next_depth == max_depth:
        if stone not in SEEN_NUM:
            SEEN_NUM[stone] = {}
        SEEN_NUM[stone][max_depth - current_depth] = len(next_stones)
        return len(next_stones)

    # Build up number of final stones
    num_stones = 0
    for next_stone in next_stones:
        num_next_stones = get_num_next_stones(next_stone, next_depth, max_depth)
        num_stones += num_next_stones

    if stone not in SEEN_NUM:
        SEEN_NUM[stone] = {}
    SEEN_NUM[stone][max_depth - current_depth] = num_stones

    return num_stones


stones = data.split()
num_blinks = 75

total_num_stones = 0
for stone in data.split():
    total_num_stones += get_num_next_stones(stone, 0, num_blinks)
print(total_num_stones)
