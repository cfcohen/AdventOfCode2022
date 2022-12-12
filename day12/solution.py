#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Advent of Code Day 12."""

import sys
from optparse import OptionParser
from collections import defaultdict

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
def part1(graph):
    "Solve part1, which is to find the shortest path from start to goal."
    path = dijsktra(graph, 'start', 'goal')
    debug(path)
    # Print the length of the shortest path.
    print(len(path) - 3)

# ----------------------------------------------------------------------------------------
# Part Two
# ----------------------------------------------------------------------------------------
def part2(graph, elevations):
    """
    Solve part2, find a starting location that provides the shortest path to the goal.

    The starting location must at elevation 'a'.
    """
    bestlen = None
    bestpath = None
    for row in range(len(elevations)):
        for col in range(len(elevations[row])):
            # The starting location must be at elevation 'a', and must have an adjacent
            # cell at elevation 'b'.
            if elevations[row][col] == 'a' and adjacentb(elevations, row, col):
                src = "%d-%d" % (row, col)
                graph.add_edge('start', src, 0)
                path = dijsktra(graph, 'start', 'goal')
                pathlen = len(path) - 3
                if bestlen is None or pathlen < bestlen:
                    bestlen = pathlen
                    bestpath = path
                    debug("New shortest path is %d steps" % (bestlen))
                graph.remove_start(src)
    debug(bestpath)
    print(bestlen)

def adjacentb(elevations, row, col):
    """
    Return True if there is an elevation 'b' adjacent to (r,c).

    Performance without this optimization is kind of bad, so I added it to speed things
    up.  In my input at least, there were a lot of cells with elevation 'a' and very few
    cells with elevation 'b'.
    """
    # East
    if allowed(elevations, row, col+1, elevations[row][col]):
        if elevations[row][col+1] == 'b':
            return True
    # West
    if allowed(elevations, row, col-1, elevations[row][col]):
        if elevations[row][col-1] == 'b':
            return True
    # North
    if allowed(elevations, row-1, col, elevations[row][col]):
        if elevations[row-1][col] == 'b':
            return True
    # South
    if allowed(elevations, row+1, col, elevations[row][col]):
        if elevations[row+1][col] == 'b':
            return False

# ----------------------------------------------------------------------------------------
# Shared
# ----------------------------------------------------------------------------------------
def debug_elevations(elevations):
    for row in elevations:
        debug(''.join(row))

# Dijsktra's algorithm courtesy of:
# https://benalexkeen.com/implementing-djikstras-shortest-path-algorithm-with-python/
class Graph():
    def __init__(self):
        """
        self.edges is a dict of all possible next nodes
        e.g. {'X': ['A', 'B', 'C', 'E'], ...}
        self.weights has all the weights between two nodes,
        with the two nodes as a tuple as the key
        e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
        """
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        self.edges[from_node].append(to_node)
        self.weights[(from_node, to_node)] = weight
        #print("Adding edge %s -> %s, weight=%s" % (from_node, to_node, weight))

    def remove_start(self, to_node):
        self.edges['start'] = []
        del self.weights[('start', to_node)]

def dijsktra(graph, initial, end):
    "Return the shortest path from initial to end."
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path

def elevations2graph(elevations, start, goal):
    "Convert the elevations map to a graph with edges indicating allowed movement."
    graph = Graph()
    for row in range(len(elevations)):
        for col in range(len(elevations[row])):
            src = "%d-%d" % (row, col)
            # East
            if allowed(elevations, row, col+1, elevations[row][col]):
                dst = "%d-%d" % (row, col+1)
                graph.add_edge(src, dst, 1)
            # West
            if allowed(elevations, row, col-1, elevations[row][col]):
                dst = "%d-%d" % (row, col-1)
                graph.add_edge(src, dst, 1)
            # North
            if allowed(elevations, row-1, col, elevations[row][col]):
                dst = "%d-%d" % (row-1, col)
                graph.add_edge(src, dst, 1)
            # South
            if allowed(elevations, row+1, col, elevations[row][col]):
                dst = "%d-%d" % (row+1, col)
                graph.add_edge(src, dst, 1)
    graph.add_edge("start", "%d-%d" % (start[0], start[1]), 0)
    graph.add_edge("%d-%d" % (goal[0], goal[1]), "goal", 0)
    return graph

def allowed(elevations, r, c, e):
    "Return True if you are allowed to move to (r,c) from elevation e."
    # Start with the easiest bounds checks.
    if r < 0 or c < 0:
        return False
    # Then the other bounds checks.
    width = len(elevations[0])
    height = len(elevations)
    if c >= width:
        return False
    if r >= height:
        return False
    # Finally, the destination elevation can be at most one higher than the starting
    # elevation.  If that's true, the movement is allowed.
    dest_elev = elevations[r][c]
    if ord(dest_elev) <= ord(e) + 1:
        return True
    # Otherwise the movement is not allowed.
    return False

def read_input():
    "Read the challenge input, which is an elevation map."
    start = None
    goal = None
    elevations = []
    r = 0
    for line in sys.stdin:
        line = line.rstrip()
        row = []
        for c, elev in enumerate(list(line)):
            if elev == 'S':
                start = (r, c)
                elev = 'a'
            elif elev == 'E':
                goal = (r, c)
                elev = 'z'
            #elev = ord(elev) - ord('a')
            row.append(elev)
        elevations.append(row)
        r += 1
    return(start, goal, elevations)

if __name__ == '__main__':
    (start, goal, elevations) = read_input()
    debug("start=%s" % str(start))
    debug("goal=%s" % str(goal))
    debug_elevations(elevations)
    graph = elevations2graph(elevations, start, goal)
    if options.part == 1:
        part1(graph)
    else:
        # We're going to vary the start node, so remove it from the graph.
        graph.remove_start("%d-%d" % (start[0], start[1]))
        part2(graph, elevations)

# Part one solution for test-input1 is: 31
# Part two solution for test-input2 is: 29
# Part one solution for input is: 534
# Part two solution for input is: 525

# Local Variables:
# mode: python
# fill-column: 90
# eval: (flyspell-buffer)
# eval: (column-number-mode)
# End:
