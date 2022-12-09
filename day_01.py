#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import collections

if len(sys.argv) == 1:
    sys.argv += ["input_01"]

test_input="""199
200
208
210
200
207
240
269
260
263"""

def work(inputs, window=1):
    r = 0
    it = map(lambda s : int(s), inputs)
    s = 0
    p = None
    q = collections.deque()
    while len(q) < window:
        v = next(it)
        s += v
        q.append(v)
        p = s
    for v in it:
        s += v - q.popleft()
        q.append(v)
        if s > p:
            r += 1
        p = s
    return r
    

def test_p1():
    assert(work(test_input.splitlines()) == 7)

test_p1()

def p1():
    print(work(fileinput.input()))
p1()

def test_p2():
    assert(work(test_input.splitlines(), 3) == 5)

test_p2()

def p2():
    print(work(fileinput.input(), 3))
p2()
