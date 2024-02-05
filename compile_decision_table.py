#! /bin/env python

from sys import stdin

from typer import run


def line_parts(line):
    return [v for v in [v.strip() for v in line.split("|")] if v]


def compile_decision_table():
    print("#! /bin/env python\n")
    print("from typer import run\n")
    header = stdin.readline()
    vars = line_parts(header)
    arglist = ", ".join(vars)
    print(f"def decide({arglist}):")
    print(f"    {arglist} = [int(a) for a in [{arglist}]]")
    for n, line in enumerate(stdin.readlines()):
        parts = line_parts(line)
        conjuncts = [f"{v} == {p}" for v, p in zip(vars, parts)]
        conjunction = " and ".join(conjuncts)
        keyword = "if" if n == 0 else "elif"
        print(f"    {keyword} {conjunction}:")
        print(f"        print({parts[len(vars)]})")
    print("    else:")
    print(f"        raise Exception('Arguments unknown: ', {arglist})")
    print(
        """\n\nif __name__ == "__main__":
    run(decide)"""
    )


if __name__ == "__main__":
    run(compile_decision_table)
