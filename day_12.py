#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque

test_input_1="""start-A
start-b
A-c
A-b
b-d
A-end
b-end""".splitlines()

test_input_2="""dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""".splitlines()

test_input_3="""fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_12"]

def parse_input(inputs):
    transitions = {}
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        n1, n2 = line.split("-")
        if n2 != 'start': # skip transitions to start
            transitions[n1] = transitions.setdefault(n1, set()).union({n2})
        if n1 != 'start':
            transitions[n2] = transitions.setdefault(n2, set()).union({n1})
    return transitions

def work(inputs, part2=False):
    transitions = parse_input(inputs)
    q = deque()
    q.append(["start"])
    all_paths = []
    
    def path_is_valid_part2(path):
        # that's one way of counting...
        l = [e for e in path if e != 'start' and e.lower() == e]
        s = set(l) # uniquify
        return len(l) == len(s) or len(l) == len(s) + 1
    
    while len(q) != 0:
        path = q.pop()
        node = path[-1]
        for nxt in transitions[node]:
            if nxt == "end":
                all_paths.append(path + [nxt])
            elif nxt.lower() == nxt and nxt in path:
                if part2:
                    npath = path + [nxt]
                    if path_is_valid_part2(npath):
                        q.append(npath)
            else:
                q.append(path + [nxt])
    #print(all_paths)
    return len(all_paths)

def test_p1():
    assert(work(test_input_1) == 10)
    assert(work(test_input_2) == 19)
    assert(work(test_input_3) == 226)
test_p1()

def p1():
    print(work(fileinput.input()))
p1()

def test_p2():
    assert(work(test_input_1, True) == 36)
    assert(work(test_input_2, True) == 103)
    assert(work(test_input_3, True) == 3509)
test_p2()

def p2():
    print(work(fileinput.input(), True))
p2()
