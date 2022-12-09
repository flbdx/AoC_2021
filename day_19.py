#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from itertools import combinations, product, permutations
import networkx as nx

test_input="""--- scanner 0 ---
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
30,-46,-14""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_19"]

# print a matrix
def print_mat(m):
    for line in m:
        s = " ".join(repr(c) for c in line)
        print(s)
    print(" ")

# matrix transposition
# returns a tuple
def mat_transpose(m):
    return tuple( tuple(m[y][x] for y in range(len(m))) for x in range(len(m[0])))

# matrix multiplication
# returns a tuple
def mat_mul(m1, m2):
    Y = len(m1)
    X = len(m2[0])
    L = len(m2)
    if len(m2) != len(m1[0]):
        raise Exception
    return tuple( tuple( sum(m1[y][i]*m2[i][x] for i in range(L)) for x in range(X) ) for y in range(Y) )

# 3x3 identity
def id_3x3():
    return ( (1,0,0), (0,1,0), (0,0,1) )

# 3x3 rotations matrix by pi/2 alongs the 3 axis
def rot_0_90():
    return ( (1,0,0), (0,0,-1), (0,1,0) )
def rot_1_90():
    return ( (0,0,1), (0,1,0), (-1,0,0) )
def rot_2_90():
    return ( (0,-1,0), (1,0,0), (0,0,1) )

# generates the 24 rotation matrices for our cubes
def all_24_rotations():
    if all_24_rotations.cache != None:
        return all_24_rotations.cache
    
    
    l = set()
    
    # starting from the identity matrix and doing 4 rotations on the x axis
    m = id_3x3()
    for n in range(4):
        l.add(m)
        m = mat_mul(m, rot_0_90())
    
    # rotation on z, and 4 positions on the y axis
    m = mat_mul(m, rot_2_90())
    for n in range(4):
        l.add(m)
        m = mat_mul(m, rot_1_90())
    
    # rotation on z, and 4 positions on the y axis
    m = mat_mul(m, rot_2_90())
    for n in range(4):
        l.add(m)
        m = mat_mul(m, rot_0_90())
    
    # rotation on z, and 4 positions on the y axis
    m = mat_mul(m, rot_2_90())
    for n in range(4):
        l.add(m)
        m = mat_mul(m, rot_1_90())
    
    # rotation on z, m is now the identity matrix
    #m = mat_mul(m, rot_2_90())
    m = id_3x3()
    
    # rotation on y, and 4 positions on the z axis
    m = mat_mul(m, rot_1_90())
    for n in range(4):
        l.add(m)
        m = mat_mul(m, rot_2_90())
    
    # last position, pi on y, and 4 positions on the z axis
    m = mat_mul(m, rot_1_90())
    m = mat_mul(m, rot_1_90())
    for n in range(4):
        l.add(m)
        m = mat_mul(m, rot_2_90())
    
    all_24_rotations.cache = tuple(l)
    return all_24_rotations.cache

all_24_rotations.cache = None

def read_inputs(inputs):
    scanners = []
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        if "scanner" in line:
            scanners.append([])
        else:
            coords = [int(s) for s in line.split(",")]
            coords = mat_transpose([coords]) # transpose for vector coords
            #print_mat(coords)
            scanners[-1].append(coords)
    return scanners

# (0,0,0) as a vector
def zero_point():
    return ((0,), (0,), (0,))

# apply a rotation on a list of point
def rotate_points(points, rotation):
    return tuple(mat_mul(rotation, p) for p in points)

def point_diff(a, b):
    return tuple( tuple( a[y][x] - b[y][x] for x in range(1) ) for y in range(3) )

# translate a list of point (returns a generator)
def rebase_points(points, t):
    return (tuple( tuple( p[y][x] + t[y][x]  for x in range(1) ) for y in range(3) ) for p in points)

# translate one point
def rebase_point(p, t):
    return tuple( tuple( p[y][x] + t[y][x] for x in range(1) ) for y in range(3) )

# search for all pairs of scanners with a large intersection
# for each pair, store the base vector and rotation to map the coordinates of the second scanner into the first
def build_relations(scanners):
    n_scanners = len(scanners)
    scanner_relative_positions = {}
    
    # for each scan, build a set of vectors between the points of the scan,
    # and precompute all the rotations on those vectors
    vectors = {}
    all_vect_rotations = {}
    for sidx in range(n_scanners):
        scan = scanners[sidx]
        vectors[sidx] = set()
        all_vect_rotations[sidx] = {}
        for p1, p2 in permutations(scan, 2):
            vectors[sidx].add(point_diff(p1, p2))
        for rot in all_24_rotations():
            all_vect_rotations[sidx][rot] = rotate_points(vectors[sidx], rot)
    
    # now for each pair of scans
    for sidx1, sidx2 in combinations(range(n_scanners), 2):
        vects1 = vectors[sidx1]
        vects2 = vectors[sidx2]
        
        pair_is_ok = False
        # we first seach a matching rotation by intersecting the sets of vectors
        for rot, vects2_r in all_vect_rotations[sidx2].items():
            if len(vects1.intersection(vects2_r)) >= 24:
                # we found the rotation
                # still missing the displacement
                # bruteforce on every couple of points
                scan1 = scanners[sidx1]
                sscan1 = set(scan1)
                scan2 = rotate_points(scanners[sidx2], rot)
                for pidx1, pidx2 in product(range(len(scan1)), range(len(scan2))):
                    pdiff = point_diff(scan1[pidx1], scan2[pidx2])
                    n_common = 0
                    for p in rebase_points(scan2, pdiff):
                        if p in sscan1:
                            n_common += 1
                            if n_common == 12:
                                scanner_relative_positions[sidx1, sidx2] = (pdiff, rot)
                                rrot = mat_transpose(rot)
                                scanner_relative_positions[sidx2, sidx1] = (mat_mul(rrot, point_diff(zero_point(), pdiff)), rrot)
                                pair_is_ok = True
                                break
                    if pair_is_ok:
                        break
                break
    return scanner_relative_positions
        

def manhattan(p1, p2):
    return sum(abs(p1[y][0] - p2[y][0]) for y in range(3))

def work_p1_p2(inputs):
    scanners = read_inputs(inputs)
    n_scanners = len(scanners)
    
    scanner_relative_positions = build_relations(scanners)
    #print(scanner_relative_positions)
    
    G = nx.Graph()
    for rel in scanner_relative_positions.keys():
        G.add_edge(*rel)

    all_beacons = set(scanners[0])
    for sidx in range(1, n_scanners):
        path = nx.shortest_path(G, sidx, 0)
        base = sidx
        scan = scanners[sidx]
        for i in range(1, len(path)):
            pdiff, rot = scanner_relative_positions[path[i], base]
            scan = rotate_points(scan, rot)
            scan = list(rebase_points(scan, pdiff))
            base = path[i]
        all_beacons.update(scan)
    res_p1 = len(all_beacons)
    
    positions_rel_to_0 = {0: zero_point()}
    
    for sidx in range(1, n_scanners):
        path = nx.shortest_path(G, sidx, 0)
        base = sidx
        p = zero_point()
        for i in range(1, len(path)):
            pdiff, rot = scanner_relative_positions[path[i], base]
            p = mat_mul(rot, p)
            p = rebase_point(p, pdiff)
            base = path[i]
        positions_rel_to_0[sidx] = p
    
    res_p2 = max(manhattan(positions_rel_to_0[p1], positions_rel_to_0[p2]) for p1, p2 in combinations(range(n_scanners), 2))
    
    return res_p1, res_p2

def test():
    assert(work_p1_p2(test_input) == (79, 3621))
test()

def work():
    print(work_p1_p2(fileinput.input()))
work()
