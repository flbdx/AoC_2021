#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re
from collections import namedtuple

test_input="""Player 1 starting position: 4
Player 2 starting position: 8""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_21"]

class DeterministicDice(object):
    def __init__(self):
        self.v = 1
        self.rolls = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next()
    
    def next(self):
        v = self.v
        self.v = 1 if self.v == 100 else self.v + 1
        self.rolls += 1
        return v

class Player(object):
    def __init__(self, n, pos):
        self.n = n
        self.pos = pos
        self.score = 0
    
    def __repr__(self):
        return "Player " + repr(self.n) + " pos " + repr(self.pos) + " score " + repr(self.score)
    
    def round(self, dice):
        for i in range(3):
            self.pos += next(dice)
        self.pos = ((self.pos - 1) % 10) + 1
        self.score += self.pos

def read_input(inputs):
    players = {}
    re_int = re.compile("[0-9]+")
    
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        ints = list(map(int, re_int.findall(line)))
        players[ints[0]] = Player(*ints)
    return players


def work_p1(inputs):
    players = read_input(inputs)
    sorted_players = list(sorted(players.keys()))
    dé = DeterministicDice()
    
    while True:
        for pn in sorted_players:
            players[pn].round(dé)
            if players[pn].score >= 1000:
                return dé.rolls * min(p.score for p in players.values())
    



State = namedtuple("State", ("p1_pos", "p1_score", "p2_pos", "p2_score", "player"))

def work_p2(inputs):
    players = read_input(inputs)
    #sorted_players = list(sorted(players.keys()))
    
    possibilities = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
    
    all_states = {}
    all_states[State(players[1].pos, 0, players[2].pos, 0, 1)] = 1 # we start with 1 univers, I hope...
    
    wins = {1:0, 2:0}
    def play_turn():
        nonlocal all_states, wins
        new_states = {}
        
        for state, n_univers in all_states.items():
            p_idx = state.player - 1
            pos, score = state[p_idx*2+0], state[p_idx*2+1]
            for adv, occurences in possibilities.items():
                npos = ((pos - 1 + adv) % 10) + 1
                nscore = score  + npos
                if nscore >= 21:
                    wins[state.player] += n_univers * occurences
                else:
                    # mutable named tuple when
                    s = State(npos, nscore, state.p2_pos, state.p2_score, 2) if p_idx == 0 else State(state.p1_pos, state.p1_score, npos, nscore, 1)
                    new_states[s] = new_states.setdefault(s, 0) + n_univers * occurences
                        
        all_states = new_states
        return wins
    
    wins = {1:0, 2:0}
    while len(all_states) > 0:
        w = play_turn()
    
    return max(wins.values())

def test_p1():
    assert(work_p1(test_input) == 739785)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 444356092776315)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
