#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_06"]

test_input = """3,4,3,1,2"""
real_input = next(fileinput.input())

def input_to_state(inputs):
    numbers = [int(v) for v in inputs.strip().split(",")]
    state = [0] * 9
    for n in numbers:
        state[n] += 1
    return state

def run_simu(state_, days, pos=0):
    state = list(state_)
    p = pos
    l = 9
    for day in range(days):
        state[(p + 7) % l] += state[p % l]
        p += 1
    return (state, p % l)

def test_p1():
    s, p = run_simu(input_to_state(test_input), 18)
    assert sum(s) == 26
    s, p = run_simu(input_to_state(test_input), 80)
    assert sum(s) == 5934
test_p1()

def p1():
    s, p = run_simu(input_to_state(real_input), 80)
    print(sum(s))
p1()

def test_p2():
    s, p = run_simu(input_to_state(test_input), 256)
    assert sum(s) == 26984457539
test_p2()

def p2():
    s, p = run_simu(input_to_state(real_input), 256)
    print(sum(s))
p2()
