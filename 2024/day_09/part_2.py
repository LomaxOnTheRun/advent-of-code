# Start time: 12:43
# End time: 14:19


import aocd

data = """2333133121414131402"""
# data = """23331331214141314021111"""
# data = """12345"""
# data = "1111111111111111111111111111"

data = aocd.get_data(year=2024, day=9)


# def print_blocks(blocks):
#     line = ""
#     for val, size in blocks:
#         val = str(val) if val > -1 else "."
#         line += val * size
#     print(line)


blocks = []
for i, size in enumerate(data):
    if not i % 2:
        blocks.append((int(i // 2), int(size)))
    else:
        blocks.append((-1, int(size)))

# print_blocks(blocks)

i = len(blocks) - 1
while i > 0:
    # if i % 1000 == 0:
    #     print(i)
    move_block_val, move_block_size = blocks[i]
    if move_block_val == -1:
        i -= 1
        continue

    for j in range(len(blocks)):
        block_val, block_size = blocks[j]
        if move_block_val == block_val:
            break

        if block_val != -1:
            continue

        if block_size < move_block_size:
            continue

        blocks[j] = (block_val, block_size - move_block_size)
        blocks.pop(i)
        blocks.insert(j, (move_block_val, move_block_size))
        blocks.insert(i, (-1, move_block_size))
        break

    i -= 1

blocks = [[val] * size for val, size in blocks]
blocks = [x for y in blocks for x in y]
print(sum(i * x for i, x in enumerate(blocks) if x != -1))
