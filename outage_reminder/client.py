import datetime

import httpx

from outage_reminder.datetime_utils import utcnow, timestamp, isoformat_datetime
from outage_reminder.types import OutageItem, OutageResponse, CitiesItem, StreetsItem

OUTAGES_API_URL = "https://www.tauron-dystrybucja.pl/waapi/outages"
GEO_API_URL = "https://www.tauron-dystrybucja.pl/waapi/enum/geo"


def get_outages(
    city_id: int,
    street_id: int,
    house_no: str,
    from_date: datetime.datetime,
    to_date: datetime.datetime,
) -> list[OutageItem]:
    url = f"{OUTAGES_API_URL}/address"

    response = httpx.get(
        url,
        params={
            "cityGAID": city_id,
            "streetGAID": street_id,
            "houseNo": house_no,
            "fromDate": isoformat_datetime(from_date),
            "toDate": isoformat_datetime(to_date),
            "getLightingSupport": True,
            "getServicedSwitchingoff": True,
            "_": timestamp(
                from_date
            ),  # timestamp of a request, we're sending it to impersonate web client
        },
    )
    response.raise_for_status()
    response_body: OutageResponse = response.json()
    return response_body["OutageItems"]


def find_city(name: str) -> list[CitiesItem]:
    url = f"{GEO_API_URL}/cities"

    response = httpx.get(
        url,
        params={
            "partName": name,
            "_": timestamp(utcnow()),
        },
    )
    response.raise_for_status()
    response_body: list[CitiesItem] = response.json()
    return response_body


def find_street(name: str, city_id: int) -> list[StreetsItem]:
    url = f"{GEO_API_URL}/streets"

    response = httpx.get(
        url,
        params={
            "partName": name,
            "ownerGAID": city_id,
            "_": timestamp(utcnow()),
        },
    )
    response.raise_for_status()
    response_body: list[StreetsItem] = response.json()
    return response_body
