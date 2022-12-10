#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Advent of Code Day X."""

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
def part1():
    pass

# ----------------------------------------------------------------------------------------
# Part Two
# ----------------------------------------------------------------------------------------
def part2():
    pass

# ----------------------------------------------------------------------------------------
# Shared
# ----------------------------------------------------------------------------------------
def read_input():
    for line in sys.stdin:
        line = line.rstrip()
        pass

if __name__ == '__main__':

    if options.part == 1:
        pass
    else:
        pass

# Part one solution for test-input1 is:
# Part two solution for test-input2 is:
# Part one solution for input is:
# Part two solution for input is:

# Local Variables:
# mode: python
# fill-column: 90
# eval: (flyspell-buffer)
# eval: (column-number-mode)
# End:
