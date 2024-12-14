import aocd, collections


def calc_stones(stone: str) -> list[str]:
    if (half_length := len(stone) // 2) == len(stone) / 2:
        return [str(int(stone[:half_length])), str(int(stone[half_length:]))]
    return ["1"] if stone == "0" else [str(int(stone) * 2024)]


def end_stones(stone: str, max_depth: int, depth: int = 0) -> int:
    # Early exit if we already know the number of final stones
    if seen_num := SEEN_NUM[stone].get(max_depth - depth):
        return seen_num

    # If max_depth reached, return number of next stones
    if depth + 1 == max_depth:
        return len(calc_stones(stone))

    # Build up number of final stones
    num_stones = sum(end_stones(ns, max_depth, depth + 1) for ns in calc_stones(stone))

    # Add to dict
    SEEN_NUM[stone][max_depth - depth] = num_stones

    return num_stones


SEEN_NUM = collections.defaultdict(dict)
for i in (25, 75):
    print(sum(end_stones(s, i) for s in aocd.get_data(year=2024, day=11).split()))
