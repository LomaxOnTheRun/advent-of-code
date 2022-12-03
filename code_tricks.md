# Code tricks

This is a list of all the tricks I've found (and rememebered to document) to help keep my shortest code as short as possible.

## `split()`

`split()` can be used instead of `split("\n")` if there is one entry per line and no whitespace in each line.

## Get items common in two lists

You can get a set of the values common in both by doing:

`set(list_1) & set(list_2)`

## Divide index by two

`x // 2` can be used instead of `int(x / 2)`.

## Set of chars

`{*string}` can be used instead of `set(string)`.
