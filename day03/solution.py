#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Advent of Code Day 3."""

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
    total = 0
    for line in sys.stdin:
        line = line.rstrip()
        # Split into two compartments.
        compartment1 = set(line[:int(len(line)/2)])
        compartment2 = set(line[int(len(line)/2):])
        # Find the intersection between the two compartments.
        shared = compartment1.intersection(compartment2).pop()
        # Get the prirority for that item.
        priority = priorities.index(shared) + 1
        # Add to the total.
        total += priority
        # Report the result when debugging.
        debug("shared=%s priority=%s total=%s" % (shared, priority, total))
    print(total)

# ----------------------------------------------------------------------------------------
# Part Two
# ----------------------------------------------------------------------------------------
def part2():
    total = 0
    group = []
    for line in sys.stdin:
        line = line.rstrip()
        group.append(line)
        # Once we've read three lines, we have a group of elves.
        if len(group) == 3:
            # Make sets for each elf.
            elf1 = set(group[0])
            elf2 = set(group[1])
            elf3 = set(group[2])
            # Find the intersection (the badge item).
            badge = elf1.intersection(elf2.intersection(elf3)).pop()
            # Get the prirority for that item.
            priority = priorities.index(badge) + 1
            # Add to the total.
            total += priority
            # Report the result when debugging.
            debug("badge=%s priority=%s total=%s" % (badge, priority, total))
            # Clear the group list for the next group.
            group = []
    print(total)

# ----------------------------------------------------------------------------------------
# Shared
# ----------------------------------------------------------------------------------------
# The priorities for each letter.
priorities = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

if __name__ == '__main__':
    if options.part == 1:
        part1()
    else:
        part2()

# Part one solution for test-input1 is: 157
# Part two solution for test-input1 is: 70
# Part one solution for input is: 7826
# Part two solution for input is: 2577

# Local Variables:
# mode: python
# fill-column: 90
# eval: (flyspell-buffer)
# eval: (column-number-mode)
# End:
