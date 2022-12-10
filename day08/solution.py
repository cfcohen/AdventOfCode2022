#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Advent of Code Day 8."""

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
def look_direction(grid, row, column, row_direction, column_direction, height = None):
    """
    Return true if the tree is visible from the edge looking in a certain direction.
    """
    if height is None:
        height = grid[row][column]
    # All trees on the border are visible.
    if row == 0 or column == 0 or row == len(grid) - 1 or column == len(grid[0]) - 1:
        return True
    # Otherwise the visibility of this tree is based on the height of the neighbors
    neighbor_row = row + row_direction
    neighbor_column = column + column_direction
    neighbor_height = grid[neighbor_row][neighbor_column]
    # If the neighboring tree blocks the view from the edge of the grid, this tree is not
    # visible.
    if neighbor_height >= height:
        return False
    # Otherwise we need to keep looking in the same direction from the neighbor.
    return look_direction(grid, neighbor_row, neighbor_column,
                          row_direction, column_direction, height)

# ----------------------------------------------------------------------------------------
def tree_is_visible(grid, row, column):
    "Return true if the tree at row and column is visible from the edge."
    if look_direction(grid, row, column, 1, 0):
        return True
    if look_direction(grid, row, column, -1, 0):
        return True
    if look_direction(grid, row, column, 0, 1):
        return True
    if look_direction(grid, row, column, 0, -1):
        return True
    return False

# ----------------------------------------------------------------------------------------
def part1(grid):
    "Count the trees that can be seen from the edge of the grid."
    count = 0
    height = len(grid)
    width = len(grid[0])
    for row in range(height):
        for column in range(width):
            if tree_is_visible(grid, row, column):
                debug("Tree of height %s at (%d, %s) is visible" % (
                    grid[row][column], row, column))
                count += 1
    print(count)

# ----------------------------------------------------------------------------------------
# Part Two
# ----------------------------------------------------------------------------------------
def count_trees(grid, row, column, row_direction, column_direction, height = None):
    "Return the number of trees visible from a given tree."
    # If no height was provided, use the height of the current tree.
    if height is None:
        height = grid[row][column]
    # All trees on the border are visible.
    if row == 0 or column == 0 or row == len(grid) - 1 or column == len(grid[0]) - 1:
        return 0
    # Otherwise the visibility of this tree is based on the height of the neighbors
    neighbor_row = row + row_direction
    neighbor_column = column + column_direction
    neighbor_height = grid[neighbor_row][neighbor_column]
    # If the neighboring tree blocks the view from the edge of the grid...
    if neighbor_height >= height:
        return 1
    # Otherwise we can see this tree and some additional number in the direction we're looking.
    return 1 + count_trees(grid, neighbor_row, neighbor_column,
                           row_direction, column_direction, height)

# ----------------------------------------------------------------------------------------
def scenic_score(grid, row, column):
    "Return the scenic score for a tree."
    up = count_trees(grid, row, column, 0, -1)
    left = count_trees(grid, row, column, -1, 0)
    down = count_trees(grid, row, column, 0, 1)
    right = count_trees(grid, row, column, 1, 0)
    ss = up * left * down * right
    debug("  scenic score: (%d, %d), height=%s = %d * %d * %d * %d = %d)" % (
        row, column, grid[row][column], up, left, down, right, ss))
    return ss

def part2(grid):
    "Choose the best scenic score from all of the trees."
    best = 0
    height = len(grid)
    width = len(grid[0])
    for row in range(height):
        for column in range(width):
            ss = scenic_score(grid, row, column)
            if ss > best:
                debug("best scenic score at: (%s, %s) is %s" % (row, column, ss))
                best = ss
    print(best)

# ----------------------------------------------------------------------------------------
# Shared
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
def debug_grid(grid):
    "Display the gyrocopter tree height grid."
    for row in grid:
        debug(row)

# ----------------------------------------------------------------------------------------
def read_input():
    "Read the challenge input."
    grid = []
    for line in sys.stdin:
        line = line.rstrip()
        grid.append(list(line))
    return grid

if __name__ == '__main__':
    grid = read_input()
    debug_grid(grid)
    if options.part == 1:
        part1(grid)
    else:
        part2(grid)

# Part one solution for test-input1 is: 21
# Part two solution for test-input1 is: 8
# Part one solution for input is: 1859
# Part two solution for input is: 332640

# Local Variables:
# mode: python
# fill-column: 90
# eval: (flyspell-buffer)
# eval: (column-number-mode)
# End:
