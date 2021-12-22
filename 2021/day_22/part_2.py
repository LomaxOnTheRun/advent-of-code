import aocd

data = """on x=10..12,y=10..12,z=10..12"""
# 27

data = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13"""
# 46

data = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11"""
# 38

data = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10"""
# 39

data = """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29"""
# 474140

data = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15"""
# 590784

data = """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507"""
# 2758514936282235

data = aocd.get_data(year=2021, day=22)


example_splits = [
    # 1x1 cube in centre of 3x3 cube
    (
        # Outer cube
        ((0, 2), (0, 2), (0, 2)),
        # Inner cube
        ((1, 1), (1, 1), (1, 1)),
        [  # Corners
            ((0, 0), (0, 0), (0, 0)),
            ((0, 0), (0, 0), (2, 2)),
            ((0, 0), (2, 2), (0, 0)),
            ((0, 0), (2, 2), (2, 2)),
            ((2, 2), (0, 0), (0, 0)),
            ((2, 2), (0, 0), (2, 2)),
            ((2, 2), (2, 2), (0, 0)),
            ((2, 2), (2, 2), (2, 2)),
        ],
        [  # Faces
            ((0, 0), (1, 1), (1, 1)),
            ((2, 2), (1, 1), (1, 1)),
            ((1, 1), (0, 0), (1, 1)),
            ((1, 1), (2, 2), (1, 1)),
            ((1, 1), (1, 1), (0, 0)),
            ((1, 1), (1, 1), (2, 2)),
        ],
        [  # Edges
            ((0, 0), (0, 0), (1, 1)),
            ((0, 0), (2, 2), (1, 1)),
            ((0, 0), (1, 1), (0, 0)),
            ((0, 0), (1, 1), (2, 2)),
            ((1, 1), (0, 0), (0, 0)),
            ((1, 1), (0, 0), (2, 2)),
            ((1, 1), (2, 2), (0, 0)),
            ((1, 1), (2, 2), (2, 2)),
            ((2, 2), (0, 0), (1, 1)),
            ((2, 2), (2, 2), (1, 1)),
            ((2, 2), (1, 1), (0, 0)),
            ((2, 2), (1, 1), (2, 2)),
        ],
        # Other
        [],
    ),
    # 1x1 cube in centre of 5x5 cube
    (
        # Outer cube
        ((0, 4), (0, 4), (0, 4)),
        # Inner cube
        ((2, 2), (2, 2), (2, 2)),
        [  # Corners
            ((0, 1), (0, 1), (0, 1)),
            ((0, 1), (0, 1), (3, 4)),
            ((0, 1), (3, 4), (0, 1)),
            ((0, 1), (3, 4), (3, 4)),
            ((3, 4), (0, 1), (0, 1)),
            ((3, 4), (0, 1), (3, 4)),
            ((3, 4), (3, 4), (0, 1)),
            ((3, 4), (3, 4), (3, 4)),
        ],
        [  # Faces
            ((0, 1), (2, 2), (2, 2)),
            ((3, 4), (2, 2), (2, 2)),
            ((2, 2), (0, 1), (2, 2)),
            ((2, 2), (3, 4), (2, 2)),
            ((2, 2), (2, 2), (0, 1)),
            ((2, 2), (2, 2), (3, 4)),
        ],
        [  # Edges
            ((0, 1), (0, 1), (2, 2)),
            ((0, 1), (3, 4), (2, 2)),
            ((0, 1), (2, 2), (0, 1)),
            ((0, 1), (2, 2), (3, 4)),
            ((2, 2), (0, 1), (0, 1)),
            ((2, 2), (0, 1), (3, 4)),
            ((2, 2), (3, 4), (0, 1)),
            ((2, 2), (3, 4), (3, 4)),
            ((3, 4), (0, 1), (2, 2)),
            ((3, 4), (3, 4), (2, 2)),
            ((3, 4), (2, 2), (0, 1)),
            ((3, 4), (2, 2), (3, 4)),
        ],
        # Other
        [],
    ),
    # 5x5 cube to right of 3x3 cube
    (
        # First cube
        ((0, 2), (0, 2), (0, 2)),
        # Second cube
        ((2, 6), (-1, 3), (-1, 3)),
        # Corners
        [],
        # Faces
        [((0, 1), (0, 2), (0, 2))],
        # Edges
        [],
        # Other
        [],
    ),
    # Two 3x3 cubes that aren't touching
    (
        # First cube
        ((0, 2), (0, 2), (0, 2)),
        # Second cube
        ((10, 2), (10, 2), (10, 2)),
        # Corners
        [],
        # Faces
        [],
        # Edges
        [],
        # Other
        [((0, 2), (0, 2), (0, 2))],
    ),
    # Two 3x3 cubes that are overlapping a corner
    (
        # First cube
        ((0, 2), (0, 2), (0, 2)),
        # Second cube
        ((-2, 0), (-2, 0), (-2, 0)),
        # Corners
        [
            ((1, 2), (1, 2), (1, 2)),
        ],
        # Faces
        [
            ((1, 2), (0, 0), (0, 0)),
            ((0, 0), (1, 2), (0, 0)),
            ((0, 0), (0, 0), (1, 2)),
        ],
        # Edges
        [
            ((0, 0), (1, 2), (1, 2)),
            ((1, 2), (0, 0), (1, 2)),
            ((1, 2), (1, 2), (0, 0)),
        ],
        # Other
        [],
    ),
]

