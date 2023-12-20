# Start time: 14:42
# End time: 16:07

import aocd, re

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


def get_next_rule_set(input_dict, rule_set) -> str:
    x, m, a, s = input_dict["x"], input_dict["m"], input_dict["a"], input_dict["s"]
    for rule in rule_set:
        output = rule(x, m, a, s)
        if output is None:
            continue
        return output


rules_lines, inputs_str = data.split("\n\n")

rule_sets = {}
for rule_line in rules_lines.split():
    rule_line = re.sub(",(\w+)}", r",True:\1}", rule_line)
    name, rule_dict_str = rule_line.strip("}").split("{")
    rules = []
    for rule_str in rule_dict_str.split(","):
        condition, output = rule_str.split(":")
        rules.append(eval(f"lambda x, m, a, s: '{output}' if {condition} else None"))
    rule_sets[name] = rules

input_dicts = []
for input_str in inputs_str.split():
    input_dicts.append(eval(re.sub("([xmas])=", r'"\1":', input_str)))

accepted = []
for input_dict in input_dicts:
    # print(input_dict)
    next_rule_set = "in"
    while next_rule_set not in ("A", "R"):
        # print(next_rule_set)
        rule_set = rule_sets[next_rule_set]
        next_rule_set = get_next_rule_set(input_dict, rule_set)

    if next_rule_set == "A":
        accepted.append(input_dict)

# print(accepted)
print(sum(sum(vals for vals in a.values()) for a in accepted))
