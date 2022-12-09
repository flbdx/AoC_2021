#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque

test_input="""#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_23"]

# returns a big tuple with the hallway status and amphipods by descending level then left from right
def read_input(inputs, part2=False):
    it = iter(inputs)
    next(it)
    next(it)
    l = [None for i in range(11)]
    level = 1
    
    amphipod_numbers = {l:1 for l in "ABCD"}
    
    for line in it:
        line = line.strip()
        for c in line:
            if c in "ABCD":
                l.append(c + repr(amphipod_numbers[c]))
                amphipod_numbers[c] += 1
        level += 1
        if level == 2 and part2:
            for c in "#D#C#B#A#":
                if c in "ABCD":
                    l.append(c + repr(amphipod_numbers[c]))
                    amphipod_numbers[c] += 1
            level += 1
            for c in "#D#B#A#C#":
                if c in "ABCD":
                    l.append(c + repr(amphipod_numbers[c]))
                    amphipod_numbers[c] += 1
            level += 1
    return tuple(l)

# energy cost
mult = {"A": 1, "B": 10, "C": 100, "D": 1000}
# position of each burrow from the hallway
burrows_pos = {"A": 2, "B": 4, "C": 6, "D": 8}
# hallway positions that we can reach from each burrow, toward the left or right
burrows_sides = {"A": ( (1, 0), (3, 5, 7, 9, 10) ), "B": ( (3, 1, 0), (5, 7, 9, 10) ), "C": ( (5, 3, 1, 0), (7, 9, 10) ), "D":  ( (7, 5, 3, 1, 0), (9, 10) )}

# super inefficient state :-) 
# hallway nodes are tuple('H', pos) with pos from 0 to 10
# burrow nodes are tupple('B', type, level) with type in "ABCD" and level >= 1 (1 == closest to hallway)
# the burrow's level is the number of steps to reach the hallway
class State(object):
    def __init__(self):
        self.nodes_content = {}
        self.amphipods_pos = {}
        self.depth = 0
    
    # set from input
    def from_tuple(self, state):
        self.nodes_content = {}
        self.amphipods_pos = {}
        self.depth = 0
        
        # hallway
        i = 0
        while i < 11:
            node = ("H", i)
            if state[i] == None:
                self.nodes_content[node] = None
            else:
                self.nodes_content[node] = state[i]
                self.amphipods_pos[state[i]] = node
            i += 1
        level = 1
        while i < len(state):
            for j in "ABCD":
                node = ("B", j, level)
                if state[i] == None:
                    self.nodes_content[node] = None
                else:
                    self.nodes_content[node] = state[i]
                    self.amphipods_pos[state[i]] = node
                i += 1
            level += 1
        self.depth = level - 1
    
    # check if an amphipod is in its final position
    def is_set(self, amphipod):
        node = self.amphipods_pos[amphipod]
        t = amphipod[0]
        if node[0] == "H": # in hallway
            return False
        if node[1] != t: # not in the correct burrow
            return False
        for l in range(node[2]+1, self.depth + 1): # check the depth of the burrow
            node2 = (node[0], node[1], l)
            if self.nodes_content[node2][0] != t:
                return False
        return True
    
    # check whether a burrow can accept an amphipod
    # if its ready, then returns the destination level
    # else returns None
    def burrow_can_accept(self, burrow):
        for l in range(self.depth, 0, -1):
            node = ('B', burrow, l)
            c = self.nodes_content[node]
            if c == None:
                return l
            if c[0] != burrow:
                return None
        return None
    
    # returns the number of steps to reach the n_to node from the n_from node
    # returns None if the path is blocked or invalid
    def path_len(self, n_from, n_to):                      
        if n_from[0] == "H" and n_to[0] == "H": # hallway to hallway is not allowed
            return None
        if n_from[0] == "B" and n_to[0] == "B" and n_from[1] == n_to[1]: # burrow to the same burrow
            return None
        
        path_len = 0
        
        p = n_from
        
        if p[0] == 'B': # reach the hallway
            burrow = p[1]
            for l in range(n_from[2] - 1, 0, -1):
                p = ("B", p[1], l)
                if self.nodes_content[p] != None:
                    return None
                path_len += 1
            
            p = ("H", burrows_pos[burrow])
            if self.nodes_content[p] != None:
                return None
            path_len += 1
        
        # move to our destination or over the destination burrow
        h_dest = n_to[1] if n_to[0] == "H" else burrows_pos[n_to[1]]
        direction = 1 if h_dest > p[1] else -1
        while p[1] != h_dest:
            p = ("H", p[1] + direction)
            if self.nodes_content[p] != None:
                return None
            path_len += 1
        
        if n_to[0] == "B": # reach the destination level
            for l in range(1, n_to[2] + 1):
                if self.nodes_content[p] != None:
                    return None
                path_len += 1

        return path_len
    
    # returns a list of the valid moves
    # each move is a tuple(amphipod, from_node, to_node, energy_cost)
    def possible_moves(self):
        moves =[]
        
        amphipod_is_set = {a:self.is_set(a) for a in self.amphipods_pos}
        
        # if we can set an amphipod, do-it
        for amphipod, node in self.amphipods_pos.items():
            if amphipod_is_set[amphipod]:
                continue
            at = amphipod[0]
            bl = self.burrow_can_accept(at)
            if bl != None:
                dnode = ('B', at, bl)
                pl = self.path_len(node, dnode)
                if pl != None:
                    return [(amphipod, node, dnode, pl * mult[at])]
        
        # no amphipod can be set, 
        # so the only valid moves are from burrow to hallway
        for amphipod, node in self.amphipods_pos.items():
            if amphipod_is_set[amphipod]:
                continue
            at = amphipod[0]
            if node[0] == "H": # in the hallway
                continue # we can only move this one in it's burrow and we could'nt
            else:
                burrow = node[1]
                level = node[2]
                # move left or right ?
                for side in burrows_sides[burrow]:
                    for hall in side:
                        dnode = ("H", hall)
                        pl = self.path_len(node, dnode)
                        if pl != None:
                            moves.append((amphipod, node, dnode, pl * mult[at]))
                        else:
                            break # this side is blocked
        return moves
    
    def __lt__(self, other):
        return repr(self) < repr(other)
    
    # returns a new state with the move applied
    def do_move(self, move):
        r = State()
        r.nodes_content = dict(self.nodes_content)
        r.amphipods_pos = dict(self.amphipods_pos)
        r.depth = self.depth
        
        amph, nfrom, nto, cost = move
        
        r.nodes_content[nfrom] = None
        r.nodes_content[nto] = amph
        r.amphipods_pos[amph] = nto
        
        return r
    
    def all_done(self):
        for amph, node in self.amphipods_pos.items():
            if node[0] == "H":
                return False
            if node[1] != amph[0]:
                return False
        return True
        

def work(inputs, part2=False):
    starting_state = read_input(inputs, part2)
    s = State()
    s.from_tuple(starting_state)

    q = deque()
    q.appendleft((s, 0))
    
    best_energy = None
    
    while len(q) > 0:
        s, energy = q.pop()
        if best_energy != None and energy >= best_energy:
            continue
        if s.all_done():
            best_energy = energy if best_energy == None else min(energy, best_energy)
        else:
            for move in s.possible_moves():
                s2 = s.do_move(move)
                q.append((s2, energy + move[3]))
    return best_energy

#import heapq
#def work(inputs, part2=False):
    #starting_state = read_input(inputs, part2)
    #s = State()
    #s.from_tuple(starting_state)
    
    #q = []
    #heapq.heappush(q, (0, s))
    #best_energy = None
    
    #while len(q) > 0:
        #energy, s = q.pop()
        #if best_energy != None and energy >= best_energy:
            #continue
        #if s.all_done():
            #best_energy = energy if best_energy == None else min(energy, best_energy)
        #else:
            #for move in s.possible_moves():
                #s2 = s.do_move(move)
                #energy2 = energy + move[3]
                #if best_energy == None or energy2 < best_energy:
                    #heapq.heappush(q, (energy2, s2))
    #return best_energy
    

def test_p1():
    assert(work(test_input) == 12521)
test_p1()

def p1():
    print(work(fileinput.input()))
p1()

def test_p2():
    assert(work(test_input, True) == 44169)
test_p2()

def p2():
    print(work(fileinput.input(), True))
p2()