example_counts = [
    ([((0, 0), (0, 0), (0, 0))], 1),
    ([((-1, 10), (0, 0), (4, 5))], 24),
]


def is_valid(coord):
    return coord[0] <= coord[1]


def split_cube(cube, new_cube):
    """Split a cube into sections which don't overlap the new cube"""
    (cx1, cx2), (cy1, cy2), (cz1, cz2) = cube
    (nx1, nx2), (ny1, ny2), (nz1, nz2) = new_cube

    # Return whole cube if not overlapping
    if any([cx2 < nx1, cx1 > nx2, cy2 < ny1, cy1 > ny2, cz2 < nz1, cz1 > nz2]):
        return [], [], [], [cube]

    # Inner cube measurements
    nx = (max(cx1, nx1), min(cx2, nx2))
    ny = (max(cy1, ny1), min(cy2, ny2))
    nz = (max(cz1, nz1), min(cz2, nz2))

    # Inter-cube measurements
    pre_x = (cx1, nx1 - 1)
    pre_y = (cy1, ny1 - 1)
    pre_z = (cz1, nz1 - 1)
    post_x = (nx2 + 1, cx2)
    post_y = (ny2 + 1, cy2)
    post_z = (nz2 + 1, cz2)

    # Calculate corners
    corners = []
    for dx in [0, 1]:
        cn_x = pre_x if dx == 0 else post_x
        if not is_valid(cn_x):
            continue
        for dy in [0, 1]:
            cn_y = pre_y if dy == 0 else post_y
            if not is_valid(cn_y):
                continue
            for dz in [0, 1]:
                cn_z = pre_z if dz == 0 else post_z
                if not is_valid(cn_z):
                    continue
                corners.append((cn_x, cn_y, cn_z))

    # Calculate faces
    faces = []
    for dx in [0, 1]:
        f_x = pre_x if dx == 0 else post_x
        if is_valid(f_x):
            faces.append((f_x, ny, nz))
    for dy in [0, 1]:
        f_y = pre_y if dy == 0 else post_y
        if is_valid(f_y):
            faces.append((nx, f_y, nz))
    for dz in [0, 1]:
        f_z = pre_z if dz == 0 else post_z
        if is_valid(f_z):
            faces.append((nx, ny, f_z))

    # Calculate edges
    edges = []
    for e_y, e_z in [(pre_y, nz), (post_y, nz), (ny, pre_z), (ny, post_z)]:
        if is_valid(pre_x) and is_valid(e_y) and is_valid(e_z):
            edges.append((pre_x, e_y, e_z))
    for e_y, e_z in [
        (pre_y, pre_z),
        (pre_y, post_z),
        (post_y, pre_z),
        (post_y, post_z),
    ]:
        if is_valid(e_y) and is_valid(e_z):
            edges.append((nx, e_y, e_z))
    for e_y, e_z in [(pre_y, nz), (post_y, nz), (ny, pre_z), (ny, post_z)]:
        if is_valid(post_x) and is_valid(e_y) and is_valid(e_z):
            edges.append((post_x, e_y, e_z))

    return corners, faces, edges, []


for i, example in enumerate(example_splits):
    # print(i)
    cube, inner_cube, ex_corners, ex_faces, ex_edges, ex_other = example
    corners, faces, edges, other = split_cube(cube, inner_cube)
    assert set(corners) == set(ex_corners)
    assert set(faces) == set(ex_faces)
    assert set(edges) == set(ex_edges)
    assert set(other) == set(ex_other)


def split_cubes(cubes, new_cube, add_new_cube=False):
    """Split all existing cubes to make way for new cube"""
    new_cubes = []
    for cube in cubes:
        corners, faces, edges, other = split_cube(cube, new_cube)
        new_cubes += corners
        new_cubes += faces
        new_cubes += edges
        new_cubes += other

    if add_new_cube:
        new_cubes.append(new_cube)

    return new_cubes


def count(cubes):
    """Count the total number of squares in all of the cubes"""
    total = 0
    for (x1, x2), (y1, y2), (z1, z2) in cubes:
        total += ((x2 + 1) - x1) * ((y2 + 1) - y1) * ((z2 + 1) - z1)
    return total


for cubes, total in example_counts:
    assert count(cubes) == total


# Clean data
data = [line.split(" ") for line in data.split("\n")]
for line in data:
    line[1] = [coord[2:] for coord in line[1].split(",")]
    line[1] = [tuple(map(int, coord.split(".."))) for coord in line[1]]

# Go through all cubes
on_cubes = []
for on_off, new_cube in data:
    add_new_cube = on_off == "on"
    on_cubes = split_cubes(on_cubes, new_cube, add_new_cube)

print(count(on_cubes))
