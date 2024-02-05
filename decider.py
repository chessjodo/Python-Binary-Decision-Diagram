#! /bin/env python

from typer import run


def decide(a, b, c):
    a, b, c = [int(a) for a in [a, b, c]]
    if a == 0 and b == 0 and c == 0:
        print(1)
    elif a == 0 and b == 0 and c == 1:
        print(0)
    elif a == 0 and b == 1 and c == 0:
        print(1)
    elif a == 0 and b == 1 and c == 1:
        print(0)
    elif a == 1 and b == 0 and c == 0:
        print(0)
    elif a == 1 and b == 0 and c == 1:
        print(1)
    elif a == 1 and b == 1 and c == 0:
        print(0)
    elif a == 1 and b == 1 and c == 1:
        print(1)
    else:
        raise Exception("Arguments unknown: ", a, b, c)


if __name__ == "__main__":
    run(decide)
