# Code tricks

This is a list of all the tricks I've found (and rememebered to document) to help keep my shortest code as short as possible.

## `split()`

`split()` can be used instead of `split("\n")` if there is one entry per line and no whitespace in each line.

## Get items common in two lists

You can get a set of the values common in both by doing:

`set(list_1) & set(list_2)`

## Divide index by two

`x // 2` can be used instead of `int(x / 2)`.

## Set of iterables

`{*iterable}` can be used instead of `set(iterable)` for an iterable (inc. a string).

## List of iterable

`[*iterable]` can be used instead of `list(iterable)` for an iterable (inc. a string).

## `for` loop

`[do_thing(x) for x in x_list]` if `do_thing` doesn't need to return a value (e.g. is `x` is an object that is updated).

## Add to dict

`my_dict[x] = my_dict.get(x, 0) + y` can be used instead of:

```
if x not in my_dict:
    my_dict[x] = 0
my_dict[x] += y
```

## if / else

`(a, b)[x == y]` can be used instead of `b if x == y else a`.

`"ab"[x == y]` can be used instead of `"b" if x == y else "a"`.

## Transpose a list of list

`[*zip(*original)]` can be used to transpose a list of lists.

## List default

`(my_list + [x])[0]` can be used to get the first item in a list, but default to `x` if the list is empty.

## for / if

`for x in range(y * (z == True)):` or `for x in range(y) if z == True else ():` can be used instead of:

```
if z == True:
    for x in range(y):
```

or:

```
for x in range(y):
    if z == True:
```

## Lists of pairs

For an input of a list of nested pairs that you need to group and also convert to numbers:

```
12-34
56-78
```

You can either loop over them:

```py
pairs = []
for line in data.split():
    left, right = line.split("-")
    pairs.append([int(left), int(right)])
```

or use list comprehentions:

```py
pairs = [[int(left), int(right)] for left, right in [line.split("-") for line in data.split()]]
pairs = [[int(n) for n in parts] for parts in [line.split("-") for line in data.split()]]
```

or break everything out into one long list and zip it together:

```py
data = [int(n) for n in data.replace("-", " ").split()]
pairs = zip(data[::2], data[1::2])
```

This last option allows all of the inner operations (`int(...)` in this example) to only be written once for all values, instead of per value (e.g. `left` and `right`), and avoiding the messy second list comprehention example.

## Walrus operator

You can fit an always true statement in a compound `if` statement to assign a value:

```py
x, y = 0, 0
if (xy := (x, y)) and x == 0:
    # xy now exists as a variable
```

You can even use this new variable later in the same `if` statement:

```py
x, y = 0, 0
if (xy := (x, y)) and xy == (0, 0):
    ...
```
