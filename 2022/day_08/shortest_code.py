# 24 lines

import aocd

trees = [[int(num) for num in line] for line in aocd.get_data(year=2022, day=8).split()]

### PART 1 ###

visible = set()

# Tallest trees in that row (i.e. the ones you can see)
tt = lambda row: [max(row[: i + 1]) for i in range(len(row))]

# Left and right
for y, row in enumerate(trees):
    # Left to right
    visible |= {(tt(row).index(height), y) for height in set(tt(row))}
    # Right to left
    visible |= {(len(row) - 1 - tt(row[::-1]).index(h), y) for h in set(tt(row[::-1]))}

# Up and down (trees are transposed)
for x, row in enumerate(zip(*trees)):
    # Top to bottom
    visible |= {(x, tt(row).index(height)) for height in set(tt(row))}
    # Bottom to top
    visible |= {(x, len(row) - 1 - tt(row[::-1]).index(h)) for h in set(tt(row[::-1]))}

print(len(visible))

### PART 2 ###


def score_row(tree_row, base_height):
    # Check if we're on the edge or if no trees are taller than the base
    if not tree_row or max(tree_row) < base_height:
        return len(tree_row)
    # Return distance to first tree that's taller than the base height
    return [tree >= base_height for tree in tree_row].index(True) + 1


best_score = -1
for y in range(len(trees)):
    for x in range(len(trees[0])):
        # Create a list of trees, no matter which way you look, and then corse that row
        right = score_row(trees[y][x + 1 :], trees[y][x])
        left = score_row(trees[y][:x][::-1], trees[y][x])
        down = score_row([*zip(*trees)][x][y + 1 :], trees[y][x])
        up = score_row([*zip(*trees)][x][:y][::-1], trees[y][x])

        # Update best score
        best_score = max(up * left * down * right, best_score)

print(best_score)
