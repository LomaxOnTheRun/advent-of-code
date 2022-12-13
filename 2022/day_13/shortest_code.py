# 13 lines

import aocd, functools


# Return values match Python sort values (-1, 0, 1)
def compare(left, right):
    # Int comparison
    if type(left) == type(right) == int:
        return left - right

    # List comparison
    if type(left) == type(right) == list:
        # Create a list of all items that are different, and the difference order
        outcomes = [compare(*sides) for sides in zip(left, right) if compare(*sides)]
        # Return the order of the first difference...
        # ... or return the difference of list lengths
        return (outcomes + [0])[0] or len(left) - len(right)

    # If one side is an int and the other a list, wrap the int and do the comparison again
    return compare([left], right) if type(left) == int else compare(left, [right])


# Convert string input into list of lists
packets = [eval(packet) for packet in aocd.get_data(year=2022, day=13).split()]

# Part 1

# Build dict of indices and outcomes (i.e. if they are in the correct order)
outcomes = {i: compare(*packets[i * 2 : (i + 1) * 2]) for i in range(len(packets) // 2)}
# Print sum of indices of all pairs that are in the correct order
print(sum([i + 1 for i in outcomes if outcomes[i] < 0]))

# Part 2

# Add decoder keys and use `sorted` to arrange entire list
pairs = sorted(packets + [[[2]], [[6]]], key=functools.cmp_to_key(compare))
# Print product of indices of decoder keys
print((pairs.index([[2]]) + 1) * (pairs.index([[6]]) + 1))
