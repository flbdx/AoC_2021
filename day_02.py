#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_02"]

test_input="""forward 5
down 5
forward 8
up 3
down 8
forward 2"""

def work(inputs, part2=False):
    depth = 0
    hpos = 0
    aim = 0
    
    def do_down(x):
        nonlocal aim
        aim += x
    def do_up(x):
        nonlocal aim
        aim -= x
    def do_forward(x):
        nonlocal hpos, depth, aim
        hpos += x
        depth += x * aim
    act = {
        "down": do_down,
        "up" : do_up,
        "forward": do_forward
    }
    
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        direction, v = line.split(" ")
        act[direction](int(v))
    if part2:
        return hpos * depth
    else:
        return hpos * aim

def test_p1():
    assert(work(test_input.splitlines()) == 150)

test_p1()

def p1():
    print(work(fileinput.input()))
p1()

def test_p2():
    assert(work(test_input.splitlines(), True) == 900)

test_p2()

def p2():
    print(work(fileinput.input(), True))
p2()
