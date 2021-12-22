import aocd, itertools as it

# data = """--- scanner 0 ---
# 0,2,0
# 4,1,0
# 3,3,0

# --- scanner 1 ---
# -5,0,1
# -1,-1,1
# -2,1,1"""

# data = """--- scanner 0 ---
# 0,2,0
# 3,3,0

# --- scanner 1 ---
# -5,0,1
# -2,1,1"""

data = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""

data = aocd.get_data(year=2021, day=19)


def scanner_list(data):
    scanners = []
    for scanner_info in data:
        info = scanner_info.split("\n", 1)[1]
        beacons = []
        for coord in info.split("\n"):
            beacons.append(tuple(map(int, coord.split(","))))
        scanners.append(beacons)
    return scanners


def get_pos_negs():
    """All possible combinations of one axis flipped"""
    return list(it.product([-1, 1], repeat=3))


def get_swaps():
    """All possible swaps of axes"""
    return [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]


def apply_pos_neg(scanner, dx, dy, dz):
    return [(x * dx, y * dy, z * dz) for x, y, z in scanner]


def apply_swap(scanner, x, y, z):
    new_scanner = []
    for b in scanner:
        new_scanner.append((b[x], b[y], b[z]))
    return new_scanner


def compare_beacons(all_beacons, scanner_2):
    """Get a list of the beacons for (x, y, z) offsets between points"""
    s1_overlaps = {}
    s2_overlaps = {}
    for b1 in all_beacons:
        for b2 in scanner_2:
            diff = (b2[0] - b1[0], b2[1] - b1[1], b2[2] - b1[2])
            s1_overlaps[diff] = s1_overlaps.get(diff, []) + [b1]
            s2_overlaps[diff] = s2_overlaps.get(diff, []) + [b2]

    best_diff = None
    max_overlaps = 0
    for diff, overlap in s1_overlaps.items():
        if not best_diff or len(overlap) > max_overlaps:
            best_diff = diff
            max_overlaps = len(overlap)

    return max_overlaps, best_diff


def get_overlaps(all_beacons, initial_scanner):
    max_overlap = 0
    matched_scanner = None
    best_diff = None
    best_best_overlap = None

    for pos_neg in get_pos_negs():
        for swap in get_swaps():
            scanner = apply_pos_neg(apply_swap(initial_scanner, *swap), *pos_neg)
            overlap, diff = compare_beacons(all_beacons, scanner)

            if overlap > max_overlap:
                max_overlap = overlap
                matched_scanner = scanner
                best_diff = diff

    return max_overlap, matched_scanner, best_diff


def normalise_scanner(matched_scanner, diff):
    beacons = []
    for beacon in matched_scanner:
        x, y, z = beacon
        dx, dy, dz = diff
        beacons.append((x - dx, y - dy, z - dz))
    return beacons


scanners = scanner_list(data.split("\n\n"))
all_beacons = set(scanners.pop(0))

diffs = [(0, 0, 0)]
while scanners:
    scanner = scanners.pop(0)
    num_overlaps, matched_scanner, diff = get_overlaps(all_beacons, scanner)
    normalised_scanner = normalise_scanner(matched_scanner, diff)
    if num_overlaps >= 12:
        all_beacons = set(list(all_beacons) + normalised_scanner)
        diffs.append(diff)
    else:
        scanners.append(scanner)

max_distance = 0
for s1 in diffs:
    for s2 in diffs:
        distance = abs(s2[0] - s1[0]) + abs(s2[1] - s1[1]) + abs(s2[2] - s1[2])
        max_distance = max(max_distance, distance)

print(max_distance)
