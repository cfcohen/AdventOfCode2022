#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Advent of Code Day 14."""

import sys
from optparse import OptionParser

# ========================================================================================
# Advent of code infrastructure
# ========================================================================================

parser = OptionParser()
parser.add_option("-d", "--debug", action="store_true",
                  help="Emit additional debugging messages.")
parser.add_option("-p", "--part", action="store", type="int",
                  help="Choose which part to solve.")

(options, args) = parser.parse_args()
if len(args) > 0:
    parser.error("no arguments are allowed")

if options.part not in [1, 2]:
    parser.error("please specify --part=1 or --part=2")

def debug(*args, **kwargs):
    if options.debug:
        print(*args, **kwargs)

# ========================================================================================
# Solution
# ========================================================================================

# ----------------------------------------------------------------------------------------
# Shared
# ----------------------------------------------------------------------------------------
def read_input():
    "Read the challenge input as a list of lists of points."
    lines = []
    max_y = 0
    for line in sys.stdin:
        line = line.rstrip()
        points = []
        for term in line.split(' -> '):
            (x, y) = term.split(',')
            max_y = max(max_y, int(y))
            points.append((int(x), int(y)))
        lines.append(points)
    return max_y, lines

def make_grid(max_y, lines, part):
    # Sand can settle at columns 500 plus or minus max_y + 1.  Add a couple of extra
    # columns to match how part two was displayed in the challenge.
    min_x = 500 - (max_y + 3)
    max_x = 500 + (max_y + 3)

    # Fill the grid with "air" (periods).  Include one extra line of air at the bottom.
    grid = []
    width = max_x - min_x + 1
    for y in range(0, max_y + 2):
        grid.append(['.'] * width)

    # If we're in part two, add a floor beneath the grid.  It doesn't need to extend to
    # inifinity in each direction, only the width of the grid because we've made the grid
    # wide enough to catch all grains.
    if part == 2:
        grid.append(['#'] * width)

    # Mark the entry point of the sand, so our picture matches the challenge (mostly).
    grid[0][500-min_x] = '+'

    # Draw the barriers in the grid as described by the points.
    for line in lines:
        last_x = None
        last_y = None
        for point in line:
            (x, y) = point
            #debug("Drawing point (%s=%s, %s)" % (x, x-min_x, y))
            if last_x is None:
                #debug("Initial point (%s=%s, %s)" % (x, x-min_x, y))
                grid[y][x-min_x] = '#'
            elif x == last_x:
                #debug("Vertical line (%s, %s) -> (%s, %s)" % (last_x, last_y, x, y))
                if y < last_y:
                    for ty in range(y, last_y+1):
                        grid[ty][x-min_x] = '#'
                else:
                    for ty in range(last_y, y+1):
                        grid[ty][x-min_x] = '#'
            elif y == last_y:
                #debug("Horizontal line (%s, %s) -> (%s, %s)" % (last_x, last_y, x, y))
                if x < last_x:
                    for tx in range(x, last_x+1):
                        grid[y][tx-min_x] = '#'
                else:
                    for tx in range(last_x, x+1):
                        grid[y][tx-min_x] = '#'
            else:
                print("Unexpected line point (%d, %d) -> (%d, %d)" % (
                    last_x, last_y, x, y), file=sys.stderr)
            last_x = x
            last_y = y

    # Display the empty grid withteh obstacles in it.
    debug_grid(grid)
    return grid

def debug_grid(grid):
    "Display the grid."
    for n, line in enumerate(grid):
        debug("%3d %s" % (n, ''.join(line)))
    debug()

def move_sand(grid, x, y, trace=False):
    """
    Move a grain of sand from location x, y and return the place where it settles.

    If it settles in the "void" return (-1, -1).  If trace is True, draw tildes along the
    path that the grain of sand traverses.
    """
    #debug("Sand moved to (%s, %s)" % (x, y))
    # If the caller requested tracing, record that the sand passes through this location.
    if trace:
        grid[y][x] = '~'
    # If the grain would fall off the map it falls into the void.
    if y > len(grid) - 2:
        return (-1, -1)
    # Fall straight down.
    if grid[y+1][x] == '.':
        return move_sand(grid, x, y + 1, trace)
    # Fall diagonally to the left.
    elif grid[y+1][x-1] == '.':
        return move_sand(grid, x - 1, y + 1, trace)
    # Fall diagonally to the right.
    elif grid[y+1][x+1] == '.':
        return move_sand(grid, x + 1, y + 1, trace)
    # Where the grain of sand came to rest.
    return(x, y)

def fill_with_sand(grid, part):
    """
    Fill the grid with sand, releasing sand from the location marked '+'.
    """
    start_x = grid[0].index('+')
    grains = 0
    while True:
        (x, y) = move_sand(grid, start_x, 0)
        #debug("Sand settled at (%d, %d)" % (x, y))
        if x == -1:
            break
        grains += 1
        grid[y][x] = 'o'
        if (x, y) == (start_x, 0):
            break
        #debug_grid(grid)

    # For part one draw the path that all future sand will take (just for fun!)
    if part == 1:
        move_sand(grid, start_x, 0, trace=True)
    # Display the final grid configuration.
    debug_grid(grid)
    # Count the grains of sand that fell, and report the solution.
    print(grains)

if __name__ == '__main__':
    max_y, lines = read_input()
    grid = make_grid(max_y, lines, options.part)
    fill_with_sand(grid, options.part)

# Part one solution for test-input1 is: 24
# Part two solution for test-input2 is: 93
# Part one solution for input is: 763
# Part two solution for input is: 23921

# Local Variables:
# mode: python
# fill-column: 90
# eval: (flyspell-buffer)
# eval: (column-number-mode)
# End:
