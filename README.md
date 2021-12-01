# Advent of Code

This is a collection of solutions for the [Advent of Code](https://adventofcode.com)
challenges. A mixture of languages have been used for various challenges, and there may
be multiple solutions per challenge (fastest to finish, fewest lines, different languages,
etc.).

The entries are split by year, and all the code for day X is stored in the `day_X`
directory. The input files given for my Github account are all placed in day directories
as `input.txt` (note that users are given different inputs, so your input files may be
different to the ones in this repo).

Finally, each day's challenge is split out into two parts, and each of these parts have
their own solution file.

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
