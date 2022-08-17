import re

from enum import Enum

import dateutil.parser as dateparser

from lark import Lark, Transformer

__QL = Lark("""
    query: query_group
         | query (LOGICAL_OPS query)+
         | project_query
         | date_query
         | year_query
         | month_query
         | day_query
         | weekday_query

    query_group: "(" query ")"

    project_query: PROJECT STR_CMP_OPS ESCAPED_STRING
                 | ESCAPED_STRING STR_CMP_OPS PROJECT

    date_query: DATE CMP_OPS DATE_LIT
              | DATE_LIT CMP_OPS DATE

    year_query: YEAR CMP_OPS INT
              | INT CMP_OPS YEAR

    month_query: MONTH CMP_OPS INT
              | INT CMP_OPS MONTH
              | MONTH CMP_OPS MONTH_NAME
              | MONTH_NAME CMP_OPS MONTH

    day_query: DAY CMP_OPS INT
             | INT CMP_OPS DAY

    weekday_query: DAY CMP_OPS WEEKDAY
                 | WEEKDAY CMP_OPS DAY

    LOGICAL_OPS: AND | OR

    CMP_OPS: EQ
           | GEQ
           | GR
           | LEQ
           | LE

    STR_CMP_OPS: EQ
               | STR_REGEX_EQUAL
               | STR_PREFIX_EQUAL

    AND: "and"i | "&"
    OR: "or"i | "|"

    EQ: "=="
    GEQ: ">="
    GR: ">"
    LEQ: "<="
    LE: "<"

    STR_REGEX_EQUAL: "~="
    STR_PREFIX_EQUAL: ".="

    DATE_LIT: INT "-" INT "-" INT

    WEEKDAY: "mon"i | "tue"i | "wed"i | "thu"i | "fri"i | "sat"i | "sun"i
    MONTH_NAME: "jan"i | "feb"i | "mar"i | "apr"i | "may"i | "jun"i | "jul"i | "aug"i | "oct"i | "nov"i | "dez"i

    PROJECT: "p"

    DATE: "d"
    YEAR: "d.y"
    MONTH: "d.m"
    DAY: "d.d"

    %import common.INT
    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS
""", start="query")


def parse(s):
    return __QueryTreeGenerator().transform(__QL.parse(s))


class __QueryTreeGenerator(Transformer):
    def query(self, q):
        if len(q) == 1:
            return q[0]

        lhs, op, rhs = q

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

        if op == "==":
            return ProjectQuery(Eq(s))
        elif op == "~=":
            return ProjectQuery(StrRegexEq(s))
        elif op == ".=":
            return ProjectQuery(StrPrefixEq(s))
        else:
            raise Exception("unrecognized operation:", op)

    def date_query(self, dq):
        lhs, op, rhs = dq

        d = rhs if lhs == "date" else lhs
        d = dateparser.isoparse(d)

        if op == "==":
            return DateQuery(Eq(d))
        elif op == ">=":
            return DateQuery(Geq(d))
        elif op == ">":
            return DateQuery(Gr(d))
        elif op == "<=":
            return DateQuery(Leq(d))
        elif op == "<":
            return DateQuery(Le(d))
        else:
            raise Exception("unrecognized operation:", op)

    def year_query(self, yq):
        lhs, op, rhs = yq

        y = rhs if lhs == "year" else lhs

        if op == "==":
            return YearQuery(Eq(int(y)))
        elif op == ">=":
            return YearQuery(Geq(int(y)))
        elif op == ">":
            return YearQuery(Gr(int(y)))
        elif op == "<=":
            return YearQuery(Leq(int(y)))
        elif op == "<":
            return YearQuery(Le(int(y)))
        else:
            raise Exception("unrecognized operation:", op)

    def month_query(self, mq):
        lhs, op, rhs = mq

        m = rhs if lhs == "month" else lhs
        m = int(m)

        if op == "==":
            return MonthQuery(Eq(m))
        elif op == ">=":
            return MonthQuery(Geq(m))
        elif op == ">":
            return MonthQuery(Gr(m))
        elif op == "<=":
            return MonthQuery(Leq(m))
        elif op == "<":
            return MonthQuery(Le(m))
        else:
            raise Exception("unrecognized operation:", op)

    def day_query(self, dq):
        lhs, op, rhs = dq

        d = rhs if lhs == "day" else lhs
        d = int(d)

        if op == "==":
            return DayQuery(Eq(d))
        elif op == ">=":
            return DayQuery(Geq(d))
        elif op == ">":
            return DayQuery(Gr(d))
        elif op == "<=":
            return DayQuery(Leq(d))
        elif op == "<":
            return DayQuery(Le(d))
        else:
            raise Exception("unrecognized operation:", op)

    def weekday_query(self, wdq):
        lhs, op, rhs = wdq

        d = rhs if lhs == "day" else lhs

        if op == "==":
            return WeekdayQuery(Eq(d.value))
        elif op == ">=":
            return WeekdayQuery(Geq(d.value))
        elif op == ">":
            return WeekdayQuery(Gr(d.value))
        elif op == "<=":
            return WeekdayQuery(Leq(d.value))
        elif op == "<":
            return WeekdayQuery(Le(d.value))
        else:
            raise Exception("unrecognized operation:", op)

    def LOGICAL_OPS(self, op):
        return op.value.lower()

    def CMP_OPS(self, op):
        return op.value

    def STR_CMP_OPS(self, op):
        return op.value

    def PROJECT(self, _):
        return "project"

    def DATE(self, _):
        return "date"

    def YEAR(self, _):
        return "year"

    def MONTH(self, _):
        return "month"

    def DAY(self, _):
        return "day"

    def DATE_LIT(self, d):
        [y, m, d] = d.value.split("-")
        return "{:04d}-{:02d}-{:02d}".format(int(y), int(m), int(d))

    def ESCAPED_STRING(self, s):
        return s.value[1:-1]

    def MONTH_NAME(self, mn):
        mn = mn.value.lower()

        if mn == "jan":
            return 1
        elif mn == "feb":
            return 2
        elif mn == "mar":
            return 3
        elif mn == "apr":
            return 4
        elif mn == "may":
            return 5
        elif mn == "jun":
            return 6
        elif mn == "jul":
            return 7
        elif mn == "aug":
            return 8
        elif mn == "sep":
            return 9
        elif mn == "oct":
            return 10
        elif mn == "nov":
            return 11
        elif mn == "dez":
            return 12
        else:
            raise Exception("unrecognized month name:", mn)

    def WEEKDAY(self, wd):
        return Weekday.from_str(wd.value)


