import functools


def execute(entries):
    return {
        "hours": functools.reduce(
            lambda acc, e: acc + e.hours, entries, 0
        ),
    }
