#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_03"]

test_input="""00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

def read_inputs(inputs):
    r = []
    for line in inputs:
        line = line.strip()
        if len(line) > 0:
            r.append(line)
    return r

def work_p1(inputs):
    inputs = read_inputs(inputs)
    width = len(inputs[0])
    
    gamma_rate = 0
    for n in range(0, width):
        c = sum(int(l[n]) for l in inputs)
        gamma_rate <<= 1
        gamma_rate |= (1 if 2*c > len(inputs) else 0)

    epsilon_rate = 2**width - 1 - gamma_rate
    
    return gamma_rate * epsilon_rate

def work_p2(inputs):
    inputs = read_inputs(inputs)
    width = len(inputs[0])
    
    oxygen_inputs = list(inputs)
    co2_inputs = list(inputs)
    
    def filter_list(lst, n, crit_1_most, crit_1_least):
        c = sum(int(l[n]) for l in lst)
        crit = crit_1_most if 2*c >= len(lst) else crit_1_least
        return [l for l in lst if l[n] == crit]
    
    for n in range(0, width):
        if len(oxygen_inputs) > 1:
            oxygen_inputs = filter_list(oxygen_inputs, n, '1', '0')
        if len(co2_inputs) > 1:
            co2_inputs = filter_list(co2_inputs, n, '0', '1')
    
    return int(oxygen_inputs[0], 2) * int(co2_inputs[0], 2)

def test_p1():
    assert(work_p1(test_input.splitlines()) == 198)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input.splitlines()) == 230)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
