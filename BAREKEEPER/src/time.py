import functools
import json
from datetime import datetime
from dateutil import parser as dateparser

from .util import fmt_date


class TimeEntry:
    def __init__(self, project, hours, date=None, description=None):
        self.hours = hours
        self.project = project

        self.date = dateparser.isoparse(date) if date is not None else None

        self.description = description

    def __repr__(self):
        return str(self.__dict__)


class Aggregator:
    def __init__(self, entries):
        self.entries = entries

    def __repr__(self):
        return str(self.entries)

    def aggregate(self, by):
        if isinstance(self.entries, list):
            self.entries = self.__aggregate_entries(by)
        else:
            for v in self.entries.values():
                v.aggregate(by)

    def sum_hours(self):
        if isinstance(self.entries, list):

            self.entries = [
                TimeEntry(
                    self.entries[0].project,
                    functools.reduce(
                        lambda acc, e: acc + e.hours, self.entries, 0
                    ),
                )
            ]
        else:
            for v in self.entries.values():
                v.sum_hours()

    def __aggregate_entries(self, by):
        d = {}

        for e in self.entries:
            k = by(e)

            if k in d:
                d[k].entries.append(e)
            else:
                d[k] = Aggregator([e])

        return d

    def to_json(self):
        return json.dumps(self, default=self.__serialize_json, indent=2)

    def __serialize_json(self, o):
        if isinstance(o, Aggregator):
            if isinstance(o.entries, list):
                return o.entries
            else:
                return {str(k): v for k, v in o.entries.items()}
        elif isinstance(o, datetime):
            return fmt_date(o)
        else:
            return {k: v for k, v in o.__dict__.items() if v is not None}
