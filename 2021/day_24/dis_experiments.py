import dis


def add_1(ab_dict, a, b):
    ab_dict[a] = ab_dict[a] + b
    return ab_dict


def add_2(ab_dict, a, b):
    ab_dict[a] += b
    return ab_dict


def add_3(ab_dict, a, b):
    ab_dict[a] += b


def add_4(ab_dict, a, b):
    return {ab + b if ab == a else ab for ab in ab_dict}


print("\nadd_1 ---------------------\n")
dis.dis(add_1)
print("\nadd_2 ---------------------\n")
dis.dis(add_2)
print("\nadd_3 ---------------------\n")
dis.dis(add_3)
# print("\nadd_4 ---------------------\n")
# dis.dis(add_4)
