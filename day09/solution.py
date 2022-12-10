#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Advent of Code Day 9."""

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
def move_knot(head_pos, tail_pos):
    "Return the new tail position based on the head position."
    # Is the tail adjacent to the head in the horizontal or vertical dimension?
    near_vertical = abs(tail_pos[1] - head_pos[1]) <= 1
    near_horizontal = abs(tail_pos[0] - head_pos[0]) <= 1
    # Is the tail near the head?
    near = near_horizontal and near_vertical

    # The tail only moves if it is not near the head.
    if not near:
        # The head is to the right of the tail.
        if tail_pos[0] < head_pos[0]:
            tail_pos = (tail_pos[0] + 1, tail_pos[1])
        # The head is to the left of the tail.
        elif tail_pos[0] > head_pos[0]:
            tail_pos = (tail_pos[0] - 1, tail_pos[1])

        # The head is above the tail.
        if tail_pos[1] < head_pos[1]:
            tail_pos = (tail_pos[0], tail_pos[1] + 1)
        # The head is below the tail.
        elif tail_pos[1] > head_pos[1]:
            tail_pos = (tail_pos[0], tail_pos[1] - 1)
    return tail_pos

# ----------------------------------------------------------------------------------------
def read_input(num_knots):
    # The position of each knot.
    # Right is positive, left is negative, up is postive, down is negative.
    # (0, 0) is the starting location.
    knots = [(0, 0)] * num_knots
    visited = set()
    for line in sys.stdin:
        line = line.rstrip()
        (direction, amount) = line.split()
        debug(direction, amount)
        # One step at a time...
        for step in range(int(amount)):
            # Move the head.
            if direction == 'R':
                knots[0] = (knots[0][0] + 1, knots[0][1])
            elif direction == 'L':
                knots[0] = (knots[0][0] - 1, knots[0][1])
            elif direction == 'U':
                knots[0] = (knots[0][0], knots[0][1] + 1)
            elif direction == 'D':
                knots[0] = (knots[0][0], knots[0][1] - 1)

            # Have the other knots follow.
            for i in range(num_knots-1):
                previous_knot = knots[i]
                knots[i+1] = move_knot(previous_knot, knots[i+1])

            # Report the position of the head and the tail.
            debug("  head=%s tail=%s" % (knots[0], knots[num_knots-1]))
            # The tail has visited this position.
            visited.add(knots[num_knots-1])
    return visited

if __name__ == '__main__':
    if options.part == 1:
        visited = read_input(2)
    else:
        visited = read_input(10)
    print(len(visited))

# Part one solution for test-input1 is: 13
# Part two solution for test-input2 is: 36
# Part one solution for input is: 6384
# Part two solution for input is: 2734

# Local Variables:
# mode: python
# fill-column: 90
# eval: (flyspell-buffer)
# eval: (column-number-mode)
# End:
