#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_24"]        


class Monad(object):
    def __init__(self, code):
        self.regs = {r:0 for r in "wxyz"}
        self.ins = []
        self.inp = ""
        
        for line in code:
            line = line.strip()
            if len(line) == 0:
                continue
            line = line.split(" ")
            if line[0] == "inp":
                self.ins.append((Monad.do_inp, line[1]))
            elif line[0] == "add":
                self.ins.append((Monad.do_add, line[1], line[2]))
            elif line[0] == "mul":
                self.ins.append((Monad.do_mul, line[1], line[2]))
            elif line[0] == "div":
                self.ins.append((Monad.do_div, line[1], line[2]))
            elif line[0] == "mod":
                self.ins.append((Monad.do_mod, line[1], line[2]))
            elif line[0] == "eql":
                self.ins.append((Monad.do_eql, line[1], line[2]))
            
    def do_inp(self, r):
        #print("\n>> inp", 14-len(self.inp) + 1, r, self.inp, self.regs)
        try:
            n, self.inp = int(self.inp[0]), self.inp[1:]
            self.regs[r] = n
        except:
            raise Exception("Empty input")
    
    def do_add(self, a, b):
        #print("add " + a + " " + repr(b), self.regs)
        if b in "wxyz":
            b = self.regs[b]
        else:
            b = int(b)
        self.regs[a] += b
    
    def do_mul(self, a, b):
        #print("mul " + a + " " + repr(b), self.regs)
        if b in "wxyz":
            b = self.regs[b]
        else:
            b = int(b)
        self.regs[a] *= b
    
    def do_div(self, a, b):
        #print("div " + a + " " + repr(b), self.regs)
        if b in "wxyz":
            b = self.regs[b]
        else:
            b = int(b)
        if b == 0:
            raise Exception("MONAD div by 0")
        self.regs[a] //= b
    
    def do_mod(self, a, b):
        #print("mod " + a + " " + repr(b), self.regs)
        if b in "wxyz":
            b = self.regs[b]
        else:
            b = int(b)
        if self.regs[a] < 0 or b <= 0:
            raise Exception("MONAD invalid mod a=" + repr(self.regs[a]) + " b=" + repr(b))
        self.regs[a] = self.regs[a] % b
    
    def do_eql(self, a, b):
        #print("eql " + a + " " + repr(b), self.regs)
        if b in "wxyz":
            b = self.regs[b]
        else:
            b = int(b)
        self.regs[a] = 1 if self.regs[a] == b else 0
    
    def run(self, inp, reset=True):
        if reset:
            self.regs = {r:0 for r in "wxyz"}
        self.inp = inp
        line = 1
        for ins in self.ins:
            try:
                ins[0](self, *(ins[1:]))
            except:
                print("Erreur ligne " + repr(line))
                raise
            line += 1

def work_p1(inputs):
    monad = Monad(inputs)
    monad.run("39999698799429")
    print(monad.regs)

def work_p2(inputs):
    monad = Monad(inputs)
    monad.run("18116121134117")
    print(monad.regs)

def test_p1():
    #assert(work(test_input) == None)
    monad = Monad(test_input)
    monad.run("9")
    print(monad.regs)
#test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def p2():
    print(work_p2(fileinput.input()))
p2()
