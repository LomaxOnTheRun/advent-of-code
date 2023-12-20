# Start time: 18:15
# End time: 18:39

import aocd

data = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

data = aocd.get_data(year=2023, day=15)


def get_hash(word: str) -> int:
    value = 0
    for char in word:
        value = ((value + ord(char)) * 17) % 256
    return value


boxes = {i: [] for i in range(256)}  # {box_id: [(lens_name, focal_length)]}
for instruction in data.split(","):
    lens_name = instruction.split("=")[0].split("-")[0]
    box_id = get_hash(lens_name)

    if instruction[-1] == "-":
        boxes[box_id] = [(ln, fl) for ln, fl in boxes[box_id] if ln != lens_name]
        continue

    focal_length = int(instruction.split("=")[1])
    new_box_lenses = []
    lens_changed = False
    for ln, fl in boxes[box_id]:
        if ln != lens_name:
            new_box_lenses.append((ln, fl))
        else:
            new_box_lenses.append((ln, focal_length))
            lens_changed = True

    if lens_changed:
        boxes[box_id] = new_box_lenses
    else:
        boxes[box_id].append((lens_name, focal_length))

total = 0
for box_id, lenses in boxes.items():
    for lens_position, (_, focal_length) in enumerate(lenses):
        total += (box_id + 1) * (lens_position + 1) * focal_length
print(total)
