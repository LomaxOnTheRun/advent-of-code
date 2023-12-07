# Start time: 07:28
# End time: 08:03

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
    if len(hand_dict) == 1 and sorted(hand_dict.values()) == [5]:
        return True

    if "J" not in hand_dict:
        return False

    hand_dict.pop("J")
    if len(hand_dict) == 1:
        return True

    return False


def is_four_of_a_kind(hand_dict: dict[str]) -> bool:
    if len(hand_dict) == 2 and sorted(hand_dict.values()) == [1, 4]:
        return True

    if "J" not in hand_dict:
        return False

    num_jokers = hand_dict.pop("J")
    if max(hand_dict.values()) + num_jokers == 4:
        return True

    # num_jokers = hand_dict.pop("J")
    # if num_jokers == 1 and sorted(hand_dict.values()) == [1, 3]:
    #     return True

    return False


def is_full_house(hand_dict: dict[str]) -> bool:
    if len(hand_dict) == 2 and sorted(hand_dict.values()) == [2, 3]:
        return True

    if "J" not in hand_dict:
        return False

    num_jokers = hand_dict.pop("J")
    if num_jokers == 1 and sorted(hand_dict.values()) == [2, 2]:
        return True
    # 2 jokers will always prioritise a 4 of a kind
    # 3 jokers will always prioritise a 5 of a kind

    return False


def is_three_of_a_kind(hand_dict: dict[str]) -> bool:
    if len(hand_dict) == 3 and sorted(hand_dict.values()) == [1, 1, 3]:
        return True

    if "J" not in hand_dict:
        return False

    num_jokers = hand_dict.pop("J")
    if num_jokers == 1 and sorted(hand_dict.values()) == [1, 1, 2]:
        return True
    if num_jokers == 2 and sorted(hand_dict.values()) == [1, 1, 1]:
        return True
    # 3 jokers will always prioritise a 4 of a kind
    # 4 jokers will always prioritise a 5 of a kind

    return False


def is_two_pair(hand_dict: dict[str]) -> bool:
    # 1 joker will always prioritise a 3 of a kind
    # 2 joker will always prioritise a 4 of a kind
    # 3 joker will always prioritise a 5 of a kind
    return len(hand_dict) == 3 and sorted(hand_dict.values()) == [1, 2, 2]


def is_one_pair(hand_dict: dict[str]) -> bool:
    if len(hand_dict) == 4 and sorted(hand_dict.values()) == [1, 1, 1, 2]:
        return True

    if "J" not in hand_dict:
        return False

    num_jokers = hand_dict.pop("J")
    if num_jokers == 1 and sorted(hand_dict.values()) == [1, 1, 1, 1]:
        return True
    # 2 jokers will always prioritise a 3 of a kind
    # 3 jokers will always prioritise a 4 of a kind
    # 4 jokers will always prioritise a 5 of a kind

    return False


def is_high_card(hand_dict: dict[str]) -> bool:
    # 1 joker will always prioritise a one pair
    return len(hand_dict) == 5 and sorted(hand_dict.values()) == [1, 1, 1, 1, 1]


def get_hand_value(hand_str: str) -> int:
    hand_type_values = {
        is_five_of_a_kind: 7,
        is_four_of_a_kind: 6,
        is_full_house: 5,
        is_three_of_a_kind: 4,
        is_two_pair: 3,
        is_one_pair: 2,
        is_high_card: 1,
    }

    hand_dict = get_hand_dict(hand_str)
    hand_value = 0
    for is_hand_type, hand_type_value in hand_type_values.items():
        if is_hand_type(hand_dict.copy()):
            hand_value = hand_type_value
            break

    if hand_value == 0:
        raise Exception(f"Hand type not found for {hand_str}")

    return hand_value


def sort_hands(hand_bid_str_1: str, hand_bid_str_2: str) -> int:
    """
    Sort hands by hand type, and then by highest early card.

    Return:
        -ve value if h1 < h2
        +ve value if h1 > h2
    """

    hand_str_1 = hand_bid_str_1.split()[0]
    hand_str_2 = hand_bid_str_2.split()[0]

    h1_value = get_hand_value(hand_str_1)
    h2_value = get_hand_value(hand_str_2)

    if h1_value < h2_value:
        return -1
    if h1_value > h2_value:
        return 1

    card_values = "J23456789TQKA"

    for i in range(5):
        card_1 = hand_str_1[i]
        card_2 = hand_str_2[i]
        if card_values.index(card_1) < card_values.index(card_2):
            return -1
        if card_values.index(card_1) > card_values.index(card_2):
            return 1

    raise Exception(f"Hands are equal: {hand_str_1} == {hand_str_2}")


sorted_hands = sorted(data.splitlines(), key=functools.cmp_to_key(sort_hands))

total_bid = 0
for i, hand_bid in enumerate(sorted_hands):
    bid = int(hand_bid.split()[1])
    total_bid += bid * (i + 1)

print(total_bid)
