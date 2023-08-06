from datetime import datetime, timezone


def utc_now():
    return datetime.now(tz=timezone.utc)


def utc_datetime(
    year: int,
    month: None | int = None,
    day: None | int = None,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
):
    return datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)
