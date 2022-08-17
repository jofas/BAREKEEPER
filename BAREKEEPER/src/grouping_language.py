from lark import Lark, Transformer

from .util import fmt_date

__GL = Lark("""
    grouping: var ("," var)* [","]

    var: project | DATE | YEAR | MONTH | DAY

    project: "p"i ["[" DEPTH "]"]

    DEPTH: INT | "*"

    DATE: "d"i
    YEAR: "d.y"i
    MONTH: "d.m"i
    DAY: "d.d"i

    %import common.INT
    %import common.WS
    %ignore WS
""", start="grouping")


def parse(s):
    return __GroupingGenerator().transform(__GL.parse(s))


class __GroupingGenerator(Transformer):
    def grouping(self, g):
        return Grouping(g)

    def var(self, v):
        return v[0]

    def project(self, p):
        [depth] = p

        if depth is None:
            return lambda e: e.project
        else:
            return lambda e: ".".join(e.project.split(".")[:depth])

    def DATE(self, d):
        return lambda e: fmt_date(e.date)

    def YEAR(self, y):
        return lambda e: e.date.year

    def MONTH(self, m):
        return lambda e: e.date.month

    def DAY(self, d):
        return lambda e: e.date.day

    def DEPTH(self, d):
        return None if d == "*" else int(d)


class Grouping:
    def __init__(self, ops):
        self.ops = ops

    def __call__(self, entry):
        return tuple(map(lambda f: f(entry), self.ops))
