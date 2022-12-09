#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque
from itertools import permutations

test_input = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_18"]

# A tree for our expressions
# either a literal if self.literal != None or a pair
class Number(object):
    def __init__(self):
        self.literal = None
        self.values = []
        self.parent = None
    
    def __repr__(self):
        if self.literal != None:
            return repr(self.literal)
        return "[" + repr(self.values[0]) + "," + repr(self.values[1]) + "]"
    
    # erase the children, replace with a literal
    def set_literal(self, v):
        self.literal = v
        for v in self.values:
            v.parent = None
        self.values = []
    
    # erase the literal and add a child
    def add_child(self, n):
        self.literal = None
        self.values.append(n)
        n.parent = self
    
    def is_literal(self):
        return self.literal != None
    
    @staticmethod
    def new_literal(v):
        n = Number()
        n.set_literal(v)
        return n
    
    @staticmethod
    def new_pair(l, r):
        n = Number()
        n.add_child(l)
        n.add_child(r)
        return n
    
    @staticmethod
    def parse(s):
        root = Number()
        stack = [root]
        for c in s.strip():
            if c == '[':
                n = Number()
                stack[-1].add_child(n)
                stack.append(n)
                value = None
            elif c == ',':
                if value != None:
                    n = Number.new_literal(value)
                    stack[-1].add_child(n)
                    value = None
            elif c == ']':
                if value != None:
                    n = Number.new_literal(value)
                    stack[-1].add_child(n)
                    value = None
                stack.pop()
            else:
                value = (value * 10 + int(c)) if value != None else int(c)
        r = root.values[0]
        r.parent = None
        return r
    
    def __add__(self, other):
        n = Number()
        n.add_child(Number.parse(repr(self)))   # boys, that's how we copy things here
        n.add_child(Number.parse(repr(other)))
        n.reduce()
        return n
    
    def reduce(self):
        # build a list with all the leaf literal nodes from left to right.
        # For each node, we store (node, depth)
        all_leafs = []
        stack = deque()
        stack.append((self, 0))
        while len(stack) != 0:
            node, depth = stack.popleft()
            if node.is_literal():
                all_leafs.append((node, depth))
            else:
                stack.appendleft((node.values[1], depth + 1))
                stack.appendleft((node.values[0], depth + 1))
        
        while True:
            one_more_pass = False
        
            # If any pair is nested inside four pairs, the leftmost such pair explodes.
            idx = 0
            while idx < len(all_leafs):
                node, depth = all_leafs[idx]
                # inside a pair of depth 4 or more, and with a right sibling
                if depth >= 5 and (idx != len(all_leafs) - 1) and all_leafs[idx+1][0].parent == node.parent:
                    pair = node.parent
                    vleft = pair.values[0]
                    vright = pair.values[1]
                    pair.set_literal(0) # replace the pair by a 0 literal
                    
                    if idx -1 >= 0: # there is another literal on our left
                        all_leafs[idx - 1][0].literal += vleft.literal
                    if idx + 2 < len(all_leafs): # maybe another literal on our right
                        all_leafs[idx + 2][0].literal += vright.literal
                    all_leafs[idx] = (pair, depth - 1)
                    del all_leafs[idx + 1]
                    
                    one_more_pass = True
                
                idx += 1
            
            # If any regular number is 10 or greater, the leftmost such regular number splits.
            idx = 0
            while idx < len(all_leafs):
                node, depth = all_leafs[idx]
                if node.literal >= 10:
                    pair = node.parent
                    side = 0 if pair.values[0] == node else 1 # left or right ?
                    
                    repl_left = node.literal // 2
                    repl_right = node.literal - repl_left
                    repl_left = Number.new_literal(repl_left)
                    repl_right = Number.new_literal(repl_right)
                    repl = Number.new_pair(repl_left, repl_right)
                    repl.parent = pair
                    pair.values[side] = repl
                    
                    all_leafs[idx] = (repl_left, depth + 1)
                    all_leafs.insert(idx + 1, (repl_right, depth + 1))
                    
                    one_more_pass = True
                    if depth >= 4:
                        break
                    else:
                        # we are sure that we have not created a new pair with a depth >= 4
                        # so let's continue splitting numbers
                        idx -= 1
                else:
                    idx += 1
            
            
            if not one_more_pass:
                break
                
    
    def magnitude(self):
        if self.literal != None:
            return self.literal
        return 3 * self.values[0].magnitude() + 2 * self.values[1].magnitude()

def work_p1(inputs):
    numbers = []
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        numbers.append(Number.parse(line))
    
    n = sum(numbers[1:], numbers[0])
    return n.magnitude()

def work_p2(inputs):
    numbers = []
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        numbers.append(Number.parse(line))

    max_mag = -1
    for n1, n2 in permutations(numbers, 2):
        mag = (n1 + n2).magnitude()
        if mag > max_mag:
            max_mag = mag
    return max_mag

def test_p1():
    assert(work_p1(test_input) == 4140)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 3993)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()


