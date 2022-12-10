#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Advent of Code Day 7."""

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
def part1(fs):
    "Report the total size of all directories < 100000 bytes in size."
    total = visit_filesystem1(fs)
    print(total)

# ----------------------------------------------------------------------------------------
def visit_filesystem1(fs):
    "Report the total size of all directories < 100000 bytes in size."
    total = 0
    for f in fs:
        if isinstance(fs[f], dict):
            total += visit_filesystem1(fs[f])
    size = fs['=']
    if size < 100000:
        total += size
    return total

# ----------------------------------------------------------------------------------------
# Part Two
# ----------------------------------------------------------------------------------------
def part2(fs):
    "Report how much disk space was freed by deleting a directory."
    # This is how much disk space is in the entire disk.
    total_space = 70000000
    # This is how much disk space is required to install the update.
    space_required = 30000000
    # This is how much disk space is already free on the drive.
    space_free = total_space - fs['/']['=']
    # This is how much additional disk space needs to be freed.
    space_to_be_deleted = space_required - space_free
    # Calculate how much disk space is freed by deleting the best size directory.
    freed = visit_filesystem2(fs, space_to_be_deleted, space_required)
    print(freed)

# ----------------------------------------------------------------------------------------
def visit_filesystem2(fs, required, best):
    """
    Return the best size directory found in the fiulesystem so far.

    Required is the target disk space to be freed, and the best is the closest directory
    size found so far.
    """
    # Consider all subdirectories of this directory...
    for f in fs:
        if isinstance(fs[f], dict):
            new_best = visit_filesystem2(fs[f], required, best)
            if new_best >= required and new_best < best:
                best = new_best
    # Is this directory the best sized directory?
    size = fs['=']
    if size >= required and size < best:
        best = size
    return best

# ----------------------------------------------------------------------------------------
# Shared
# ----------------------------------------------------------------------------------------
def fs_pwd(fs, pwd):
    "Return the directory of the filesystem corresponding with pwd."
    tfs = fs
    for d in pwd:
        tfs = tfs[d]
    return tfs

# ----------------------------------------------------------------------------------------
def compute_size(fs):
    "Compute the size of the directory and store it in a file named '='."
    size = 0
    for f in fs:
        if isinstance(fs[f], dict):
            size += compute_size(fs[f])
        else:
            size += fs[f]
    fs['='] = size
    return size

# ----------------------------------------------------------------------------------------
def debug_filesystem(fs, indent=''):
    "Display the contents of the filesystem."
    for f in sorted(fs):
        if isinstance(fs[f], dict):
            debug('%s- %s (dir)' % (indent, f))
            debug_filesystem(fs[f], indent + '  ')
        else:
            debug('%s  - %s (file, size=%s)' % (indent, f, fs[f]))

# ----------------------------------------------------------------------------------------
def read_input():
    "Read the challenge input."
    fs = {"/": {} }
    pwd = ["/"]
    for line in sys.stdin:
        line = line.rstrip()
        if line.startswith('$ '):
            if line.startswith('$ ls'):
                # Lines will be handled in the else case.
                pass
            elif line.startswith('$ cd '):
                parameter = line[5:]
                if parameter == '/':
                    pwd = ["/"]
                elif parameter == '..':
                    pwd.pop()
                else:
                    pwd.append(parameter)
                #print("PWD is now: %s" % (pwd))
            else:
                print("unexpected command: %s" % line, file=sys.stderr)
        else:
            tfs = fs_pwd(fs, pwd)
            if line.startswith("dir "):
                newdir = line[4:]
                if newdir not in tfs:
                    tfs[newdir] = {}
            else:
                (size, name) = line.split()
                if name not in tfs:
                    tfs[name] = int(size)
                else:
                    print("unexpected duplicate: %s" % line, file=sys.stderr)
    return fs

if __name__ == '__main__':
    fs = read_input()
    compute_size(fs)
    debug_filesystem(fs)
    if options.part == 1:
        part1(fs)
    else:
        part2(fs)

# Part one solution for test-input1 is: 95437
# Part two solution for test-input1 is: 24933642
# Part one solution for input is: 1391690
# Part two solution for input is: 5469168

# Local Variables:
# mode: python
# fill-column: 90
# eval: (flyspell-buffer)
# eval: (column-number-mode)
# End:
