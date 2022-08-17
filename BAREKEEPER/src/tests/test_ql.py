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
