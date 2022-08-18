from enum import Enum


class Weekday(Enum):
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6
    SUN = 7

    @classmethod
    def from_str(self, s):
        s = s.lower()

        if s == "mon":
            return Weekday.MON
        elif s == "tue":
            return Weekday.TUE
        elif s == "wed":
            return Weekday.WED
        elif s == "thu":
            return Weekday.THU
        elif s == "fri":
            return Weekday.FRI
        elif s == "sat":
            return Weekday.SAT
        elif s == "sun":
            return Weekday.SUN
        else:
            raise Exception("unrecognized weekday name:", s)

    def __str__(self):
        return repr(self).split(".")[1][:3].lower()


def fmt_date(dt):
    return "{:04d}-{:02d}-{:02d}".format(dt.year, dt.month, dt.day)
