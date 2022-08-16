import json
import sys

import fire

from src.time import TimeEntry, Aggregator
import src.query_language as ql


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

        for aggregation in aggregations:
            if aggregation == "project":
                a.aggregate(lambda e: e.project)
            elif aggregation == "month":
                a.aggregate(lambda e: e.date.month)
            elif aggregation == "year":
                a.aggregate(lambda e: e.date.year)
            else:
                raise Exception("unknown aggregation: {}".format(aggregation))

        # sum
        a.sum_hours()

        print(a.to_json())


if __name__ == "__main__":
    fire.Fire(BAREKEEPER)
