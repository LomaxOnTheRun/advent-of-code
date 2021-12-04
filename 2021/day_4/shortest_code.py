import aocd, re

data = aocd.get_data(year=2021, day=4).split("\n\n")

all_numbers = [int(num) for num in data[0].split(",")]
boards = [[int(num) for num in re.split(r"[\n ]", board) if num] for board in data[1:]]

is_full = lambda row_or_col, numbers: all([square in numbers for square in row_or_col])
lines = lambda board: [(board[5 * i : 5 * (i + 1)], board[i::5]) for i in range(5)]

wins = {str(board): False for board in boards}
for nums in [all_numbers[:i] for i in range(1, len(all_numbers) + 1)]:
    for board in boards:
        for row, col in lines(board):
            if is_full(row, nums) or is_full(col, nums):
                # Part 1
                if all([not win for win in wins.values()]):
                    print(sum([sqr for sqr in board if sqr not in nums]) * nums[-1])
                # Part 2
                wins[str(board)] = True
                if all(wins.values()):
                    print(sum([sqr for sqr in board if sqr not in nums]) * nums[-1])
                    exit()
