#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Advent of Code Day 5."""

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
def move_crates_part1(stacks, count, from_stack, to_stack):
    # Implement the move, one crate at a time.
    for c in range(count):
        crate = stacks[from_stack].pop()
        stacks[to_stack].append(crate)

# ----------------------------------------------------------------------------------------
# Part Two
# ----------------------------------------------------------------------------------------
def move_crates_part2(stacks, count, from_stack, to_stack):
    # Implement the move, all crates at once.
    crates = stacks[from_stack][-count:]
    stacks[from_stack] = stacks[from_stack][:-count]
    stacks[to_stack].extend(crates)

# ----------------------------------------------------------------------------------------
# Shared
# ----------------------------------------------------------------------------------------
def debug_stacks(stacks):
    "Print the stacks for debugging.  Stack top is on right."
    for n, stack in enumerate(stacks[1:]):
        debug("  ", n + 1, ''.join(stack))

# ----------------------------------------------------------------------------------------
def read_input(part):
    "Read the challenge input and solve it."
    # Our stacks. The zero element is unused.
    stacks = []
    for line in sys.stdin:
        line = line.rstrip()
        if line.startswith("move"):
            (move, count, from_word, from_stack, to_word, to_stack) = line.split()
            count = int(count)
            from_stack = int(from_stack)
            to_stack = int(to_stack)
            print("Move count=%d from=%d to=%d" % (count, from_stack, to_stack))
            # Move the crates, using the strategy from part 1 or part 2.
            if part == 1:
                move_crates_part1(stacks, count, from_stack, to_stack)
            else:
                move_crates_part2(stacks, count, from_stack, to_stack)
            # Report the stacks after the move.
            debug_stacks(stacks)
        elif line == '':
            # Report the stacks after initialization.
            debug_stacks(stacks)
        else:
            # Initialize the stacks (first lines in input)
            pos = 1
            stack = 1
            while pos < len(line):
                letter = line[pos]
                # Ignore the line that labels the stacks.
                if letter == '1':
                    break
                # If we've not created the stack yet, do so now.
                while len(stacks) - 1 < stack:
                    stacks.append([])
                # Skip stacks that have no crate in this position
                if letter != ' ':
                    stacks[stack].insert(0, letter)
                # Advance to next location in line, and next stack.
                pos += 4
                stack += 1

    answer = []
    for stack in stacks[1:]:
        if len(stack) > 0:
            answer.append(stack[-1])
    print(''.join(answer))

if __name__ == '__main__':
    read_input(options.part)

# Part one solution for test-input1 is: CMZ
# Part two solution for test-input1 is: MCD
# Part one solution for input is: VWLCWGSDQ
# Part two solution for input is: TCGLQSLPW

# Local Variables:
# mode: python
# fill-column: 90
# eval: (flyspell-buffer)
# eval: (column-number-mode)
# End:
