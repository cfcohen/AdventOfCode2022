#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Advent of Code Day 4."""

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
def part1(elf1, elf2):
    "Return one if one elf is a subset of the other, otherwise zero."
    if elf1.issubset(elf2) or elf2.issubset(elf1):
        return 1
    return 0

# ----------------------------------------------------------------------------------------
# Part Two
# ----------------------------------------------------------------------------------------
def part2(elf1, elf2):
    "Return one if the two elves overlap, otherwise zero."
    if len(elf1.intersection(elf2)) > 0:
        return 1
    return 0

# ----------------------------------------------------------------------------------------
# Shared
# ----------------------------------------------------------------------------------------
def read_input(part):
    "Read the challenge input and solve it."
    count = 0
    for line in sys.stdin:
        line = line.rstrip()
        # Split line into two elves.
        (elf1, elf2) = line.split(',')
        # Convert each elf into a min and max for the range.
        (elf1min, elf1max) = elf1.split('-')
        (elf2min, elf2max) = elf2.split('-')
        # Make sets for each elf.
        elf1set = set(range(int(elf1min), int(elf1max) + 1))
        elf2set = set(range(int(elf2min), int(elf2max) + 1))
        if part == 1:
            count += part1(elf1set, elf2set)
        else:
            count += part2(elf1set, elf2set)
        debug("count=%s elf1=%s elf2=%s" % (count, elf1set, elf2set))
    print(count)

if __name__ == '__main__':
    read_input(options.part)

# Part one solution for test-input1 is: 2
# Part two solution for test-input1 is: 4
# Part one solution for input is: 560
# Part two solution for input is: 839

# Local Variables:
# mode: python
# fill-column: 90
# eval: (flyspell-buffer)
# eval: (column-number-mode)
# End:
