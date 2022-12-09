#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_09"]

test_input = """2199943210
3987894921
9856789892
8767896789
9899965678""".splitlines()

def read_input(inputs):
    grid = {}
    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            break
        for x, c in enumerate(line):
            grid[x,y] = int(c)
    
    return (grid, (x+1, y+1))

def work(inputs, part2=False):
    grid, (width,height) = read_input(inputs)
    
    def neighbours(x, y):
        nonlocal width, height
        l=[]
        if x != 0:
            l.append((x-1,y))
        if y != 0:
            l.append((x,y-1))
        if x != width - 1:
            l.append((x+1, y))
        if y != height - 1:
            l.append((x,y+1))
        return l
    
    all_low_points = set()
    ret1 = 0
    for (x,y), h in grid.items():
        low_point = True
        for nx, ny in neighbours(x, y):
            if grid[nx,ny] <= h:
                low_point = False
                break
        if low_point:
            all_low_points.add((x,y))
            ret1 += h+1
            
    if not part2:
        return ret1
    
    
    visited = set()
    bassins = {p:{p} for p in all_low_points}
    
    for p in all_low_points:
        to_check = set(p for p in neighbours(*p) if grid[p] < 9)
        visited.add(p)
        while len(to_check) != 0:
            p2 = to_check.pop()
            visited.add(p2)
            bassins[p].add(p2)
            for n in neighbours(*p2):
                if grid[n] < 9 and not n in visited:
                    to_check.add(n)
    
    lens = [len(bassins[p]) for p in bassins]
    lens = list(sorted(lens))
    
    return lens[-1] * lens[-2] * lens[-3]

def test_p1():
    assert(work(test_input) == 15)
test_p1()

def p1():
    print(work(fileinput.input()))
p1()

def test_p2():
    assert(work(test_input, True) == 1134)
test_p2()

def p2():
    print(work(fileinput.input(), True))
p2()
