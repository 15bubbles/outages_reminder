import pytest

from outage_reminder.parser import filter_outages
from outage_reminder.types import OutageItem


def dobrzykowice_outage_item() -> OutageItem:
    return {
        "OutageId": "df299f57-0e12-4518-a688-843be27b0fe5",
        "Modified": "2024-06-14T05:06:09.917Z",
        "StartDate": "2024-06-25T06:30:00Z",
        "EndDate": "2024-06-25T10:30:00Z",
        "IdsWWW": [6],
        "AddressPointIds": [],
        "Message": "Dobrzykowice ul. Ogrodowa, Spokojna, Polna, Akacjowa, Krótka, Wiosenna i działki przyległe. Gm. Czernica.",
        "TypeId": 1,
        "IsActive": True,
    }


def wojnowice_outage_item() -> OutageItem:
    return {
        "OutageId": "98e6556e-9245-4c50-b572-bd15d54d29d5",
        "Modified": "2024-06-14T05:17:33.754Z",
        "StartDate": "2024-06-25T06:00:00Z",
        "EndDate": "2024-06-25T12:00:00Z",
        "IdsWWW": [6],
        "AddressPointIds": [],
        "Message": "Wojnowice ul. Słoneczna, Pogodna. Gm. Czernica.",
        "TypeId": 1,
        "IsActive": True,
    }


@pytest.mark.parametrize(
    ["given_outages", "given_kwargs", "expected"],
    [
        (
            [dobrzykowice_outage_item(), wojnowice_outage_item()],
            {"city_name": "Dobrzykowice", "street_name": "Ogrodowa"},
            [dobrzykowice_outage_item()],
        ),
        (
            [dobrzykowice_outage_item(), wojnowice_outage_item()],
            {"city_name": "Dobrzykowice"},
            [dobrzykowice_outage_item()],
        ),
        (
            [dobrzykowice_outage_item(), wojnowice_outage_item()],
            {"street_name": "Słoneczna"},
            [wojnowice_outage_item()],
        ),
        (
            [dobrzykowice_outage_item(), wojnowice_outage_item()],
            {},
            [dobrzykowice_outage_item(), wojnowice_outage_item()],
        ),
    ],
)
def test_filter_outages(
    given_outages: list[OutageItem],
    given_kwargs: dict[str, str],
    expected: list[OutageItem],
) -> None:
    actual = filter_outages(given_outages, **given_kwargs)

    assert actual == expected
