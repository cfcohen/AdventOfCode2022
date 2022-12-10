#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Advent of Code Day 2."""

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
def part1(play):
    "Convert XYZ to the same play (ABC) as my opponent."
    return {"X": "A", "Y": "B", "Z": "C"}[play]

# ----------------------------------------------------------------------------------------
# Part Two
# ----------------------------------------------------------------------------------------
def part2(opponent, strategy):
    "Choose my play based on the recommended strategy."
    # lose
    if strategy == "X":
        lose = {"A": "C", "B": "A", "C": "B"}
        return lose[opponent]
    # draw
    elif strategy == "Y":
        return opponent
    # win
    else:
        win = {"A": "B", "B": "C", "C": "A"}
        return win[opponent]

# ----------------------------------------------------------------------------------------
# Shared
# ----------------------------------------------------------------------------------------
# The score earned based on your play.
play_score = { "A": 1, "B": 2, "C": 3}

def round_score(opponent, me):
    "Return the score for winning or losing the round."
    # draw
    if opponent == me:
        return 3
    # lose
    if ((opponent == "C" and me == "B")
        or (opponent == "B" and me == "A")
        or (opponent == "A" and me == "C")):
        return 0
    # win
    return 6

# ----------------------------------------------------------------------------------------
def read_input(part):
    "Read the challenge input and solve it."
    score = 0
    for line in sys.stdin:
        line = line.rstrip()
        (opponent, strategy) = line.split()
        # Choose my play based on which strategy guide we're uding (part1 or part2).
        if part == 1:
            me = part1(strategy)
        else:
            me = part2(opponent, strategy)
        # Increment my score by the results for this round.
        score += (play_score[me] + round_score(opponent, me))
    print(score)


if __name__ == '__main__':
    read_input(options.part)

# Part one solution for test-input1 is: 15
# Part two solution for test-input1 is: 12
# Part one solution for input is: 10595
# Part two solution for input is: 9541

# Local Variables:
# mode: python
# fill-column: 90
# eval: (flyspell-buffer)
# eval: (column-number-mode)
# End:
