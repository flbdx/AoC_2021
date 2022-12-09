#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import operator
from functools import reduce, cached_property

if len(sys.argv) == 1:
    sys.argv += ["input_16"]

real_input = next(fileinput.input())

def hex_to_bits(c):
    c = c.upper()
    n = (ord(c) - ord('0')) if c in "0123456789" else (ord(c) - ord('A') + 10)
    s = bin(n)[2:]
    return ("0"* (4 - len(s))) + s

class Bitstream(object):
    SEEK_SET = 0
    SEEK_CUR = 1
    SEEK_END = 2
    
    def __init__(self, hex_string):
        hex_string = hex_string.strip()
        self.bitstring = "".join(hex_to_bits(c) for c in hex_string)
        self.len = len(self.bitstring)
        self.pos = 0

    def read(self, n):
        end = min(self.pos + n, self.len)
        start = self.pos
        self.pos = end
        return self.bitstring[start:end]

    def tell(self):
        return self.pos

    def __len__(self):
        return self.len

    def __repr__(self):
        return repr((self.bitstring, self.pos))

    def __bool__(self):
        return self.pos < self.len
            
class Packet(object):
    def __init__(self, version, id_):
        self.version = version
        self.id = id_
        self.children = []
        self.literal = None

    def to_string(self, indent=""):
        s = "Packet v=" + repr(self.version) + " id=" + repr(self.id)
        if self.literal != None:
            s += " lit=" + repr(self.literal)
        for c in self.children :
            s += "\n  " + indent + c.to_string(indent + "  ")
        return s

    def __repr__(self):
        return self.to_string()
    
    @cached_property
    def value(self):
        return self.calc_packet()
    
    def calc_packet(self):
        if self.id == 0:
            return sum(c.value for c in self.children)
        if self.id == 1:
            return reduce(operator.mul, (c.value for c in self.children), 1)
        if self.id == 2:
            return reduce(min, (c.value for c in self.children))
        if self.id == 3:
            return reduce(max, (c.value for c in self.children))
        if self.id == 4:
            return self.literal
        if self.id == 5:
            return 1 if self.children[0].value > self.children[1].value else 0
        if self.id == 6:
            return 1 if self.children[0].value < self.children[1].value else 0
        if self.id == 7:
            return 1 if self.children[0].value == self.children[1].value else 0
    
    @staticmethod
    def read_one_packet(bs):
        p = Packet(int(bs.read(3), 2), int(bs.read(3), 2))
        if p.id == 4:
            n = 0
            while True:
                v = bs.read(5)
                more, v = int(v[0]), int(v[1:], 2)
                n += v
                if more == 1:
                    n *= 16
                else:
                    break
            p.literal = n
            return p
        else:
            length_type = int(bs.read(1), 2)
            if length_type == 0:
                total_length = int(bs.read(15), 2)
                pos = bs.tell()
                while total_length:
                    p.children.append(Packet.read_one_packet(bs))
                    npos = bs.tell()
                    total_length -= (npos - pos)
                    pos = npos
                return p
            else:
                n_sub_packets = int(bs.read(11), 2)
                for n in range(n_sub_packets):
                    p.children.append(Packet.read_one_packet(bs))
            return p


def work_p1(inputs):
    bs = Bitstream(inputs)
    p = Packet.read_one_packet(bs)
    vsum = p.version
    to_check = list(p.children)
    while len(to_check) != 0:
        c = to_check.pop()
        vsum += c.version
        to_check += list(c.children)
    return vsum

def work_p2(inputs):
    bs = Bitstream(inputs)
    p = Packet.read_one_packet(bs)
    return p.calc_packet()

def test_p1():
    assert(work_p1("8A004A801A8002F478") == 16)
    assert(work_p1("620080001611562C8802118E34") == 12)
    assert(work_p1("C0015000016115A2E0802F182340") == 23)
    assert(work_p1("A0016C880162017C3686B18A3D4780") == 31)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2("C200B40A82") == 3)
    assert(work_p2("04005AC33890") == 54)
    assert(work_p2("880086C3E88112") == 7)
    assert(work_p2("CE00C43D881120") == 9)
    assert(work_p2("D8005AC2A8F0") == 1)
    assert(work_p2("F600BC2D8F") == 0)
    assert(work_p2("9C005AC2F8F0") == 0)
    assert(work_p2("9C0141080250320F1802104A08") == 1)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
