#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Advent of Code Day 6."""

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

# ----------------------------------------------------------------------------------------
# Part Two
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Shared
# ----------------------------------------------------------------------------------------
def read_input(size):
    "Read the challenge input and solve it."
    # Input is only one line, but the test-input was several.  Each line is a separate test.
    for line in sys.stdin:
        line = line.rstrip()
        # The buffer containing size most recent characters.
        buff = []
        # The current position in the message.
        pos = 1
        # The message is composed of characters.
        for char in line:
            # Add the new character to the buffer.
            buff.append(char)
            # If the buffer is too big (>size characters), remove the oldest character.
            if len(buff) > size:
                buff.pop(0)
            debug("buff=%4s set=%4s" % (''.join(buff), ''.join(set(buff))))
            # If we have a full buffer and there are size unique characters in the buffer,
            # then this is our solution.
            if len(buff) == size and len(set(buff)) == size:
                print(pos)
                break
            # Advance to the next character.
            pos += 1

if __name__ == '__main__':
    if options.part == 1:
        read_input(4)
    else:
        read_input(14)

# Part one solution for test-input1 is: 7,5,6,10,11
# Part two solution for test-input1 is: 19,23,23,29,26
# Part one solution for input is: 1582
# Part two solution for input is: 3588

# Local Variables:
# mode: python
# fill-column: 90
# eval: (flyspell-buffer)
# eval: (column-number-mode)
# End:
