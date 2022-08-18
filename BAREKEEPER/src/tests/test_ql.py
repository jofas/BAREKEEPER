import src.query_language as ql
from src.time import TimeEntry


def test_lops_and():
    q = ql.parse('p == "private" AND d == 2022-08-16')

    e = TimeEntry("private", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("work", 1, "2022-08-16")
    assert not q(e)

    e = TimeEntry("private", 1, "2022-08-17")
    assert not q(e)

    e = TimeEntry("work", 1, "2022-08-17")
    assert not q(e)


def test_lops_or():
    q = ql.parse('p == "private" OR d == 2022-08-16')

    e = TimeEntry("private", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("work", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("private", 1, "2022-08-17")
    assert q(e)

    e = TimeEntry("work", 1, "2022-08-17")
    assert not q(e)


def test_no_brackets():
    q = ql.parse('p == "private" AND d == 2022-08-16 OR d == 2022-08-17')

    e = TimeEntry("private", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("work", 1, "2022-08-16")
    assert not q(e)

    e = TimeEntry("private", 1, "2022-08-17")
    assert q(e)

    e = TimeEntry("work", 1, "2022-08-17")
    assert q(e)


def test_brackets():
    q = ql.parse('(p == "private" AND d == 2022-08-16) OR d == 2022-08-17')

    e = TimeEntry("private", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("work", 1, "2022-08-16")
    assert not q(e)

    e = TimeEntry("private", 1, "2022-08-15")
    assert not q(e)

    e = TimeEntry("work", 1, "2022-08-17")
    assert q(e)


def test_project_eq():
    q = ql.parse('p == "private"')

    e = TimeEntry("private", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("work", 7.5, "2022-08-16")
    assert not q(e)


def test_project_regex_eq():
    q = ql.parse('P ~= "p.*"')

    e = TimeEntry("private", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("work", 7.5, "2022-08-16")
    assert not q(e)


def test_project_prefix_eq():
    q = ql.parse('p .= "p"')

    e = TimeEntry("private", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("work", 7.5, "2022-08-16")
    assert not q(e)


def test_date_eq():
    q = ql.parse('d == 2022-8-8')

    e = TimeEntry("", 1, "2022-08-08")
    assert q(e)

    e = TimeEntry("", 1, "2021-08-16")
    assert not q(e)


def test_date_geq():
    q = ql.parse('d >= 2022-8-8')

    e = TimeEntry("", 1, "2022-08-11")
    assert q(e)

    e = TimeEntry("", 1, "2021-08-16")
    assert not q(e)


def test_date_gr():
    q = ql.parse('D > 2022-8-8')

    e = TimeEntry("", 1, "2022-08-09")
    assert q(e)

    e = TimeEntry("", 1, "2022-08-08")
    assert not q(e)


def test_date_leq():
    q = ql.parse('d <= 2022-8-8')

    e = TimeEntry("", 1, "2022-08-07")
    assert q(e)

    e = TimeEntry("", 1, "2022-08-09")
    assert not q(e)


def test_date_le():
    q = ql.parse('d < 2022-8-8')

    e = TimeEntry("", 1, "2022-08-07")
    assert q(e)

    e = TimeEntry("", 1, "2022-08-08")
    assert not q(e)


def test_year_eq():
    q = ql.parse('D.y == 2022')

    e = TimeEntry("", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("", 1, "2021-08-16")
    assert not q(e)


def test_year_geq():
    q = ql.parse('d.Y >= 2022')

    e = TimeEntry("", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("", 1, "2021-08-16")
    assert not q(e)


def test_year_gr():
    q = ql.parse('D.Y > 2022')

    e = TimeEntry("", 1, "2023-08-16")
    assert q(e)

    e = TimeEntry("", 1, "2022-08-16")
    assert not q(e)


def test_year_leq():
    q = ql.parse('d.y <= 2022')

    e = TimeEntry("", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("", 1, "2023-08-16")
    assert not q(e)


def test_year_le():
    q = ql.parse('d.y < 2022')

    e = TimeEntry("", 1, "2021-08-16")
    assert q(e)

    e = TimeEntry("", 1, "2022-08-16")
    assert not q(e)


def test_month_eq():
    q = ql.parse('D.m == 8')

    e = TimeEntry("", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("", 1, "2022-07-16")
    assert not q(e)


def test_month_geq():
    q = ql.parse('d.M >= 8')

    e = TimeEntry("", 1, "2022-09-16")
    assert q(e)

    e = TimeEntry("", 1, "2022-07-16")
    assert not q(e)


def test_month_gr():
    q = ql.parse('D.M > 8')

    e = TimeEntry("", 1, "2023-09-16")
    assert q(e)

    e = TimeEntry("", 1, "2022-08-16")
    assert not q(e)


def test_month_leq():
    q = ql.parse('d.m <= 8')

    e = TimeEntry("", 1, "2023-08-16")
    assert q(e)

    e = TimeEntry("", 1, "2022-09-16")
    assert not q(e)


def test_month_le():
    q = ql.parse('d.m < 8')

    e = TimeEntry("", 1, "2021-07-16")
    assert q(e)

    e = TimeEntry("", 1, "2022-08-16")
    assert not q(e)


def test_month_geq_abbr():
    q = ql.parse('d.m >= aug')

    e = TimeEntry("", 1, "2022-09-16")
    assert q(e)

    e = TimeEntry("", 1, "2022-07-16")
    assert not q(e)


def test_month_gr_abbr():
    q = ql.parse('d.m > Aug')

    e = TimeEntry("", 1, "2023-09-16")
    assert q(e)

    e = TimeEntry("", 1, "2022-08-16")
    assert not q(e)


def test_month_leq_abbr():
    q = ql.parse('d.m <= aUG')

    e = TimeEntry("", 1, "2023-08-16")
    assert q(e)

    e = TimeEntry("", 1, "2022-09-16")
    assert not q(e)


def test_month_le_abbr():
    q = ql.parse('d.m < AUG')

    e = TimeEntry("", 1, "2021-07-16")
    assert q(e)

    e = TimeEntry("", 1, "2022-08-16")
    assert not q(e)


def test_day_eq():
    q = ql.parse('D.d == 16')

    e = TimeEntry("", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("", 1, "2022-08-17")
    assert not q(e)


def test_day_geq():
    q = ql.parse('d.D >= 16')

    e = TimeEntry("", 1, "2022-09-16")
    assert q(e)

    e = TimeEntry("", 1, "2022-07-15")
    assert not q(e)


def test_day_gr():
    q = ql.parse('D.D > 16')

    e = TimeEntry("", 1, "2023-09-17")
    assert q(e)

    e = TimeEntry("", 1, "2022-08-16")
    assert not q(e)


def test_day_leq():
    q = ql.parse('d.d <= 16')

    e = TimeEntry("", 1, "2023-08-16")
    assert q(e)

    e = TimeEntry("", 1, "2022-09-17")
    assert not q(e)


def test_day_le():
    q = ql.parse('d.d < 16')

    e = TimeEntry("", 1, "2021-07-15")
    assert q(e)

    e = TimeEntry("", 1, "2022-08-16")
    assert not q(e)


"""
Tests the equality operator (==) for the weekday of a date.
"""


def test_weekday_eq():
    q = ql.parse('d.d == tue')

    e = TimeEntry("", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("", 1, "2022-08-17")
    assert not q(e)


"""
Tests the greater-equal operator (>=) for the weekday of a date.
"""


def test_weekday_geq():
    q = ql.parse('d.d >= tue')

    e = TimeEntry("", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("", 1, "2022-08-15")
    assert not q(e)


"""
Tests the greater-than operator (>) for the weekday of a date.
"""


def test_weekday_gr():
    q = ql.parse('d.d > Tue')

    e = TimeEntry("", 1, "2022-08-17")
    assert q(e)

    e = TimeEntry("", 1, "2022-08-16")
    assert not q(e)


"""
Tests the less-equal operator (<=) for the weekday of a date.
"""


def test_weekday_leq():
    q = ql.parse('d.d <= TuE')

    e = TimeEntry("", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("", 1, "2022-08-17")
    assert not q(e)


"""
Tests the less-than operator (<) for the weekday of a date.
"""


def test_weekday_le():
    q = ql.parse('d.d < TUE')

    e = TimeEntry("", 1, "2022-08-15")
    assert q(e)

    e = TimeEntry("", 1, "2022-08-16")
    assert not q(e)
