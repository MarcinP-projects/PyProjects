import pandas as pd
from pandas.tseries.offsets import BMonthBegin, BMonthEnd, MonthBegin, MonthEnd


def detect_pattern(dates):

    first_day = all(d.day == 1 for d in dates)
    last_day = all(d == d + MonthEnd(0) for d in dates)
    first_business = all(d == d + BMonthBegin(0) for d in dates)
    last_business = all(d == d + BMonthEnd(0) for d in dates)

    if first_business:
        return "first_business_day"
    if last_business:
        return "last_business_day"
    if first_day:
        return "first_day"
    if last_day:
        return "last_day"

    return None


def detect_format(date_str):

    if "-" in date_str:
        return "%Y-%m-%d"

    if "." in date_str:
        return "%d.%m.%Y"

    if "/" in date_str:
        return "%Y/%m/%d"

    return "%Y-%m-%d"


def add_next_date(dates):

    fmt = detect_format(dates[0])

    dt = pd.to_datetime(dates, format=fmt).sort_values()

    pattern = detect_pattern(dt)

    last = dt[-1]

    if pattern == "first_day":
        next_date = last + MonthBegin(1)

    elif pattern == "last_day":
        next_date = last + MonthEnd(1)

    elif pattern == "first_business_day":
        next_date = last + BMonthBegin(1)

    elif pattern == "last_business_day":
        next_date = last + BMonthEnd(1)

    else:
        step = dt.diff().median()
        next_date = last + step

    result = list(dt) + [next_date]
    dates.append(next_date.strftime(fmt))
    return dates
