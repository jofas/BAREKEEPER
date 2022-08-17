import src.query_language as ql
from src.time import TimeEntry


def test_project_eq():
    q = ql.parse('p == "private"')

    e = TimeEntry("private", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("work", 7.5, "2022-08-16")
    assert not q(e)


def test_project_regex_eq():
    q = ql.parse('p ~= "p.*"')

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
    q = ql.parse('d > 2022-8-8')

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
    q = ql.parse('d.y == 2022')

    e = TimeEntry("", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("", 1, "2021-08-16")
    assert not q(e)


def test_year_geq():
    q = ql.parse('d.y >= 2022')

    e = TimeEntry("", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("", 1, "2021-08-16")
    assert not q(e)


def test_year_gr():
    q = ql.parse('d.y > 2022')

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
    q = ql.parse('d.m == 8')

    e = TimeEntry("", 1, "2022-08-16")
    assert q(e)

    e = TimeEntry("", 1, "2022-07-16")
    assert not q(e)


def test_month_geq():
    q = ql.parse('d.m >= 8')

    e = TimeEntry("", 1, "2022-09-16")
    assert q(e)

    e = TimeEntry("", 1, "2022-07-16")
    assert not q(e)


def test_month_gr():
    q = ql.parse('d.m > 8')

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
