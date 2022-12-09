#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>""".splitlines()

def read_input(inputs):
    east_facing = set()
    south_facing = set()
    for y, line in enumerate(inputs):
        line = line.strip()
        for x, c in enumerate(line):
            if c == '>':
                east_facing.add((x, y))
            elif c == 'v':
                south_facing.add((x,y))
    return (east_facing, south_facing, x+1, y+1)

if len(sys.argv) == 1:
    sys.argv += ["input_25"]

def work(inputs):
    east_facing, south_facing, width, height = read_input(inputs)
    
    steps = 1
    while True:
        ne = set()
        ns = set()
        
        for sc in east_facing:
            next_pos = ((sc[0]+1) % width, sc[1])
            if next_pos in east_facing or next_pos in south_facing:
                ne.add(sc)
            else:
                ne.add(next_pos)
        
        for sc in south_facing:
            next_pos = (sc[0], (sc[1]+1) % height)
            if next_pos in ne or next_pos in south_facing:
                ns.add(sc)
            else:
                ns.add(next_pos)
        
        if east_facing == ne and south_facing == ns:
            return steps
        
        east_facing = ne
        south_facing = ns
        
        steps += 1

def test_p1():
    assert(work(test_input) == 58)
test_p1()

def p1():
    print(work(fileinput.input()))
p1()

