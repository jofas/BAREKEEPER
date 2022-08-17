import functools


def execute(entries):
    return functools.reduce(
        lambda acc, e: acc + e.hours, entries, 0
    )
