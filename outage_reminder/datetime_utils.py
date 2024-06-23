import datetime


def utcnow() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def isoformat_datetime(d: datetime.datetime) -> str:
    format = "%Y-%m-%dT%H:%M:%S.%f"
    s = f"{d.strftime(format)[:-3]}"

    if d.tzinfo == datetime.timezone.utc:
        return f"{s}Z"

    return s


def timestamp(d: datetime.datetime) -> str:
    return str(d.timestamp() * 1000).split(".")[0]
