#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re

if len(sys.argv) == 1:
    sys.argv += ["input_05"]

test_input="""0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

def parse_input(inputs, part2 = False):
    grid = {}
    re_coords = re.compile("([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)")
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        m = re_coords.match(line)
        x1,y1,x2,y2 = [int(v) for v in m.groups()]
        if x1 == x2 or y1 == y2 or part2:
            a = complex(x1,y1)
            b = complex(x2,y2)
            d = b-a
            d = complex(1 if d.real > 0 else -1 if d.real < 0 else 0, 1 if d.imag > 0 else -1 if d.imag < 0 else 0)
            #d = complex(0 if d.real == 0 else d.real//abs(d.real), 0 if d.imag == 0 else d.imag//abs(d.imag))
            p = a
            while True:
                grid[p.real,p.imag] = grid.setdefault((p.real,p.imag), 0) + 1
                if p == b:
                    break
                p += d
    return grid
    

def work_p1(inputs):
    grid = parse_input(inputs)
    return sum(1 for e in grid.values() if e > 1)

def work_p2(inputs):
    grid = parse_input(inputs, True)
    return sum(1 for e in grid.values() if e > 1)

def test_p1():
    assert(work_p1(test_input.splitlines()) == 5)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input.splitlines()) == 12)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
