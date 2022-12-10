#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Advent of Code Day 1."""

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
    "Read the challenge input."
    sums = []
    s = 0
    for line in sys.stdin:
        line = line.rstrip()
        if line == '':
            sums.append(s)
            s = 0
        else:
            s += int(line)

    sums.append(s)
    return sums

if __name__ == '__main__':
    sums = read_input()
    if options.part == 1:
        debug(sums)
        print(max(sums))
    else:
        debug(sorted(sums)[-3:])
        print(sum(sorted(sums)[-3:]))

# Part one solution for test-input1 is: 24000
# Part two solution for test-input1 is: 45000
# Part one solution for input is: 66186
# Part two solution for input is: 196804

# Local Variables:
# mode: python
# fill-column: 90
# eval: (flyspell-buffer)
# eval: (column-number-mode)
# End:
