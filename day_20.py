#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_20"]

def read_input(inputs):
    algo = []
    image = {} # we store only the lighted pixel
    
    it = iter(inputs)
    line = next(it).strip()
    algo = [1 if c == '#' else 0 for c in line]
    next(it)
    
    min_x, max_x, min_y, max_y = None, None, None, None
    
    for y, line in enumerate(it):
        line = line.strip()
        if len(line) == 0:
            continue
        for x, c in enumerate(line):
            if c == '#':
                image[x,y] = 1
                min_x = x if min_x == None or x < min_x else min_x
                max_x = x if max_x == None or x > max_x else max_x
                min_y = y if min_y == None or y < min_y else min_y
                max_y = y if max_y == None or y > max_y else max_y
    
    
    return (algo, image, min_x, max_x, min_y, max_y)

def work(inputs, steps=2):
    algo, image, min_x, max_x, min_y, max_y = read_input(inputs)
    
    default = 0 # default pixel value for what's not stored in "image"
    alt = (algo[0] == 1) # ah. yeah... flashing infinity
    
    # the infinite borders of our puzzle are flashing if alt == True
    # so we alternate the default value of image after each step

    for s in range(steps):
        # helper function to get a value from image without inserting a new one and defaulting to the current value of "default"
        # /!\ a lambda captures by reference and not by value
        # since we will modify default, this function will help to copy default
        def gen_dict_getter(d):
            return lambda x, y : image.get((x,y), d)
        get = gen_dict_getter(default)
        
        if alt:
            default = (1 - default)
        nimage = {}
        
        for y in range(min_y - 1, max_y + 2):
            for x in range(min_x - 1, max_x + 2):
                n = 0
                for v in [get(x-1,y-1), get(x,y-1), get(x+1,y-1), get(x-1,y), get(x,y), get(x+1,y), get(x-1,y+1), get(x,y+1), get(x+1,y+1)]:
                    n = n << 1
                    n += v
                r = algo[n]
                if r != default:
                    nimage[x,y] = r
        image = nimage
        min_x -= 1
        min_y -= 1
        max_x += 1
        max_y += 1
    
    # I guess we won't be asked for an odd number of steps with a flashing puzzle... 
    return len(image) # sum(1 for p in image if image[p] == 1)

def test_p1():
    assert(work(test_input) == 35)
test_p1()

def p1():
    print(work(fileinput.input(), 2))
p1()

def test_p2():
    assert(work(test_input, 50) == 3351)
test_p2()

def p2():
    print(work(fileinput.input(), 50))
p2()
