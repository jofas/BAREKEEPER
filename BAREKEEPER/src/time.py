import functools
from dateutil import parser as dateparser

class TimeEntry:
    def __init__(self, date, description, hours, project):
        self.date = dateparser.isoparse(date)
        self.description = description
        self.hours = hours
        self.project = project

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
            self.entries = functools.reduce(
                lambda acc, e: acc + e.hours, self.entries, 0
            )
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
