#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import Counter

test_input="""NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_14"]

def read_input(inputs):
    seq = ""
    rules = {}
    
    inputs = list(inputs)
    it = iter(inputs)
    seq = next(it).strip()
    next(it)
    while True:
        line = next(it, None)
        if line == None:
            break
        line = line.strip()
        if len(line) == 0:
            break
        a, b = line.split(" -> ")
        p1, p2 = a[0], a[1]
        rules[p1, p2] = b
    
    return seq, rules

def work_p2(inputs, steps=40):
    seq, rules = read_input(inputs)
    # with this prefix and suffix, every char belongs to 2 pairs
    seq = "*" + seq + "*"
    
    pairs_count = {}
    for i in range(len(seq) - 1):
        a, b = seq[i:i+2]
        pairs_count[a,b] = pairs_count.setdefault((a,b), 0) + 1
    
    for step in range(steps):
        pairs = list(p for p,c in pairs_count.items() if c > 0)
        n_pairs_count = {}
        for p in pairs:
            if '*' in p:
                n_pairs_count[p] = pairs_count[p]
            else:
                r = rules[p]
                c = pairs_count[p]
                n_pairs_count[p[0], r] = n_pairs_count.setdefault((p[0], r), 0) + c
                n_pairs_count[r, p[1]] = n_pairs_count.setdefault((r, p[1]), 0) + c
        pairs_count = n_pairs_count
    
    count = {}
    for p, c in pairs_count.items() :
        count[p[0]] = count.setdefault(p[0], 0) + c
        count[p[1]] = count.setdefault(p[1], 0) + c
    del count["*"]
    
    max_count = max(c//2 for p, c in count.items())
    min_count = min(c//2 for p, c in count.items())
    return max_count - min_count

def test_p1():
    assert(work_p2(test_input, 10) == 1588)
test_p1()

def p1():
    print(work_p2(fileinput.input(), 10))
p1()

def test_p2():
    assert(work_p2(test_input) == 2188189693529)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
