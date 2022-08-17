import json
import sys
from datetime import datetime
import importlib
import importlib.util
import os

import fire

from src.time import TimeEntry, Aggregator
import src.query_language as ql
import src.grouping_language as gl
from src.util import fmt_date


class BAREKEEPER:
    def __init__(self, filename="-"):
        if filename == "-":
            self.stream = sys.stdin.read()
        else:
            with open(filename) as file:
                self.stream = file.read()

    def time(self, filter=None, group_by=None, transformer="tf.no_tf"):
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

        # TODO: handle case where no grouping is applied as graceful as
        #       possible
        if group_by is not None:
            apply_grouping = gl.parse(group_by)

            g = gl.Grouping(entries, apply_grouping)

            for k, entries in g.groups():
                g[k] = t.execute(entries)

            # TODO: csv output
            #
            # TODO: I got titles for the key, now what?
            #
            print(g)
        else:
            entries = t.execute(entries)

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
