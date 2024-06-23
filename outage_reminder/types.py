from typing import Any, TypedDict


# TODO: perhaps some dataclasses or pydantic dataclasses/models would be better than
# typed dicts
OutageItem = TypedDict(
    "OutageItem",
    {
        "OutageId": str,
        "Modified": str,
        "StartDate": str,
        "EndDate": str,
        "IdsWWW": list[int],
        "AddressPointIds": list[Any],
        "Message": str,
        "TypeId": int,
        "IsActive": bool,
    },
)

OutageResponse = TypedDict(
    "OutageResponse",
    {
        "OutageListType": int,
        "AddressPoint": Any,
        "IdsWWW": list[int],
        "AddressLightingSupport": dict[str, Any],
        "ServicedSwitchingoff": bool | None,
        "OutageItems": list[OutageItem],
    },
)

CitiesItem = TypedDict(
    "CitiesItem",
    {
        "GUS": str,
        "DistrictGAID": int,
        "ProvinceGAID": int,
        "CountryGAID": int,
        "CommuneName": str,
        "DistrictName": str,
        "ProvinceName": str,
        "GAID": int,
        "OwnerGAID": int,
        "Name": str,
    },
)

StreetsItem = TypedDict(
    "StreetsItem",
    {
        "StreetGUS": str,
        "Prefix": str,
        "PostFix": str | None,
        "FullName": str,
        "ShortName": str,
        "GAID": int,
        "OwnerGAID": int,
        "Name": str,
    },
)
