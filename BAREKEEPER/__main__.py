import json
import sys
from datetime import datetime

import fire

from src.time import TimeEntry, Aggregator
import src.query_language as ql
from src.util import fmt_date


class BAREKEEPER:
    def __init__(self, filename="-"):
        if filename == "-":
            self.stream = sys.stdin.read()
        else:
            with open(filename) as file:
                self.stream = file.read()

    def time(self, filter=None, aggregations=[]):
        entries = [TimeEntry(**e) for e in json.loads(self.stream)]

        if filter is not None:
            q = ql.parse(filter)
            entries = [e for e in entries if q(e)]

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


if __name__ == "__main__":
    fire.Fire(BAREKEEPER)
