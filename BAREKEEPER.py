import sys
import json
import functools
import re

from dateutil import parser as dateparser

import fire

from lark import Lark, Transformer

ql = Lark("""
    query: query_group
         | query (logical_ops query)+
         | project_query

    query_group: "(" query ")"

    project_query: project str_eq_ops ESCAPED_STRING
                 | ESCAPED_STRING str_eq_ops project

    logical_ops: and | or

    and: "AND" | "and" | "&"
    or: "OR" | "or" | "|"

    str_eq_ops: str_exact_equal
              | str_regex_equal
              | str_prefix_equal

    str_exact_equal: "=="
    str_regex_equal: "~="
    str_prefix_equal: ".="

    project: "p"

    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS
""", start="query")

class Op:
    def apply(self, _):
        return False


class LogicalOp(Op):
    pass


class StrExactEq(Op):
    def __init__(self, s):
        self.s = s

    def apply(self, s):
        return s == self.s

    def __repr__(self):
        return "== {}".format(self.s)

class StrRegexEq(Op):
    def __init__(self, s):
        self.re = re.compile(s)

    def apply(self, s):
        return self.re.match(s) is not None

    def __repr__(self):
        return "~= {}".format(self.re)


class StrPrefixEq(Op):
    def __init__(self, s):
        self.s = s

    def apply(self, s):
        return s.startswith(self.s)

    def __repr__(self):
        return ".= {}".format(self.s)


class And(LogicalOp):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def apply(self, entry):
        return self.lhs.apply(entry) and self.rhs.apply(entry)

    def __repr__(self):
        return "{} and {}".format(self.lhs, self.rhs)


class Or(LogicalOp):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def apply(self, entry):
        return self.lhs.apply(entry) or self.rhs.apply(entry)

    def __repr__(self):
        return "{} or {}".format(self.lhs, self.rhs)


class Brackets(Op):
    def __init__(self, inner):
        self.inner = inner

    def apply(self, entry):
        return self.inner.apply(entry)

    def __repr__(self):
        return "({})".format(self.inner)


class ProjectQuery(Op):
    def __init__(self, op):
        self.op = op

    def apply(self, entry):
        return self.op.apply(entry.project)

    def __repr__(self):
        return "p {}".format(self.op)


class QueryTreeGenerator(Transformer):
    def query(self, q):
        if len(q) == 1:
            return q

        [lhs], op, [rhs] = q

        if op == "or":
            return Or(lhs, rhs)
        elif op == "and":
            if isinstance(rhs, Or):
                return Or(And(lhs, rhs.lhs), rhs.rhs)
            return And(lhs, rhs)

    def query_group(self, qg):
        return Brackets(qg[0])

    def project_query(self, pq):
        lhs, op, rhs = pq

        s = rhs if lhs == "project" else lhs

        print(lhs, op, rhs, s)

        if op == "str_exact_equal":
            return ProjectQuery(StrExactEq(s))
        elif op == "str_regex_equal":
            return ProjectQuery(StrRegexEq(s))
        elif op == "str_prefix_equal":
            return ProjectQuery(StrPrefixEq(s))
        else:
            raise Exception("unrecognized operation:", op)

    def logical_ops(self, op):
        return op[0].data.value

    def str_eq_ops(self, op):
        return op[0].data.value

    def project(self, op):
        return "project"

    def ESCAPED_STRING(self, s):
        return s.value[1:-1]


q = ql.parse("p == \"carpolice\" AND (p ~= \"personal\" OR \"car\".=p)")

print(q.pretty())
q = QueryTreeGenerator().transform(q)
print(q)

class TimeEntry:
    def __init__(self, date, description, hours, project):
        self.date = dateparser.isoparse(date)
        self.description = description
        self.hours = hours
        self.project = project

    def __repr__(self):
        return str(self.__dict__)


class Aggregator:
    def __init__(self, entries):
        self.entries = entries

    def __repr__(self):
        return str(self.entries)

    def aggregate(self, by):
        if isinstance(self.entries, list):
            self.entries = self.__aggregate_entries(by)
        else:
            for v in self.entries.values():
                v.aggregate(by)

    def sum_hours(self):
        if isinstance(self.entries, list):
            self.entries = functools.reduce(
                lambda acc, e: acc + e.hours, self.entries, 0
            )
        else:
            for v in self.entries.values():
                v.sum_hours()

    def __aggregate_entries(self, by):
        d = {}

        for e in self.entries:
            k = by(e)

            if k in d:
                d[k].entries.append(e)
            else:
                d[k] = Aggregator([e])

        return d


"""
Allows the generation of reports on time keeping data.
"""
def time(filename="-", aggregations = []):
    if filename == "-":
        stream = sys.stdin.read()
    else:
        with open(filename) as file:
            stream = file.read()

    entries = [TimeEntry(**e) for e in json.loads(stream)]

    a = Aggregator(entries)

    for aggregation in aggregations:
        if aggregation == "project":
            a.aggregate(lambda e: e.project)
        elif aggregation == "month":
            a.aggregate(lambda e: e.date.month)
        elif aggregation == "year":
            a.aggregate(lambda e: e.date.year)
        else:
            raise Exception("unknown aggregation: {}".format(aggregation))

    # sum
    a.sum_hours()

    print(a)

if __name__ == "__main__":
    fire.Fire()
