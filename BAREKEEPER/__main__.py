import json
import sys
from datetime import datetime
import importlib
import importlib.util
import os

import fire

from src.time import TimeEntry
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

        if group_by is not None:
            if isinstance(group_by, tuple):
                group_by = ",".join(group_by)

            apply_grouping = gl.parse(group_by)
        else:
            apply_grouping = None

        g = gl.Grouping(entries, apply_grouping)

        for k, entries in g.groups():
            g[k] = t.execute(entries)

        g.as_csv(sys.stdout)


if __name__ == "__main__":
    fire.Fire(BAREKEEPER)
