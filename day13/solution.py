#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Advent of Code Day 13."""

import sys
import functools
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
    "Solve part 1, determine which packets are in the correct order."
    # Read the packets in pairs, and evaluate to convert to Python lists.
    pairs = []
    pair = []
    for line in sys.stdin:
        line = line.rstrip()
        if line != '':
            packet = eval(line)
            pair.append(packet)
            if len(pair) == 2:
                pairs.append(pair)
                pair = []

    # For each pair of packets determine if they're in the correct order.
    correct_order = []
    for n, pair in enumerate(pairs):
        (left, right) = pair
        debug("== Pair %s ==" % (n+1))
        if compare(left, right) == -1:
            correct_order.append(n+1)
        debug()
    # Report the pairs that were in the correct order.
    debug("The pairs in the correct order are: %s" % str(correct_order))
    print(sum(correct_order))

# ----------------------------------------------------------------------------------------
# Part Two
# ----------------------------------------------------------------------------------------
def part2():
    "Solve part 2, placing the packets in the correct order and locating dividers."
    packets = []
    for line in sys.stdin:
        line = line.rstrip()
        if line != '':
            packet = eval(line)
            packets.append(packet)
    # Add the two divider packets.
    divider2 = [[2]]
    packets.append(divider2)
    divider6 = [[6]]
    packets.append(divider6)
    # Sort the packets.
    sorted_packets = sorted(packets, key=functools.cmp_to_key(compare))

    # Display the sorted packets and determine where the dividers are located.
    debug()
    debug("The sorted list of packets is:")
    dividers = []
    for n, packet in enumerate(sorted_packets):
        if packet == divider2:
            dividers.append(n+1)
        elif packet == divider6:
            dividers.append(n+1)
        debug(packet)
    # Display the locations of the dividers and compute the answer.
    debug()
    debug("Dividers are at positions: %s and %s" % (dividers[0], dividers[1]))
    print(dividers[0] * dividers[1])

# ----------------------------------------------------------------------------------------
# Shared
# ----------------------------------------------------------------------------------------
def compare(left, right, indent=''):
    "Return -1 if left comes before right, -1 if not, and zero if equal."
    debug("%s- Compare %s vs %s" % (indent, left, right))
    mixed_msg = "%s    - Mixed types; convert %s to %s and retry comparison"
    int_msg = "%s    - %s side is smaller, so inputs are %sin the right order"
    for left_value, right_value in zip(left, right):
        if isinstance(left_value, int) and isinstance(right_value, int):
            debug("%s  - Compare %s vs %s" % (indent, left_value, right_value))
            if left_value < right_value:
                debug(int_msg % (indent, "Left", ""))
                return -1
            elif left_value > right_value:
                debug(int_msg % (indent, "Right", "not "))
                return 1
        elif isinstance(left_value, list) and isinstance(right_value, list):
            decision = compare(left_value, right_value, indent + "  ")
            if decision != 0:
                return decision
        elif isinstance(left_value, int) and isinstance(right_value, list):
            debug(mixed_msg % (indent, "left", [left_value]))
            decision = compare([left_value], right_value, indent + "    ")
            if decision != 0:
                return decision
        elif isinstance(left_value, list) and isinstance(right_value, int):
            debug(mixed_msg % (indent, "right", [right_value]))
            decision = compare(left_value, [right_value], indent + "    ")
            if decision != 0:
                return decision

    if len(left) < len(right):
        debug("  - Left side ran out of terms, so inputs are in the right order")
        return -1
    elif len(left) > len(right):
        debug("  - Right side ran out of terms, so inputs are not in the right order")
        return 1
    # Both sides had the same number of elements.
    debug("    - Both sides were the same length, continue with next element")
    return 0

if __name__ == '__main__':
    if options.part == 1:
        part1()
    else:
        part2()

# Part one solution for test-input1 is: 13
# Part two solution for test-input2 is: 140
# Part one solution for input is: 5031
# Part two solution for input is: 25038

# Local Variables:
# mode: python
# fill-column: 90
# eval: (flyspell-buffer)
# eval: (column-number-mode)
# End:
