def fmt_date(datetime, day=True):
    ym = "{:04d}-{:02d}".format(datetime.year, datetime.month)
    return "{}-{:02d}".format(ym, datetime.day) if day else ym
