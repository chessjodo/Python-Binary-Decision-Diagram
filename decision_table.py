#! /bin/env python

from random import randint
from string import ascii_lowercase

from typer import run


def decision_table(vars: int = 3, outputs: int = 2):
    """
    Write a decision table over VARS variables with random outputs, either of
    type Boolean, i.e. 0 or 1, or of integers in the range [0,outputs).
    """
    print("|", " | ".join(ascii_lowercase[:vars]), "||   |")
    for b in range(2**vars):
        combos = " | ".join(f"{b:0{vars}b}")
        out = randint(0, 1 if outputs == 1 else outputs - 1)
        print(f"| {combos} || {out} |")


if __name__ == "__main__":
    run(decision_table)
