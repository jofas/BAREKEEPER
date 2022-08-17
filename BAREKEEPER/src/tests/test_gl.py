import src.grouping_language as gl
from src.time import TimeEntry


def test_1():
    g = gl.parse("p,d,d.y,D.M,d.D")

    e = TimeEntry("private", 1, "2022-08-16")

    assert g(e) == ("private", "2022-08-16", 2022, 8, 16)


def test_depth_1():
    g = gl.parse("p[1],")

    e = TimeEntry("private.confidential", 1, "2022-08-16")

    assert g(e) == ("private",)


def test_depth_2():
    g = gl.parse("P[*]")

    e = TimeEntry("private.confidential", 1, "2022-08-16")

    assert g(e) == ("private.confidential",)


def test_depth_3():
    g = gl.parse("P[5555]")

    e = TimeEntry("private.confidential", 1, "2022-08-16")

    assert g(e) == ("private.confidential",)


def test_depth_4():
    g = gl.parse("P[0]")

    e = TimeEntry("private.confidential", 1, "2022-08-16")

    assert g(e) == ("",)
