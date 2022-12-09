#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re

test_input = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_13"]

def read_input(inputs):
    points = set()
    folds = []
    it = iter(inputs)
    while True:
        line = next(it)
        line = line.strip()
        if len(line) == 0:
            break
        x, y = [int(v) for v in line.split(",")]
        points.add((x,y))

    rgxp = re.compile("fold along ([xy])=([0-9]+)")
    while True:
        line = next(it, None)
        if line == None:
            break
        line = line.strip()
        if len(line) == 0:
            break
        m = rgxp.match(line)
        folds.append((m.group(1), int(m.group(2))))

    return points, folds

def apply_up_fold(points, fold_y):
    res = set()
    for p in points:
        if p[1] < fold_y:
            res.add(p)
        else:
            res.add((p[0], 2 * fold_y - p[1]))
    return res

def apply_left_fold(points, fold_x):
    res = set()
    for p in points:
        if p[0] < fold_x:
            res.add(p)
        else:
            res.add((2 * fold_x - p[0], p[1]))
    return res

def work_p1(inputs):
    points, folds = read_input(inputs)

    for fold in folds:
        points = (apply_left_fold if fold[0] == "x" else apply_up_fold)(points, fold[1])
        break

    return len(points)

def work_p2(inputs):
    points, folds = read_input(inputs)

    for fold in folds:
        points = (apply_left_fold if fold[0] == "x" else apply_up_fold)(points, fold[1])

    for y in range(0, max(p[1] for p in points)+1):
        s = ""
        for x in range(0, max(p[0] for p in points)+1):
            s += "\u25AE" if (x,y) in points else " "
            if ((x+1)%5) == 0: # just to make the text more readable...
                s += " "
        print(s)
    print("")

def test_p1():
    assert(work_p1(test_input) == 17)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    work_p2(test_input)
test_p2()

def p2():
    work_p2(fileinput.input())
p2()
