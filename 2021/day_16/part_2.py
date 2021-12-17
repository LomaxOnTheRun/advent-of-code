import aocd, math, typing as t


test_data = [
    # Part 1 examples
    # "38006F45291200",
    # "EE00D40C823060",
    # "8A004A801A8002F478",
    # "620080001611562C8802118E34",
    # "C0015000016115A2E0802F182340",
    # "A0016C880162017C3686B18A3D4780",
    # # Part 2 examples
    # "C200B40A82",
    # "04005AC33890",
    # "880086C3E88112",
    # "CE00C43D881120",
    # "D8005AC2A8F0",
    # "F600BC2D8F",
    # "9C005AC2F8F0",
    # "9C0141080250320F1802104A08",
    # # My examples
    # "9e009080250320f1802104a080",  # Mine, should be 1 because (1+3)==(2*2)
]

data = aocd.get_data(year=2021, day=16)


def pretty_number(data_str: str) -> str:
    pretty_str = "---NUM|"
    i = 6
    while data_str[i] == "1":
        pretty_str += f"1({data_str[i+1:i+5]})"
        i += 5
    pretty_str += f"0({data_str[i+1:i+5]})"
    if len(data_str) >= i + 5:
        pretty_str += "..."

    data_str = data_str[6:]
    value_str = ""
    while True:
        stop = data_str[0] == "0"
        value_str += data_str[1:5]
        data_str = data_str[5:]
        if stop:
            break
    pretty_str += f" ({int(value_str, 2)})"

    return pretty_str


def pretty_op(data_str: str) -> str:
    pretty_str = f"---OP{int(data_str[3:6], 2)}|"
    pretty_str += f"{data_str[6]}:"
    if data_str[6] == "0":
        length = int(data_str[7:22], 2)
        pretty_str += f"{data_str[7:22]}({length})"
    else:
        length = int(data_str[7:18], 2)
        pretty_str += f"{data_str[7:18]}({length})"
    pretty_str += "..."
    return pretty_str


def pretty(data_str: str) -> str:
    if data_str[3:6] == "100":
        print(pretty_number(data_str))
    else:
        print(pretty_op(data_str))


def apply_op(type_id: str, values: t.List[int]) -> int:
    # print(type_id, values)
    if type_id == "000":
        return sum(values)
    if type_id == "001":
        return math.prod(values)
    if type_id == "010":
        return min(values)
    if type_id == "011":
        return max(values)
    if type_id == "101":
        return int(values[0] > values[1])
    if type_id == "110":
        return int(values[0] < values[1])
    if type_id == "111":
        return int(values[0] == values[1])


def get_value_and_remainder(data_str: str) -> t.Tuple[int, str]:
    # print("Num: -----------------------")
    # print(data_str[:70], "..." if len(data_str) > 70 else "")
    # pretty(data_str)

    type_id = data_str[3:6]
    if type_id != "100":
        raise Exception("Given number does not have a type of 100")

    data_str = data_str[6:]
    value_str = ""
    while True:
        stop = data_str[0] == "0"
        value_str += data_str[1:5]
        data_str = data_str[5:]
        if stop:
            return int(value_str, 2), data_str


def get_ops_value_and_remainder(data_str: str) -> t.Tuple[int, str]:
    # print("Op: -----------------------")
    # print(data_str[:70], "..." if len(data_str) > 70 else "")
    # pretty(data_str)

    type_id = data_str[3:6]
    if type_id == "100":
        raise Exception("Given operator has a type of 100")

    data_str = data_str[6:]
    # print("type_id", int(type_id, 2))

    values = []
    length_id = data_str[0]
    if length_id == "0":
        # print("length_id", length_id)
        length_str = data_str[1:16]
        data_str = data_str[16:]
        subpackets_length = int(length_str, 2)

        if subpackets_length > len(data_str):
            raise Exception("Subpacket length is longer than remaining data")

        data_sub_str = data_str[:subpackets_length]
        # data_sub_str = data_str
        remainder = data_str[subpackets_length:]

        # print("remainder 1", remainder[:50])

        # print("subpackets_length:", subpackets_length)

        while data_sub_str.count("1") > 0:
            if data_sub_str[3:6] == "100":
                value, data_sub_str = get_value_and_remainder(data_sub_str)
            else:
                value, data_sub_str = get_ops_value_and_remainder(data_sub_str)
            values.append(value)

        # print("remainder 2", remainder[:50])
        # remainder = data_sub_str

    else:
        # print("length_id", length_id, "<*******************************")
        length_str = data_str[1:12]
        data_str = data_str[12:]
        num_subpackets = int(length_str, 2)

        # print("num_subpackets", num_subpackets)

        data_sub_str = data_str

        for _ in range(num_subpackets):
            if data_sub_str[3:6] == "100":
                value, data_sub_str = get_value_and_remainder(data_sub_str)
            else:
                value, data_sub_str = get_ops_value_and_remainder(data_sub_str)
            values.append(value)
        remainder = data_sub_str

        # print("remainder 3", remainder[:50])

    value = apply_op(type_id, values)
    # print(type_id, values, value)

    return value, remainder


for td in test_data:
    print(f"\nNEW TEST DATA: {td}")
    # Turn into binary, keeping all leading zeros
    td = format(int(td, 16), f"0{4 * len(td)}b")
    print(get_ops_value_and_remainder(td)[0])

data = format(int(data, 16), f"0{4 * len(data)}b")
# print("Total length:", len(data))
print(get_ops_value_and_remainder(data)[0])
