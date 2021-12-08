# Start time 1: 6:23am
# End time 1: 6:48am
# Start time 2: 8:17am
# End time 2: 8:27am

import aocd

data = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

data = aocd.get_data(year=2021, day=8)

data = [line.split(" | ") for line in [line for line in data.split("\n") if line]]


def get_digits_of_length(digits, length):
    return [digit for digit in digits if len(digit) == length]


def get_diff(big_digit, small_digit):
    return [char for char in big_digit if char not in small_digit]


def get_digit_map(digits: list):
    one = get_digits_of_length(digits, 2)[0]
    four = get_digits_of_length(digits, 4)[0]
    seven = get_digits_of_length(digits, 3)[0]
    eight = get_digits_of_length(digits, 7)[0]
    zero_six_nine = get_digits_of_length(digits, 6)
    two_three_five = get_digits_of_length(digits, 5)

    for num in zero_six_nine:
        if len(get_diff(num, four + seven)) == 1:
            nine = num
        elif len(get_diff(num, one)) == 4:
            zero = num
        else:
            six = num

    for num in two_three_five:
        if len(get_diff(num, one)) == 3:
            three = num
        elif len(get_diff(num, four)) == 3:
            two = num
        else:
            five = num

    return {
        "".join(sorted(zero)): "0",
        "".join(sorted(one)): "1",
        "".join(sorted(two)): "2",
        "".join(sorted(three)): "3",
        "".join(sorted(four)): "4",
        "".join(sorted(five)): "5",
        "".join(sorted(six)): "6",
        "".join(sorted(seven)): "7",
        "".join(sorted(eight)): "8",
        "".join(sorted(nine)): "9",
    }


sum = 0
for digits, values in data:
    digit_map = get_digit_map(digits.split(" "))
    sum += int(
        "".join([digit_map["".join(sorted(value))] for value in values.split(" ")])
    )

print(sum)
