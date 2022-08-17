import json
import sys
from datetime import datetime
import importlib
import importlib.util
import os

import fire

from src.time import TimeEntry, Aggregator
import src.query_language as ql
from src.util import fmt_date


# [group1, group2, group3]
#
# grouping(entry) -> (group1, group2, group3)
#

#
# dictionary for each group
# for each group, intersect with other groups
#
# 1. create dict for each group
# 2. recursively intersect dictionaries and save a list of groups
#
# ... how to create a dict from groups? TUPLES!
# recursively
#
# ... pandas???
#


class Grouping:
    def __init__(self, apply, entries):
        self.grouping = {}

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


class BAREKEEPER:
    def __init__(self, filename="-"):
        if filename == "-":
            self.stream = sys.stdin.read()
        else:
            with open(filename) as file:
                self.stream = file.read()

    def time(self, filter=None, group_by=[], transformer="tf.no_tf"):
        entries = [TimeEntry(**e) for e in json.loads(self.stream)]

        if filter is not None:
            q = ql.parse(filter)
            entries = [e for e in entries if q(e)]

        if os.path.isfile(transformer):
            spec = importlib.util.spec_from_file_location(
                "tf.custom", transformer,
            )
            t = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(t)
        else:
            t = importlib.import_module(transformer)

        # TODO: implement grouping function
        g = Grouping(lambda _: (1,), entries)

        for k, entries in g.groups():
            g[k] = t.execute(entries)

        # TODO: either json or csv output
        print(g)

        """
        a = Aggregator(entries)

        for aggregation in dict.fromkeys(aggregations):
            if aggregation == "p":
                a.aggregate(lambda e: e.project)
            elif aggregation == "m":
                a.aggregate(lambda e: e.date.month)
            elif aggregation == "y":
                a.aggregate(lambda e: e.date.year)
            elif aggregation == "d":
                a.aggregate(lambda e: e.date.day)
            elif aggregation == "ym":
                a.aggregate(lambda e: fmt_date(e.date, day=False))
            elif aggregation == "ymd":
                a.aggregate(lambda e: fmt_date(e.date))
            else:
                raise Exception("unknown aggregation: {}".format(aggregation))

        a.sum_hours()

        print(a.to_json())
        """


if __name__ == "__main__":
    fire.Fire(BAREKEEPER)
