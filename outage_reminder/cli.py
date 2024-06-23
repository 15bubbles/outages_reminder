import datetime
import sys

import click
from rich import print

from outage_reminder.client import find_city, find_street, get_outages
from outage_reminder.datetime_utils import utcnow
from outage_reminder.parser import filter_outages


# TODO: parameters for start date and end date
# TODO: nicer output if there's 0 results for outages
# TODO: better logging with INFO/ERROR/etc prefixes added by default
#  also check if there is a way to automatically turn on verbosity to
#  not add a handful number of `if` statements
# TODO: better output for outages in general (including start date, end date and message)
@click.command()
@click.option("-c", "--city", required=True, help="")
@click.option("-s", "--street", required=True, help="")
@click.option("-h", "--house", required=False, help="")
@click.option("--all", required=False, is_flag=True, help="")
def list_outages(city: str, street: str, house: str, all: bool) -> None:
    print(f"INFO: Searching city '{city}'...")
    cities = find_city(city)

    if len(cities) == 0:
        print(f"ERROR: City '{city}' was not found by the API")
        sys.exit(1)

    # TODO: multiple cities with similar names could be a valid scenario
    #  so there's a need to allow for providing more specific information
    if len(cities) > 1:
        print(
            f"ERROR: More than 1 city was found for '{city}', please be more specific"
        )
        sys.exit(1)

    city_id = cities[0]["GAID"]
    city_name = cities[0]["Name"]

    print(f"INFO: Searching street '{street}' in '{city_name}'")
    streets = find_street(street, city_id)

    if len(streets) == 0:
        print(f"ERROR: Street '{street}' in '{city_name}' was not found by the API")
        sys.exit(1)

    if len(streets) > 1:
        print(
            f"ERROR: More than 1 street was found in '{city_name}', please be more specific"
        )
        sys.exit(1)

    street_id = streets[0]["GAID"]
    street_name = streets[0]["Name"]

    print(f"INFO: Searching for outages in '{city_name}' at '{street_name}'...")
    from_date = utcnow()
    to_date = utcnow() + datetime.timedelta(days=5)
    outages = get_outages(city_id, street_id, house, from_date, to_date)

    if not all:
        outages = filter_outages(outages, city_name=city_name, street_name=street_name)

    print(outages)
    sys.exit(0)