class Weekday(Enum):
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6
    SUN = 7

    @classmethod
    def from_str(self, s):
        s = s.lower()

        if s == "mon":
            return Weekday.MON
        elif s == "tue":
            return Weekday.TUE
        elif s == "wed":
            return Weekday.WED
        elif s == "thu":
            return Weekday.THU
        elif s == "fri":
            return Weekday.FRI
        elif s == "sat":
            return Weekday.SAT
        elif s == "sun":
            return Weekday.SUN
        else:
            raise Exception("unrecognized weekday name:", s)


class Op:
    def __call__(self, _):
        return False


class LogicalOp(Op):
    pass


class Brackets(Op):
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, entry):
        return self.inner(entry)

    def __repr__(self):
        return "({})".format(self.inner)


class And(LogicalOp):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __call__(self, entry):
        return self.lhs(entry) and self.rhs(entry)

    def __repr__(self):
        return "{} and {}".format(self.lhs, self.rhs)


class Or(LogicalOp):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __call__(self, entry):
        return self.lhs(entry) or self.rhs(entry)

    def __repr__(self):
        return "{} or {}".format(self.lhs, self.rhs)


class Eq(Op):
    def __init__(self, s):
        self.s = s

    def __call__(self, s):
        return s == self.s

    def __repr__(self):
        return "== {}".format(self.s)


class Geq(Op):
    def __init__(self, s):
        self.s = s

    def __call__(self, s):
        return s >= self.s

    def __repr__(self):
        return ">= {}".format(self.s)


class Gr(Op):
    def __init__(self, s):
        self.s = s

    def __call__(self, s):
        return s > self.s

    def __repr__(self):
        return "> {}".format(self.s)


class Leq(Op):
    def __init__(self, s):
        self.s = s

    def __call__(self, s):
        return s <= self.s

    def __repr__(self):
        return "<= {}".format(self.s)


class Le(Op):
    def __init__(self, s):
        self.s = s

    def __call__(self, s):
        return s < self.s

    def __repr__(self):
        return "< {}".format(self.s)


class StrRegexEq(Op):
    def __init__(self, s):
        self.re = re.compile(s)

    def __call__(self, s):
        return self.re.match(s) is not None

    def __repr__(self):
        return "~= {}".format(self.re)


class StrPrefixEq(Op):
    def __init__(self, s):
        self.s = s

    def __call__(self, s):
        return s.startswith(self.s)

    def __repr__(self):
        return ".= {}".format(self.s)


class ProjectQuery(Op):
    def __init__(self, op):
        self.op = op

    def __call__(self, entry):
        return self.op(entry.project)

    def __repr__(self):
        return "p {}".format(self.op)


class DateQuery(Op):
    def __init__(self, op):
        self.op = op

    def __call__(self, entry):
        return self.op(entry.date)

    def __repr__(self):
        return "d {}".format(self.op)


class YearQuery(Op):
    def __init__(self, op):
        self.op = op

    def __call__(self, entry):
        return self.op(entry.date.year)

    def __repr__(self):
        return "d.y {}".format(self.op)


class MonthQuery(Op):
    def __init__(self, op):
        self.op = op

    def __call__(self, entry):
        return self.op(entry.date.month)

    def __repr__(self):
        return "d.m {}".format(self.op)


class DayQuery(Op):
    def __init__(self, op):
        self.op = op

    def __call__(self, entry):
        return self.op(entry.date.day)

    def __repr__(self):
        return "d.d {}".format(self.op)


class WeekdayQuery(Op):
    def __init__(self, op):
        self.op = op

    def __call__(self, entry):
        return self.op(entry.date.isoweekday())

    def __repr__(self):
        return "d.d {}".format(self.op)
