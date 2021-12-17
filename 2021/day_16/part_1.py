import aocd, typing as t

# data = """D2FE28"""
# data = """38006F45291200"""
# data = """EE00D40C823060"""
# data = """8A004A801A8002F478"""
# data = """620080001611562C8802118E34"""
# data = """C0015000016115A2E0802F182340"""
data = """A0016C880162017C3686B18A3D4780"""

data = aocd.get_data(year=2021, day=16)

# Turn into binary, keeping all leading zeros
data = format(int(data, 16), f"0{4 * len(data)}b")


def get_number_version_and_remainder(data_str: str) -> t.Tuple[int, t.List[int], str]:
    # print("Num: -----------------------")
    # print(data_str)
    version = int(data_str[:3], 2)
    type_id = data_str[3:6]
    if type_id != "100":
        raise Exception("Given number does not have a type of 100")
    data_str = data_str[6:]

    num_str = ""
    while True:
        stop = data_str[0] == "0"
        num_str += data_str[1:5]
        data_str = data_str[5:]
        if stop:
            break

    return int(num_str, 2), [version], data_str


def get_operator_versions_and_remainder(data_str: str) -> t.Tuple[t.List[int], str]:
    # print("Op: -----------------------")
    # print(data_str)
    version = int(data_str[:3], 2)
    type_id = data_str[3:6]
    if type_id == "100":
        raise Exception("Given operator has a type of 100")
    data_str = data_str[6:]

    length_id = data_str[0]
    if length_id == "0":
        length_str = data_str[1:16]
        data_str = data_str[16:]
        subpackets_length = int(length_str, 2)

        data_sub_str = data_str[:subpackets_length]
        remainder = data_str[subpackets_length:]

        # print("subpackets_length:", subpackets_length)

        versions = []
        while data_sub_str.count("1") > 0:
            if data_sub_str[3:6] == "100":
                _, sub_versions, sub_remainder = get_number_version_and_remainder(
                    data_sub_str
                )
                versions += sub_versions
            else:
                sub_versions, sub_remainder = get_operator_versions_and_remainder(
                    data_sub_str
                )
                versions += sub_versions
            data_sub_str = sub_remainder
        return [version] + versions, remainder

    else:
        length_str = data_str[1:12]
        data_str = data_str[12:]
        num_subpackets = int(length_str, 2)

        # print("num_subpackets", num_subpackets)

        versions = []
        for _ in range(num_subpackets):
            if data_str[3:6] == "100":
                _, num_versions, remainder = get_number_version_and_remainder(data_str)
                versions += num_versions
                data_str = remainder
            else:
                op_versions, remainder = get_operator_versions_and_remainder(data_str)
                versions += op_versions
                data_str = remainder

        return [version] + versions, data_str


# print(data)

versions = get_operator_versions_and_remainder(data)[0]
print(sum(versions))
