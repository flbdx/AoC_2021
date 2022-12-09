#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque

if len(sys.argv) == 1:
    sys.argv += ["input_10"]

test_input = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""".splitlines()

matching_chars = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
    }

points_p1 = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
    }

points_p2 = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
    }

def work(inputs, part2=False):
    score_p1 = 0
    scores_p2 = []
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        q = deque()
        broken = False
        score_p2 = 0
        for c in line:
            if c in '{(<[':
                q.append(c)
            else:
                if matching_chars[q.pop()] != c:
                    score_p1 += points_p1[c]
                    broken = True
                    break
        if not broken:
            while len(q) != 0:
                score_p2 = score_p2*5 + points_p2[matching_chars[q.pop()]]
            scores_p2.append(score_p2)
    
    scores_p2 = list(sorted(scores_p2))
    
    return scores_p2[len(scores_p2)//2] if part2 else score_p1

def test_p1():
    assert(work(test_input) == 26397)
test_p1()

def p1():
    print(work(fileinput.input()))
p1()

def test_p2():
    assert(work(test_input, True) == 288957)
test_p2()

def p2():
    print(work(fileinput.input(), True))
p2()
