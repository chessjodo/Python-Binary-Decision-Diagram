#! /bin/env python

from copy import deepcopy
from dataclasses import dataclass
from pprint import PrettyPrinter
from sys import stdin

from typer import run

pp = PrettyPrinter(indent=4)


@dataclass
class Node:
    var: str
    false: "BDD"
    true: "BDD"


@dataclass
class Leaf:
    val: bool


BDD = Node | Leaf


def order_vars(vars):
    """Put variables in desired order. Currently just returns them."""
    return vars


def header_parts(line):
    """Split a truth-table header into its parts."""
    return [v for v in [v.strip() for v in line.split("|")] if v]


def line_parts(line):
    """Split a truth-table line into its parts and make each an int."""
    return [int(v) for v in [v.strip() for v in line.split("|")] if v]


def reduce_lines(var, vars, val, lines_in):
    """Filter, keeping lines where var has val and then drop the var column."""
    lines = deepcopy(lines_in)
    i = vars.index(var)
    lines = [line for line in lines if line[i] == val]
    # print(lines)
    for line in lines:
        del line[i]
    return lines


def bdd_level(vars, lastvar, lines):
    """Recursively build a BDD from truth-table lines using vars in order."""
    var = vars[0]
    if var == lastvar:
        f, t = lines[0][1], lines[1][1]
        if t == f:
            return Leaf(t)
        else:
            return Node(var, Leaf(f), Leaf(t))
    else:
        left = reduce_lines(var, vars, 0, lines)
        right = reduce_lines(var, vars, 1, lines)
        restvars = vars[1:]
        false = bdd_level(restvars, lastvar, left)
        true = bdd_level(restvars, lastvar, right)
        return Node(var, false, true)


def build_bdd():
    """Read a truth table from stdin and print its BDD to stdout."""
    header = stdin.readline()
    vars = order_vars(header_parts(header))
    lines = [line_parts(line) for line in stdin.readlines()]
    lastvar = vars[-1]
    pp.pprint(bdd_level(vars, lastvar, lines))


if __name__ == "__main__" and "__file__" in globals():
    run(build_bdd)
