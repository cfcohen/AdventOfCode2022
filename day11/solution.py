#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Advent of Code Day 11."""

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
def part1(monkeys):
    "Solve part 1: Twenty rounds and then calculate the monkey business value."
    for round_num in range(20):
        do_round(monkeys)
        debug("After round %d, the monkeys are holding items with these worry levels:" % (round_num + 1))
        for monkey in monkeys.values():
            debug("Monkey %d inspected items %d times." % (monkey.num, monkey.activity))

    debug("The most active monkeys are:")
    active_monkeys = sorted(monkeys.values(), key=lambda monkey: monkey.activity, reverse=True)
    for monkey in active_monkeys:
        debug("Monkey %d inspected items %d times." % (monkey.num, monkey.activity))

    monkey_business = active_monkeys[0].activity * active_monkeys[1].activity
    print(monkey_business)

# ----------------------------------------------------------------------------------------
# Part Two
# ----------------------------------------------------------------------------------------
def part2(monkeys):
    """
    Solve part 2: 10000 rounds without division by 3 and calculate the monkey business.

    Then return the monkey business value.  The trick here is to observe that you can
    always reduce the giant worry value modulo the product of all of the monkey's
    divisible values.
    """
    product = 1
    for monkey in monkeys.values():
        monkey.reduction = False
        product *= monkey.divisible

    for monkey in monkeys.values():
        monkey.product = product

    for round_num in range(10000):
        do_round(monkeys, detail=False)
        if round_num + 1 in [1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]:
            debug("== After round %d ==" % (round_num + 1))
            for monkey in monkeys.values():
                debug("Monkey %d inspected items %d times." % (monkey.num, monkey.activity))

    debug("The most active monkeys are:")
    active_monkeys = sorted(monkeys.values(), key=lambda monkey: monkey.activity, reverse=True)
    for monkey in active_monkeys:
        debug("Monkey %d inspected items %d times." % (monkey.num, monkey.activity))

    monkey_business = active_monkeys[0].activity * active_monkeys[1].activity
    print(monkey_business)

# ----------------------------------------------------------------------------------------
# Shared
# ----------------------------------------------------------------------------------------
class Monkey(object):

    def __init__(self, num):
        self.num = num
        self.divisible = None
        self.operator = None
        self.arg = None
        self.true_target = None
        self.false_target = None
        self.items = []
        self.activity = 0
        self.reduction = True

    @property
    def opr_str(self):
        if self.operator == '*':
            return 'is multiplied'
        elif self.operator == '+':
            return 'increases'

    @property
    def arg_str(self):
        if self.arg == 'old':
            return 'itself'
        else:
            return str(self.arg)

    def operation(self, value):
        "Do the addition, multiplication, square operation on monkey inspection."
        if self.operator == '*':
            if self.arg == 'old':
                return value * value
            else:
                return value * int(self.arg)
        elif self.operator == '+':
            if self.arg == 'old':
                return value + value
            else:
                return value + int(self.arg)
        assert(False)

    def inspect(self, monkeys, detail=True):
        if detail:
            debug("Monkey %d:" % self.num)
        for item in self.items:
            # This monkey has inspected an item.  Increase it's activity by one.
            self.activity += 1
            # Emir the output from the challenge.
            if detail:
                debug("  Monkey inspects and item with a worry level of %d." % item)
            worry = self.operation(item)
            if detail:
                debug("    Worry level %s by %s to %s" % (self.opr_str, self.arg, worry))
                debug("    Monkey gets bored with item. ", end = '')
            # In part 2, we're no longer reducing the worry leve with each inspection.
            if self.reduction:
                worry = int(worry/3)
                if detail:
                    debug("    Worry level is divided by 3 to %d." % worry)
            if worry % self.divisible == 0:
                target = self.true_target
                tstr = ''
            else:
                target = self.false_target
                tstr = 'not '
            if detail:
                debug("    Current worry level is %sdivisible by %d." % (tstr, self.divisible))
                debug("    Item with worry level %d is thrown to monkey %d." % (worry, target))

            # And as a consequence, in order to keep the numbers from becoming
            # ridiculously large (in other words, TOO LARGE), we need to reduce it.
            if not self.reduction:
                worry = worry % self.product

            monkeys[target].items.append(worry)
        self.items = []

    def __str__(self):
        "Return the monkey as a string for debugging."
        return "Monkey(%d), new=old%s%s x%%%d?%s:%s activity=%d items=%s" % (
            self.num, self.operator, self.arg, self.divisible,
            self.true_target, self.false_target, self.activity, self.items)

# ----------------------------------------------------------------------------------------
def do_round(monkeys, detail=True):
    "Evaluate a round of monkeys throwing objects."
    for monkey in monkeys.values():
        monkey.inspect(monkeys, detail)

# ----------------------------------------------------------------------------------------
def read_input():
    "Read the challenge input and initialize the monkeys."
    monkeys = {}
    monkey = None
    for line in sys.stdin:
        line = line.rstrip()
        if line.startswith("Monkey "):
            monkey = Monkey(int(line[7]))
        elif line.startswith("  Starting items: "):
            monkey.items = [int(x) for x in line[18:].split(', ')]
        elif line.startswith("  Operation: new = old "):
            monkey.operator = line[23]
            monkey.arg = line[25:]
        elif line.startswith("  Test: divisible by "):
            monkey.divisible = int(line[21:])
        elif line.startswith("    If true: throw to monkey "):
            monkey.true_target = int(line[29])
        elif line.startswith("    If false: throw to monkey "):
            monkey.false_target = int(line[30])
        elif line == "":
            debug(str(monkey))
            monkeys[monkey.num] = monkey
            monkey = None
        else:
            print("Unexpected line: '%s'" % line, file=sys.stderr)
    debug(str(monkey))
    monkeys[monkey.num] = monkey
    return monkeys

if __name__ == '__main__':
    monkeys = read_input()
    if options.part == 1:
        part1(monkeys)
    else:
        part2(monkeys)

# Part one solution for test-input1 is: 10605
# Part two solution for test-input1 is: 2713310158
# Part one solution for input is: 55458
# Part two solution for input is: 14508081294

# Local Variables:
# mode: python
# fill-column: 90
# eval: (flyspell-buffer)
# eval: (column-number-mode)
# End:
