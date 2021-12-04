import aocd

# data = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

# 22 13 17 11  0
#  8  2 23  4 24
# 21  9 14 16  7
#  6 10  3 18  5
#  1 12 20 15 19

#  3 15  0  2 22
#  9 18 13 17  5
# 19  8  7 25 23
# 20 11 10 24  4
# 14 21 16 12  6

# 14 21 17 24  4
# 10 16 15  9 19
# 18  8 23 26 20
# 22 11 13  6  5
#  2  0 12  3  7"""
# data = data.split("\n\n")

data = aocd.get_data(year=2021, day=4).split("\n\n")

numbers = [int(num) for num in data[0].split(",")]

boards = [board.replace("\n", " ") for board in data[1:]]
boards = [board.strip() for board in boards]
boards = [board.replace("  ", " ") for board in boards]
boards = [[int(num) for num in board.split(" ")] for board in boards]


def check_row(board, i, numbers):
    return all([square in numbers for square in board[5 * i : 5 * (i + 1)]])


def check_col(board, i, numbers):
    return all([square in numbers for square in board[i::5]])


def get_uncalled(board, numbers):
    return [square for square in board if square not in numbers]


win = False
for num_nums in range(len(numbers)):
    nums = numbers[: num_nums + 1]
    for board in boards:
        for i in range(5):
            if check_row(board, i, nums) or check_col(board, i, nums):
                win = True
                break

        if win:
            print(sum(get_uncalled(board, nums)) * nums[-1])
            break

    if win:
        break
