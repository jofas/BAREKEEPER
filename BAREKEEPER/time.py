from dateutil import parser


class TimeEntry:
    def __init__(self, project, hours, date, description=None):
        self.hours = hours
        self.project = project
        self.date = parser.isoparse(date).date()
        self.description = description
