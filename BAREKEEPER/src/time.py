import functools
import json
from datetime import datetime
from dateutil import parser as dateparser

from .util import fmt_date


class TimeEntry:
    def __init__(self, project, hours, date, description=None):
        self.hours = hours
        self.project = project
        self.date = dateparser.isoparse(date).date()
        self.description = description
