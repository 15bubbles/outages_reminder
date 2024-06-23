import datetime

import pytest

from outage_reminder.datetime_utils import isoformat_datetime, timestamp


@pytest.mark.parametrize(
    ["given_datetime", "expected"],
    [
        (
            datetime.datetime(2024, 6, 22, 11, 52, 25, 0, datetime.timezone.utc),
            "2024-06-22T11:52:25.000Z",
        ),
        (datetime.datetime(2024, 6, 22, 11, 52, 25, 0), "2024-06-22T11:52:25.000"),
    ],
)
def test_isoformat_datetime(given_datetime: datetime.datetime, expected: str) -> None:
    actual = isoformat_datetime(given_datetime)

    assert actual == expected


def test_timestamp() -> None:
    d = datetime.datetime(2024, 6, 22, 11, 52, 25, 0, datetime.timezone.utc)
    expected = "1719057145000"

    actual = timestamp(d)

    assert actual == expected


# TODO: write test for utcnow function, but it will probably require
#  some library like `freezegun`
