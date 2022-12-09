#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re

if len(sys.argv) == 1:
    sys.argv += ["input_04"]

test_input="""7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

class Grid:
    def __init__(self, numbers):
        self.all_numbers = []
        self.sets = [set(line) for line in numbers]
        self.sets += [set(numbers[l][c] for l in range(0,5)) for c in range(0, 5)]
        for line in numbers:
            self.all_numbers.extend(line)
    
    # if the grid is a winner for this draw, returns the sum of the unmarked numbers
    # else returns None
    def test_draw(self, draw):
        for s in self.sets:
            if len(s.difference(draw)) == 0:
                return sum([n for n in self.all_numbers if not n in draw])
        return None

def parse_input(inputs):
    re_int = re.compile("[0-9]+")
    line_it = iter(list(inputs))
    
    line = next(line_it)
    draw = [int(n) for n in line.strip().split(",")]
    
    grids = []
    
    try:
        while True:
            numbers = []
            next(line_it)
            for n in range(0, 5):
                numbers.append(list(map(int, re_int.findall(next(line_it)))))
            grids.append(Grid(numbers))
    except StopIteration:
        pass
    
    return (draw, grids)
    

def work_p1(inputs):
    draw, grids = parse_input(inputs)
    
    for n in range(1, len(draw)+1):
        sub_draw = set(draw[0:n])
        for g in grids:
            r= g.test_draw(sub_draw)
            if r != None:
                return r * draw[n-1]

    return None

def work_p2(inputs):
    draw, grids = parse_input(inputs)
    
    grids = set(grids)
    last_winner = None
    for n in range(1, len(draw)+1):
        sub_draw = set(draw[0:n])
        winners = set()
        for g in grids:
            r= g.test_draw(sub_draw)
            if r != None:
                winners.add(g)
                last_winner = (r, draw[n-1])
        grids.difference_update(winners)

    return last_winner[0] * last_winner[1]

def test_p1():
    assert(work_p1(test_input.splitlines()) == 4512)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input.splitlines()) == 1924)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
