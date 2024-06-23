from outage_reminder.types import OutageItem


def filter_outages(
    outages: list[OutageItem], *, city_name: str = "", street_name: str = ""
) -> list[OutageItem]:
    return [
        item
        for item in outages
        if city_name in item["Message"] and street_name in item["Message"]
    ]
