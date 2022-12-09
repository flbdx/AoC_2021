#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_08"]

test_input_short=["acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"]
test_input = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce""".splitlines()
#real_input = fileinput.input().splitlines()

def work_p1(inputs):
    r = 0
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        pre_words, valid_words = [p.split(" ") for p in line.split(" | ")]
        r += sum(1 for w in valid_words if len(w) in (2,3,4,7))
    return r

def solve(words):
    candidates = {l:set("abcdefg") for l in "abcdefg"}
    
    # when a segment is set, remove it from the other candidates
    def simplify():
        nonlocal candidates
        for l1 in candidates:
            if len(candidates[l1]) == 1:
                for l2 in candidates:
                    if l1 != l2:
                        candidates[l2].difference_update(candidates[l1])
    
    # reduce the possibilities using the numbers 1, 7 and 4
    for word in words:
        if len(word) == 2:
            candidates['c'].intersection_update(set(word))
            candidates['f'].intersection_update(set(word))
            for l in "abdeg":
                candidates[l].difference_update(set(word))
        elif len(word) == 3:
            candidates['a'].intersection_update(set(word))
            candidates['c'].intersection_update(set(word))
            candidates['f'].intersection_update(set(word))
            for l in "bdeg":
                candidates[l].difference_update(set(word))
        elif len(word) == 4:
            candidates['b'].intersection_update(set(word))
            candidates['c'].intersection_update(set(word))
            candidates['d'].intersection_update(set(word))
            candidates['f'].intersection_update(set(word))
            for l in "aeg":
                candidates[l].difference_update(set(word))
    simplify()
    
    # here, we always have the "a" segment set, and only two candidates for the other segments
    
    # the "b" and "e" segment appear once among the 5 segment digits (2, 3 and 5)
    # "b" appears 3 times among the 6 segment digits(0, 6 9)
    # while "e" appears 2 times
    for seg in "abcdefg":
        count_5 = sum(1 for w in words if len(w) == 5 and seg in w)
        count_6 = sum(1 for w in words if len(w) == 6 and seg in w)
        if count_5 == 1: # segment b or e
            if count_6 == 2: # segment e
                candidates["e"] = {seg}
            elif count_6 == 3: # segment b
                candidates["b"] = {seg}
    simplify()
    
    # here we should only avec the c and f segments left to sort out
    # the "c" segment must appear twice in the 6 segment digits
    for seg in candidates['c']:
        #count_5 = sum(1 for w in words if len(w) == 5 and seg in w)
        count_6 = sum(1 for w in words if len(w) == 6 and seg in w)
        if count_6 == 2: # segment c
            candidates["c"] = {seg}
            break
    simplify()
    
    return {list(candidates[l])[0]:l for l in candidates}

def word_to_digit(word):
    return {"abcefg": "0",
            "cf": "1",
            "acdeg": "2",
            "acdfg": "3",
            "bcdf": "4",
            "abdfg": "5",
            "abdefg": "6",
            "acf": "7",
            "abcdefg": "8",
            "abcdfg": "9"}[word]

def work_p2(inputs):
    r = 0
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        pre_words, valid_words = [p.split(" ") for p in line.split(" | ")]
        
        table = solve(pre_words)
        #print(table)
        
        converted_words = ["".join(sorted(table[c] for c in w))  for w in valid_words]
        converted_words = [word_to_digit(w) for w in converted_words]
        r += int("".join(converted_words))
        
    return r

def test_p1():
    assert(work_p1(test_input)) == 26
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input_short) == 5353)
    assert(work_p2(test_input) == 61229)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
