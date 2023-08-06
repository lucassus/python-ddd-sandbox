from datetime import datetime, timezone


def utc_now():
    return datetime.now(tz=timezone.utc)


def utc_datetime(
    year,
    month=None,
    day=None,
    hour=0,
    minute=0,
    second=0,
):
    return datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)
