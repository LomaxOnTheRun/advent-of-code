# Start time: 06:39
# End time: 07:28

import aocd, functools

data = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

data = aocd.get_data(year=2023, day=7)


def get_hand_dict(hand_str) -> dict[str, int]:
    """
    Build dict of card type to count of that type in the hand.
    """
    hand_dict = {}
    for card in hand_str:
        hand_dict[card] = hand_dict[card] + 1 if card in hand_dict else 1
    return hand_dict


def is_five_of_a_kind(hand_dict: dict[str]) -> bool:
    return len(hand_dict) == 1 and sorted(hand_dict.values()) == [5]


def is_four_of_a_kind(hand_dict: dict[str]) -> bool:
    return len(hand_dict) == 2 and sorted(hand_dict.values()) == [1, 4]


def is_full_house(hand_dict: dict[str]) -> bool:
    return len(hand_dict) == 2 and sorted(hand_dict.values()) == [2, 3]


def is_three_of_a_kind(hand_dict: dict[str]) -> bool:
    return len(hand_dict) == 3 and sorted(hand_dict.values()) == [1, 1, 3]


def is_two_pair(hand_dict: dict[str]) -> bool:
    return len(hand_dict) == 3 and sorted(hand_dict.values()) == [1, 2, 2]


def is_one_pair(hand_dict: dict[str]) -> bool:
    return len(hand_dict) == 4 and sorted(hand_dict.values()) == [1, 1, 1, 2]


def is_high_card(hand_dict: dict[str]) -> bool:
    return len(hand_dict) == 5 and sorted(hand_dict.values()) == [1, 1, 1, 1, 1]


def sort_hands(hand_bid_str_1: str, hand_bid_str_2: str) -> int:
    """
    Sort hands by hand type, and then by highest early card.

    Return:
        -ve value if h1 < h2
        +ve value if h1 > h2
    """

    hand_type_values = {
        is_five_of_a_kind: 7,
        is_four_of_a_kind: 6,
        is_full_house: 5,
        is_three_of_a_kind: 4,
        is_two_pair: 3,
        is_one_pair: 2,
        is_high_card: 1,
    }

    hand_str_1 = hand_bid_str_1.split()[0]
    h1 = get_hand_dict(hand_str_1)
    hand_str_2 = hand_bid_str_2.split()[0]
    h2 = get_hand_dict(hand_str_2)

    h1_value = 0
    for is_hand_type, hand_type_value in hand_type_values.items():
        if is_hand_type(h1):
            h1_value = hand_type_value
            break

    h2_value = 0
    for is_hand_type, hand_type_value in hand_type_values.items():
        if is_hand_type(h2):
            h2_value = hand_type_value
            break

    if h1_value < h2_value:
        return -1
    if h1_value > h2_value:
        return 1

    card_values = "23456789TJQKA"

    for i in range(5):
        card_1 = hand_str_1[i]
        card_2 = hand_str_2[i]
        if card_values.index(card_1) < card_values.index(card_2):
            return -1
        if card_values.index(card_1) > card_values.index(card_2):
            return 1

    raise Exception(f"Hands are equal: {hand_str_1} == {hand_str_2}")


sorted_hands = sorted(data.splitlines(), key=functools.cmp_to_key(sort_hands))
# print(sorted_hands)

total_bid = 0
for i, hand_bid in enumerate(sorted_hands):
    bid = int(hand_bid.split()[1])
    total_bid += bid * (i + 1)

print(total_bid)
