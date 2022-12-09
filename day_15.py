#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import networkx as nx

test_input="""1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_15"]

def read_input(inputs):
    grid = {}
    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            break
        for x, c in enumerate(line):
            grid[x,y] = int(c)
    return grid, x+1, y+1

def work_p1(inputs):
    grid, width, height = read_input(inputs)
    
    start_state = (0,0)
    end_state = (width - 1, height - 1)
    
    G = nx.DiGraph()
    for y in range(height):
        for x in range(width):
            if y != 0:
                G.add_edge((x,y), (x, y-1), weight=grid[x, y-1])
            if y != height - 1:
                G.add_edge((x,y), (x, y+1), weight=grid[x, y+1])
            if x != 0:
                G.add_edge((x,y), (x-1, y), weight=grid[x-1, y])
            if x != width - 1:
                G.add_edge((x,y), (x+1, y), weight=grid[x+1, y])
    
    return nx.shortest_path_length(G, start_state, end_state, weight="weight")
    

def work_p2(inputs):
    grid, width, height = read_input(inputs)
    
    def expanded_grid_value(x, y):
        nonlocal grid, width, height
        gx, mx = divmod(x, width)
        gy, my = divmod(y, height)
        v = grid[mx,my] + gx + gy
        return ((v - 1) % 9) + 1
    
    xwidth = width * 5
    xheight = height * 5
    start_state = (0,0)
    end_state = (xwidth - 1, xheight - 1)
    
    G = nx.DiGraph()
    for y in range(xheight):
        for x in range(xwidth):
            if y != 0:
                G.add_edge((x,y), (x, y-1), weight=expanded_grid_value(x, y-1))
            if y != xheight - 1:
                G.add_edge((x,y), (x, y+1), weight=expanded_grid_value(x, y+1))
            if x != 0:
                G.add_edge((x,y), (x-1, y), weight=expanded_grid_value(x-1, y))
            if x != xwidth - 1:
                G.add_edge((x,y), (x+1, y), weight=expanded_grid_value(x+1, y))
    
    #print(G.order(), G.size())
    return nx.shortest_path_length(G, start_state, end_state, weight="weight")

def test_p1():
    assert(work_p1(test_input) == 40)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 315)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
