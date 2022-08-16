import re

from lark import Lark, Transformer

__QL = Lark("""
    query: query_group
         | query (logical_ops query)+
         | project_query

    query_group: "(" query ")"

    project_query: project str_cmp_ops ESCAPED_STRING
                 | ESCAPED_STRING str_cmp_ops project

    data_query: DATE cmp_ops DATE_FMT
              | DATE_FMT cmp_ops DATE

    year_query: YEAR cmp_ops INT
              | INT cmp_ops YEAR

    month_query: MONTH cmp_ops INT
             | INT cmp_ops MONTH
             | MONTH cmp_ops MONTH_NAME
             | MONTH_NAME cmp_ops MONTH

    day_query: DAY cmp_ops INT
             | INT cmp_ops DAY
             | DAY cmp_ops WEEKDAY
             | WEEKDAY cmp_ops DAY

    logical_ops: AND | OR

    AND: "and"i | "&"
    OR: "or"i | "|"

    cmp_ops: eq
           | geq
           | gr
           | leq
           | le

    eq: "=="
    geq: ">="
    gr: ">"
    leq: "<="
    le: "<"

    str_cmp_ops: eq
               | str_regex_equal
               | str_prefix_equal

    str_regex_equal: "~="
    str_prefix_equal: ".="

    DATE_FMT: INT "-" INT "-" INT

    WEEKDAY: "mon"i | "tue"i | "wed"i | "thu"i | "fri"i | "sat"i | "sun"i
    MONTH_NAME: "jan"i | "feb"i | "mar"i | "apr"i | "may"i | "jun"i | "jul"i | "oct"i | "nov"i | "dez"i

    project: "p"

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

        if op == "eq":
            return ProjectQuery(StrExactEq(s))
        elif op == "str_regex_equal":
            return ProjectQuery(StrRegexEq(s))
        elif op == "str_prefix_equal":
            return ProjectQuery(StrPrefixEq(s))
        else:
            raise Exception("unrecognized operation:", op)

    def logical_ops(self, op):
        return op[0].data.value

    def str_cmp_ops(self, op):
        return op[0].data.value

    def project(self, op):
        return "project"

    def ESCAPED_STRING(self, s):
        return s.value[1:-1]


class Op:
    def __call__(self, _):
        return False


class LogicalOp(Op):
    pass


class StrExactEq(Op):
    def __init__(self, s):
        self.s = s

    def __call__(self, s):
        return s == self.s

    def __repr__(self):
        return "== {}".format(self.s)


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


class Brackets(Op):
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, entry):
        return self.inner(entry)

    def __repr__(self):
        return "({})".format(self.inner)


class ProjectQuery(Op):
    def __init__(self, op):
        self.op = op

    def __call__(self, entry):
        return self.op(entry.project)

    def __repr__(self):
        return "p {}".format(self.op)
