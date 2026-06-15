from datetime import UTC, datetime


def utc_now():
    return datetime.now(tz=UTC)


def utc_datetime(
    year,
    month=None,
    day=None,
    hour=0,
    minute=0,
    second=0,
):
    # Untyped test helper: the None month/day defaults can reach datetime() (a latent bug mypy
    # missed because disallow_untyped_defs=False skipped this body). Hardening it is out of scope
    # for the migration, so the trailing suppression keeps ty green without changing behavior.
    return datetime(year, month, day, hour, minute, second, tzinfo=UTC)  # ty: ignore[invalid-argument-type]
