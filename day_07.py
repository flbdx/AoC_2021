#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_07"]

test_input = """16,1,2,0,4,2,7,1,2,14"""
real_input = next(fileinput.input())

def work(inputs, part2=False):
    crabs = [int(v) for v in inputs.strip().split(',')]
    min_x = min(crabs)
    max_x = max(crabs)

    best_fuel = None
    best_pos = None
    
    if not part2:
        fuel_func = lambda x : sum(d for d in [abs(c-x) for c in crabs])
    else:
        fuel_func = lambda x : sum((d * (d+1))//2 for d in [abs(c-x) for c in crabs])
    
    for x in range(min_x, max_x + 1):
        fuel = fuel_func(x)
        if best_fuel == None or fuel < best_fuel:
            best_fuel = fuel
            best_pos = x
    return (best_pos, best_fuel)

def test_p1():
    pos, fuel = work(test_input)
    assert(fuel == 37)
    assert(pos == 2)
test_p1()

def p1():
    pos, fuel = work(real_input)
    print(pos, fuel)
p1()

def test_p2():
    pos, fuel = work(test_input, True)
    assert(fuel == 168)
    assert(pos == 5)
test_p2()

def p2():
    pos, fuel = work(real_input, True)
    print(pos, fuel)
p2()
