from lark import Lark, Transformer

from .util import fmt_date

__GL = Lark("""
    grouping: overridden_title ("," overridden_title)* [","]

    overridden_title: var ["=" ESCAPED_STRING]

    var: project | DATE | YEAR | MONTH | DAY

    project: "p"i ["[" DEPTH "]"]

    DEPTH: INT | "*"

    DATE: "d"i
    YEAR: "d.y"i
    MONTH: "d.m"i
    DAY: "d.d"i

    %import common.INT
    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS
""", start="grouping")


def parse(s):
    return __GroupingGenerator().transform(__GL.parse(s))


class __GroupingGenerator(Transformer):
    def grouping(self, g):
        titles, ops = zip(*g)
        return Grouping(titles, ops)

    def overridden_title(self, ot):
        var, title = ot

        if title is not None:
            return (title, var[1])
        else:
            return var

    def var(self, v):
        return v[0]

    def project(self, p):
        [depth] = p

        if depth is None:
            return "project", lambda e: e.project
        else:
            return (
                "project",
                lambda e: ".".join(e.project.split(".")[:depth])
            )

    def DATE(self, d):
        return "date", lambda e: fmt_date(e.date)

    def YEAR(self, y):
        return "year", lambda e: e.date.year

    def MONTH(self, m):
        return "month", lambda e: e.date.month

    def DAY(self, d):
        return "day", lambda e: e.date.day

    def DEPTH(self, d):
        return None if d == "*" else int(d)

    def ESCAPED_STRING(self, s):
        return s[1:-1]


class Grouping:
    def __init__(self, titles, ops):
        self.titles = titles
        self.ops = ops

    def __call__(self, entry):
        return tuple(map(lambda f: f(entry), self.ops))
