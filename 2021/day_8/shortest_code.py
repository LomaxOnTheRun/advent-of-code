import aocd

data = aocd.get_data(year=2021, day=8)

data = [line.split(" | ") for line in [line for line in data.split("\n")]]

# Part 1
print(len([n for _, vals in data for n in vals.split(" ") if len(n) in [2, 3, 4, 7]]))


# Part 2
def digits_lengths(ds, ls):
    # Return a list of either:
    # - The set for a digit if there is just one of that length (1, 4, 7, 8)
    # - The intersection of all possible digits for that length (0, 6, 9 and 2, 3, 5)
    return [set.intersection(*[set(d) for d in ds if len(d) == l]) for l in ls]


def get_number(digits, values):
    # Get all digits as sets, or intersections of sets if multiple digits possible
    _1, _4, _7, _8, _069, _235 = digits_lengths(digits.split(" "), [2, 4, 3, 7, 6, 5])
    # Calculate the sets for each currently ambiguous digit (0, 2, 3, 5, 6, 9)
    _0, _2, _6 = (_8 - _235) | _069, (_8 - _069) | _235, _069 | (_8 - _1)
    d_sets = [_0, _1, _2, (_235 | _1), _4, (_069 | _235), _6, _7, _8, (_069 | _4)]
    # Create a map from (frozen) set to string representation of each digit
    digit_map = {frozenset(d_sets[i]): str(i) for i in range(10)}
    # Create number as string, then convert to int
    return int("".join([digit_map[frozenset(value)] for value in values.split(" ")]))


# Print sum of all values
print(sum([get_number(digits, values) for digits, values in data]))
