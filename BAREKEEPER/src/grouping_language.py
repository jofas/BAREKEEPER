import csv

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
        return ApplyGrouping(titles, ops)

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


class ApplyGrouping:
    def __init__(self, titles, ops):
        self.titles = titles
        self.ops = ops

    def __call__(self, entry):
        return tuple(map(lambda f: f(entry), self.ops))


class Grouping:
    def __init__(self, entries, apply=None):
        self.grouping = {}

        if apply is None:
            apply = ApplyGrouping((), ())

        self.key_titles = apply.titles

        for e in entries:
            key = apply(e)

            if key in self.grouping:
                self.grouping[key].append(e)
            else:
                self.grouping[key] = [e]

    def groups(self):
        return self.grouping.items()

    def __repr__(self):
        return str(self.grouping)

    def __setitem__(self, k, v):
        self.grouping[k] = v

    def as_csv(self, stream):
        records = []

        for k, v in self.groups():
            if isinstance(v, list):
                for v in v:
                    records.append(self.__create_record(k, v.__dict__))
            elif isinstance(v, dict):
                records.append(self.__create_record(k, v))
            else:
                records.append(self.__create_record(k, v.__dict__))

        writer = csv.DictWriter(stream, records[0].keys())

        writer.writeheader()
        writer.writerows(records)

    def __create_record(self, k, v):
        if k != ():
            record = {l: w for l, w in zip(self.key_titles, k)}
        else:
            record = {}

        record.update(v)
        return record
