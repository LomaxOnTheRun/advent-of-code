# Advent of Code

This is a collection of solutions for the [Advent of Code](https://adventofcode.com)
challenges. A mixture of languages have been used for various challenges, and there may
be multiple solutions per challenge (fastest to finish, fewest lines, different languages,
etc.).

The entries are split by year, and all the code for day X is stored in the `day_X`
directory. Each day's challenge has two parts, and each of these parts have their own
solution file.

## Python specific notes

### Input

Some of the inputs are manually added, but for many of the Python solutions the
[aocd](https://pypi.org/project/advent-of-code-data/) library is used to automatically
read in the day's data for a Github account.

### Requirements

To install the `aocd` dependency, navigate to the base directory and run:

```bash
pip install -r requirements.txt
```

## How to run the code

### Python

All Python entries use Python 3, so to show any of the solutions just run the following
in a terminal:

```bash
python3 <filename>
```

And the answer should be printed in the terminal.

### C

To compile day X's code into an executable file, navigate to the directory `day_X` and
run:

```bash
# For part 1
gcc -o part_1.out part_1.c

# For part 2
gcc -o part_2.out part_2.c
```

To run an executable file, navigate to the directory `day_X` and run:

```bash
# For part 1
./part_1.c

# For part 2
./part_2.c
```
