from datetime import datetime, date, timedelta

def parse_date(s):
    """
    Parse a string into datetime.date or datetime.datetime based on format.
    Supports common formats like YYYY-MM-DD, YYYY-MM-DD HH:MM:SS, DD/MM/YYYY.
    """
    if isinstance(s, (date, datetime)):
        return s
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
            parsed = datetime.strptime(s, fmt)
            # If format has no time components, return date
            if '%H' not in fmt and '%I' not in fmt and '%p' not in fmt:
                return parsed.date()
            return parsed
        except ValueError:
            pass
    raise ValueError(f"Unable to parse date string: {repr(s)}")

def format_date(dt, fmt='%Y-%m-%d'):
    """
    Format date or datetime object using strftime format string.
    """
    if isinstance(dt, date) and not isinstance(dt, datetime):
        dt = datetime.combine(dt, datetime.min.time())
    return dt.strftime(fmt)

def days_between(d1, d2):
    """
    Return the number of days between d1 and d2 (d2 - d1).
    Handles both date and datetime inputs by converting to date.
    """
    if isinstance(d1, datetime):
        d1 = d1.date()
    if isinstance(d2, datetime):
        d2 = d2.date()
    return (d2 - d1).days

def is_weekend(dt):
    """
    Return True if dt is a Saturday or Sunday.
    """
    if isinstance(dt, datetime):
        dt = dt.date()
    return dt.weekday() >= 5  # 0=Mon, 5=Sat, 6=Sun

def next_business_day(dt):
    """
    Return the next business day (Monday-Friday) after dt.
    """
    if isinstance(dt, datetime):
        dt = dt.date()
    dt += timedelta(days=1)
    while dt.weekday() >= 5:
        dt += timedelta(days=1)
    return dt

if __name__ == "__main__":
    # Test examples
    print("parse_date('2023-01-01'):", parse_date('2023-01-01'))
    print("parse_date('2023-01-01 12:00:00'):", parse_date('2023-01-01 12:00:00'))
    print("format_date(datetime(2023,1,1), '%d/%m/%Y'):", format_date(datetime(2023,1,1), '%d/%m/%Y'))
    print("days_between(date(2023,1,1), date(2023,1,5)):", days_between(date(2023,1,1), date(2023,1,5)))
    print("is_weekend(date(2023,1,7)):", is_weekend(date(2023,1,7)))  # Saturday
    print("next_business_day(date(2023,1,6)):", next_business_day(date(2023,1,6)))  # Friday -> Monday 2023-01-09
