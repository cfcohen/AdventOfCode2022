#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Advent of Code Day 15."""

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
def part1(sensors):
    "Solve part one, counting the number of blocked cells on a given line."
    if len(sensors) == 14:
        linenum = 10
    else:
        linenum = 2000000
    blocked_ranges = evaluate_line(sensors, linenum)
    print(count_blocked(blocked_ranges)-1)

def evaluate_line(sensors, lnum):
    "Calculate the ranges of cells blocked by each sensor on a given line."
    blocked_ranges = []
    for sensor in sensors:
        (sx, sy, bx, by) = sensor
        distance_to_beacon = abs(sx-bx) + abs(sy-by)
        debug("Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d, distance=%d" % (
            sx, sy, bx, by, distance_to_beacon))
        vertical_distance = abs(lnum-sy)
        debug("  Vertical distance to line %d is %d" % (lnum, vertical_distance))
        width_on_line = distance_to_beacon - vertical_distance
        debug("  Horizontal width on line %d is %d" % (lnum, width_on_line))
        if width_on_line > 0:
            minx = sx - width_on_line
            maxx = sx + width_on_line
            debug("  Beacon at (%d, %d) blocks range (%d, %d) to (%d, %d)!" % (
                sx, sy, lnum, minx, lnum, maxx))
            blocked_ranges.append((minx, maxx))
    debug("Blocked column ranges for line=%d are: %s" % (lnum, blocked_ranges))
    return blocked_ranges

def count_blocked(blocked_ranges):
    "Count the number of blocked cells in the given list of ranges."
    count = 0
    pmax = None
    for blocked in sorted(blocked_ranges, key=lambda x: x[0]):
        (minx, maxx) = blocked
        if pmax is None:
            count = (maxx - minx) + 1
            debug("Range (%d, %d) blocked %d cells" % (minx, maxx, count))
            pmax = maxx
        elif minx <= pmax + 1 and maxx >= pmax + 1:
            count += (maxx - pmax)
            debug("Range (%d, %d) blocked %d additional cells, total=%d" % (
                minx, maxx, maxx - pmax, count))
            pmax = maxx
    return count

# ----------------------------------------------------------------------------------------
# Part Two
# ----------------------------------------------------------------------------------------
def part2(sensors):
    """
    Solve part two, find the one location where the disress beacon can be located.

    This one was very difficult for me, but then very easy to code once I saw the
    solution.  The key insight is that if there's only one possible location for the
    distress beacon, then that location must be exactly one cell farther from a sensor
    than the distance to the nearest beacon for that sensor.  If the distress beacon was
    two cells more distant, then there would be more than one solution (the found location
    AND the location one closer).

    Further, when you're considering a given location for the distress beacon, you only
    need to see whether it would be closer to any other sensor than that sensor's current
    beacon.  If your proposed location of the distress beacon was closer, the distress
    beacon would have been reported as the closest beacon for that sensor -- but it
    wasn't, so the location is incorrect.  When no sensor contradicts your proposed
    location, that must be the solution, because if any different location met that
    criteria, then there would be more than one solution, and the challenge states clearly
    that there is only one location that the distress beacon can be at.
    """
    if len(sensors) == 14:
        limit = 20
    else:
        limit = 4000000
    # Visit each sensor to evaluate all candidate locations for the distress beacon on the
    # border of the blocked region for this sensor.
    for sensor1 in sensors:
        (sx, sy, bx, by) = sensor1
        distance = abs(sx-bx) + abs(sy-by)
        debug("Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d, distance=%d" % (
            sx, sy, bx, by, distance))
        # Check candidate positions on the upper edge of the excluded area.
        (cx, cy) = consider_candidates(sensors, sx, sy, distance+1, limit)
        # If the proposed solution was no explicitly rejected, this is our solution!
        if cx != -1:
            print(cx * 4000000 + cy)
            break

def consider_candidate(sensors, x, y):
    """
    Evaluate whether the proposed location for the distress beacon is correct.

    Return true if it is, and False if it is not.
    """
    for sensor in sensors:
        (sx, sy, bx, by) = sensor
        sensor_to_beacon = abs(sx-bx) + abs(sy-by)
        candidate_to_sensor = abs(sx-x) + abs(sy-y)
        debug("      Considering sensor at (%d, %d) beacon=(%d, %d)" % (sx, sy, bx, by))
        if candidate_to_sensor <= sensor_to_beacon:
            debug("      Candidate (%d, %d) is too close to sensor (%d, %d), distance=%d" % (
                x, y, sx, sy, candidate_to_sensor))
            return False
    debug("    No beacon was closer to (%d, %d)!" % (x, y))
    return True

def consider_sweep(sensors, x, y, d, limit, xdir, ydir):
    "Consider candidates on one diagonal sweep on the border the sensor's blocked area."
    for v in range(0, d + 1):
        cx = x + (v * xdir)
        cy = y + (d - (v * ydir))
        if cx > limit or cy > limit or cx < 0 or cy < 0:
            continue
        debug("    Candidate location is: (%d, %d)" % (cx, cy))
        if consider_candidate(sensors, cx, cy):
            return (cx, cy)
    return (-1, -1)

def consider_candidates(sensors, x, y, d, limit):
    "Consider the locations on the bounary of a blocked area for a given sensor."
    debug("  Considering candidates for sensor (%d, %d) distance=%d" % (x, y, d))
    # Lower right
    (cx, cy) = consider_sweep(sensors, x, y, d, limit, 1, 1)
    if cx != -1:
        return (cx, cy)
    # Lower left
    (cx, cy) = consider_sweep(sensors, x, y, d, limit, -1, 1)
    if cx != -1:
        return (cx, cy)
    # Upper right
    (cx, cy) = consider_sweep(sensors, x, y, d, limit, 1, -1)
    if cx != -1:
        return (cx, cy)
    # Upper left
    (cx, cy) = consider_sweep(sensors, x, y, d, limit, -1, -1)
    if cx != -1:
        return (cx, cy)
    # No candidate locations bordering this sensor were valid.
    return (-1, -1)

# ----------------------------------------------------------------------------------------
# Shared
# ----------------------------------------------------------------------------------------
def read_input():
    "Read the challenge input, and return a list of sensors."
    sensors = []
    for line in sys.stdin:
        line = line.rstrip()
        line = line.replace("Sensor at x=", "")
        line = line.replace(": closest beacon is at x=", ", ")
        line = line.replace("y=", "")
        (sx, sy, bx, by) = line.split(",")
        sx = int(sx)
        sy = int(sy)
        bx = int(bx)
        by = int(by)
        sensors.append((sx, sy, bx, by))
    return sensors

if __name__ == '__main__':
    sensors = read_input()
    if options.part == 1:
        part1(sensors)    else:
        part2(sensors)

# Part one solution for test-input1 is: 26
# Part two solution for test-input2 is: 56000011
# Part one solution for input is: 5142231
# Part two solution for input is: 10884459367718

# Local Variables:
# mode: python
# fill-column: 90
# eval: (flyspell-buffer)
# eval: (column-number-mode)
# End:
