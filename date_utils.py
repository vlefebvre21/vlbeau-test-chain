"""Date utility functions with robust parsing, formatting, and business day calculations.

Uses Python stdlib datetime and typing.
"""

from __future__ import annotations

from datetime import datetime, date, timedelta
from typing import Union


DateLike = Union[date, datetime]


def parse_date(s: str) -> DateLike:
    """Parse a string into a datetime or date object.

    Accepts common date/datetime string formats.
    Raises ValueError if no format matches.

    >>> parse_date('2023-01-01')
    datetime.date(2023, 1, 1)
    >>> parse_date('2023-01-01 12:00:00')
    datetime.datetime(2023, 1, 1, 12, 0)
    """
    from datetime import datetime

    s = s.strip()
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d',
        '%d/%m/%Y',
        '%d-%m-%Y',
        '%Y/%m/%d',
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(s, fmt)
            # Return date object if no time component in the format
            if '%H' not in fmt and '%I' not in fmt and '%p' not in fmt:
                return dt.date()
            return dt
        except ValueError:
            continue
    raise ValueError(f"Unable to parse date string: {repr(s)}")


def format_date(dt: DateLike, fmt: str = '%Y-%m-%d') -> str:
    """Format a date or datetime object with the given strftime format.

    Converts date to datetime internally for formatting consistency.

    >>> format_date(datetime(2023, 1, 1), '%d/%m/%Y')
    '01/01/2023'
    """
    if isinstance(dt, date) and not isinstance(dt, datetime):
        dt = datetime.combine(dt, datetime.min.time())
    return dt.strftime(fmt)


def days_between(d1: DateLike, d2: DateLike) -> int:
    """Return the number of days between two dates or datetimes (d2 - d1).

    Converts datetime to date to avoid time component influence.

    >>> days_between(date(2023, 1, 1), date(2023, 1, 5))
    4
    """
    if isinstance(d1, datetime):
        d1 = d1.date()
    if isinstance(d2, datetime):
        d2 = d2.date()

    return (d2 - d1).days


def is_weekend(dt: DateLike) -> bool:
    """Return True if the date is a Saturday or Sunday.

    >>> is_weekend(date(2023, 1, 7))
    True
    >>> is_weekend(date(2023, 1, 9))
    False
    """
    if isinstance(dt, datetime):
        dt = dt.date()
    return dt.weekday() >= 5


def next_business_day(dt: DateLike) -> date:
    """Return the next business day (Monday-Friday) after the given date.

    >>> next_business_day(date(2023, 1, 6))  # Friday
    datetime.date(2023, 1, 9)
    """
    if isinstance(dt, datetime):
        dt = dt.date()
    dt += timedelta(days=1)
    while dt.weekday() >= 5:
        dt += timedelta(days=1)
    return dt


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import datetime

    # CLI demo
    print("parse_date('2023-01-01'):", parse_date('2023-01-01'))
    print("parse_date('2023-01-01 12:00:00'):", parse_date('2023-01-01 12:00:00'))
    print("format_date(datetime.datetime(2023,1,1), '%d/%m/%Y'):",
          format_date(datetime.datetime(2023,1,1), '%d/%m/%Y'))
    print("days_between(datetime.date(2023,1,1), datetime.date(2023,1,5)):",
          days_between(datetime.date(2023,1,1), datetime.date(2023,1,5)))
    print("is_weekend(datetime.date(2023,1,7)):", is_weekend(datetime.date(2023,1,7)))
    print("next_business_day(datetime.date(2023,1,6)):", next_business_day(datetime.date(2023,1,6)))
