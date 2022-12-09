#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re

if len(sys.argv) == 1:
    sys.argv += ["input_17"]

test_input = """target area: x=20..30, y=-10..-5"""
real_input = next(fileinput.input())

def read_input(inputs):
    re_int = re.compile("[-]?[0-9]+")
    line = inputs.strip()
    ints = list(map(int, re_int.findall(line)))
    return (ints[0], ints[1], ints[2], ints[3])

class Trajectory(object):
    def __init__(self, vx, vy):
        self.d = complex(vx, vy)
        self.p = 0 + 0j
    
    def __iter__(self):
        return self
    
    def __next__(self):
        self.p += self.d
        self.d -= 1j
        if self.d.real > 0:
            self.d -= 1
        return (self.p.real, self.p.imag)

def work_p1(inputs):
    x_min, x_max, y_min, y_max = read_input(inputs)
    
    # for a vertical velocity vy, the max height is (vy*vy+1) / 2
    #
    # moreover, for a positive vy, the speed when going down and crossing 0 is -vy
    # therefore if -vy > ymin, we overshoot the target in one step
    # so it gives us an upperbound
    def in_area(x, y):
        nonlocal x_min, x_max, y_min, y_max
        return x >= x_min and x <= x_max and y >= y_min and y <= y_max
    
    def overshoot(x, y):
        return x > x_max or y < y_min
    
    # start from our upperbound
    vy = -y_min + 1
    while vy >= y_min:
        for vx in range(1, x_max + 1):
            for p in Trajectory(vx, vy):
                if in_area(*p):
                    return (vy * (vy+1)) // 2
                if overshoot(*p):
                    break
        vy -= 1
    return int(max_height)
    


def work_p2(inputs):
    x_min, x_max, y_min, y_max = read_input(inputs)
    
    def in_area(x, y):
        nonlocal x_min, x_max, y_min, y_max
        return x >= x_min and x <= x_max and y >= y_min and y <= y_max
    
    def overshoot(x, y):
        return x > x_max or y < y_min
    
    vy = y_min
    
    all_init_v = set()
    
    # we are lucky the input values are small. Otherwise we would have to to *Maths*
    while vy < (-y_min + 1):
        for vx in range(1, x_max+1):
            traj_max_height = y_min
            traj = Trajectory(vx, vy)
            for p in traj:
                traj_max_height = max(traj_max_height, p[1])
                if in_area(*p):
                    all_init_v.add((vx, vy))
                    break
                if overshoot(*p):
                    break
        vy += 1
        
    
    return len(all_init_v)

def test_p1():
    assert(work_p1(test_input) == 45)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == 112)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
