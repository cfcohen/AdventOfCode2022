#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Advent of Code Day 10."""

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
# Part One
# ----------------------------------------------------------------------------------------
def part1(history):
    "Sum the signal strengths at select cycles."
    strengths = []
    for chosen in [20, 60, 100, 140, 180, 220]:
        (cycle, X) = history[chosen-1]
        strengths.append(cycle * X)
    debug(strengths)
    print(sum(strengths))

# ----------------------------------------------------------------------------------------
# Part Two
# ----------------------------------------------------------------------------------------
def part2(history):
    "Render the screen image."
    row = 0
    column = 0
    for (cycle, X) in history:
        # If the raster column is one before X, on X, or after, light the pixel.
        if column == (X-1) or column == X or column == (X+1):
            print("#", end = '')
        # Otehrwise the pixel is dark.
        else:
            print(".", end = '')
        # Advance to the next raster column on the next cycle.
        column += 1
        # If we're in the laster column, return to the first column on the next line.
        if cycle % 40 == 0:
            row += 1
            column = 0
            print()

# ----------------------------------------------------------------------------------------
# Shared
# ----------------------------------------------------------------------------------------
def read_input():
    "Process the challenge input, execute, and produce an execution history."
    # The value of the X register.
    X = 1
    # The cycle number.
    cycle = 1
    # The history of the machine state.
    history = []
    for line in sys.stdin:
        line = line.rstrip()
        # Addx takes two cycles, and adds the value to X.
        if line.startswith("addx "):
            history.append((cycle, X))
            cycle += 1
            history.append((cycle, X))
            cycle += 1
            X += int(line[5:])
        # Noop takes 1 cycle and does not change X.
        elif line == "noop":
            history.append((cycle, X))
            cycle += 1
    # Add one final cycle.
    history.append((cycle, X))
    # Report the entire history for debugging.
    for (cycle, X) in history:
        debug("cycle=%d X=%d strength=%d" % (cycle, X, cycle * X))
    # And return it.
    return history

if __name__ == '__main__':
    history = read_input()
    if options.part == 1:
        part1(history)
    else:
        part2(history)

# Part one solution for test-input1 is: 13140
# Part two solution for test-input2 is:
# ##..##..##..##..##..##..##..##..##..##..
# ###...###...###...###...###...###...###.
# ####....####....####....####....####....
# #####.....#####.....#####.....#####.....
# ######......######......######......####
# #######.......#######.......#######.....
# Part one solution for input is: 16060
# Part two solution for input is: BACEKHLF
# ###...##...##..####.#..#.#....#..#.####.
# #..#.#..#.#..#.#....#.#..#....#..#.#....
# ###..#..#.#....###..##...#....####.###..
# #..#.####.#....#....#.#..#....#..#.#....
# #..#.#..#.#..#.#....#.#..#....#..#.#....
# ###..#..#..##..####.#..#.####.#..#.#....

# Local Variables:
# mode: python
# fill-column: 90
# eval: (flyspell-buffer)
# eval: (column-number-mode)
# End:
