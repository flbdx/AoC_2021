#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_11"]

def read_input(inputs):
    grid = {}
    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            break
        for x, c in enumerate(line):
            grid[x,y] = int(c)
    return grid

def adjacents(x, y):
    return [(x+ox,y+oy) for ox,oy in ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)) if x+ox >= 0 and y+oy >= 0 and x+ox < 10 and y+oy < 10]

def work(inputs, steps=100, part2=False):
    grid = read_input(inputs)
    
    total_flashs = 0
    
    s = 0
    while part2 or s < steps:
        grid = {p:grid[p]+1 for p in grid}
        to_check = list(grid.keys())
        flashed = set()
        while len(to_check) > 0:
            p = to_check.pop()
            if grid[p] > 9 and not p in flashed:
                flashed.add(p)
                for adj in adjacents(*p):
                    to_check.append(adj)
                    grid[adj] += 1
        for p in flashed:
            grid[p] = 0
        
        if part2 and len(flashed) == 100:
            return s + 1
        
        total_flashs += len(flashed)
        s += 1

        #print("step " + repr(s+1))
        #for y in range(0, 10):
            #print("".join(repr(grid[x,y]) for x in range(0, 10)))
        #print("")
            
    return total_flashs

def test_p1():
    assert(work(test_input, steps=100) == 1656)
test_p1()

def p1():
    print(work(fileinput.input(), steps=100))
p1()

def test_p2():
    assert(work(test_input, part2=True) == 195)
test_p2()

def p2():
    print(work(fileinput.input(), part2=True))
p2()
