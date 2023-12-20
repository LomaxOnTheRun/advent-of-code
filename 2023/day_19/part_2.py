# Start time: 16:07
# End time: 17:08

import aocd

data = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

data = aocd.get_data(year=2023, day=19)

rule_lines = data.split("\n\n")[0].splitlines()

rules = {}
for rule_line in rule_lines:
    name, rule_str = rule_line.strip("}").split("{")
    rules[name] = rule_str.split(",")

# Cube: {"x": (mix, max), "m": (min, max), "a": (min, max), "s": (min, max)}
#   - Min and max values are inclusive
# Cubes: [(next_instructions, current_cube)]
cubes = [("in", {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)})]
accepted = []

while rules:
    rule_name, cube = cubes.pop(0)
    rule = rules.pop(rule_name)

    for split in rule[:-1]:
        split, next_rule = split.split(":")
        axis = split[0]
        old_min, old_max = cube[axis]
        if split[1] == "<":
            new_max = int(split[2:]) - 1
            new_lower_cube = cube.copy()
            new_lower_cube[axis] = (old_min, new_max)

            new_min = int(split[2:])
            new_higher_cube = cube.copy()
            new_higher_cube[axis] = (new_min, old_max)

            if next_rule == "A":
                accepted.append((next_rule, new_lower_cube))
            elif next_rule != "R":
                cubes.append((next_rule, new_lower_cube))

            cube = new_higher_cube
        else:
            new_max = int(split[2:])
            new_lower_cube = cube.copy()
            new_lower_cube[axis] = (old_min, new_max)

            new_min = int(split[2:]) + 1
            new_higher_cube = cube.copy()
            new_higher_cube[axis] = (new_min, old_max)

            if next_rule == "A":
                accepted.append((next_rule, new_higher_cube))
            elif next_rule != "R":
                cubes.append((next_rule, new_higher_cube))

            cube = new_lower_cube

    next_rule = rule[-1]
    if next_rule == "A":
        accepted.append((next_rule, cube))
    elif next_rule != "R":
        cubes.append((next_rule, cube))

total = 0
for _, cube in accepted:
    cube_total = 1
    for min_val, max_val in cube.values():
        cube_total *= (max_val - min_val) + 1
    total += cube_total


print(total)
