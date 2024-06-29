import datetime
import json
import sys

import click
from rich import print

from outage_reminder.client import find_city, find_street, get_outages
from outage_reminder.datetime_utils import utcnow
from outage_reminder.parser import filter_outages
from outage_reminder.types import OutageItem, OutageType

# TODO: better logging with INFO/ERROR/etc prefixes added by default
#  also check if there is a way to automatically turn on verbosity to
#  not add a handful number of `if` statements


def pretty_print(outages: list[OutageItem]) -> None:
    if len(outages) == 0:
        click.echo("\nNo outages found for given location")

    for outage in outages:
        click.echo("\n---")
        click.echo(f"Start: {outage['StartDate']}")
        click.echo(f"End: {outage['EndDate']}")
        click.echo(f"Type: {OutageType(outage['TypeId']).name}")
        click.echo(f"{outage['Message']}")


def raw_print(outages: list[OutageItem]) -> None:
    click.echo(
        json.dumps(
            [
                {
                    "StartDate": outage["StartDate"],
                    "EndDate": outage["EndDate"],
                    "Message": outage["Message"],
                    "Type": OutageType(outage["TypeId"]).name,
                }
                for outage in outages
            ],
            indent=2,
        )
    )


@click.command()
@click.option(
    "-c",
    "--city",
    help=(
        "Name of the city for which outages should be found "
        '(if city name has to parts put it in quotes, e.g. "Mińsk Mazowiecki")'
    ),
    required=True,
)
@click.option(
    "-s",
    "--street",
    help=(
        "Name of the street in given city for which outages should be found "
        '(if street name has two parts, put it in quotes, e.g. "Świętego Jana")'
    ),
    required=True,
)
@click.option(
    "-h",
    "--house",
    help="Number of the house for which outages should be found",
    required=False,
)
@click.option(
    "-f",
    "--from",
    "from_",
    default=utcnow(),
    help="Start date for which outages should be found. By default it's current datetime",
    required=False,
    type=click.DateTime(),
)
@click.option(
    "-t",
    "--to",
    help="End date for which outages should be found. By default it's 5 days from current datetime",
    default=utcnow() + datetime.timedelta(days=5),
    required=False,
    type=click.DateTime(),
)
@click.option(
    "--all",
    "all_",
    is_flag=True,
    help=(
        "If specified, then all outages found by API will be printed out "
        "(outages in vicinity of given location), otherwise they are filtered "
        "to only show outages specific for given city and street"
    ),
    required=False,
)
@click.option(
    "--raw",
    is_flag=True,
    help="If specified, output is printed as JSON",
)
def list_outages(
    city: str,
    street: str,
    house: str,
    from_: datetime.datetime,
    to: datetime.datetime,
    all_: bool,
    raw: bool,
) -> None:
    click.echo(f"INFO: Searching city '{city}'...", err=True)
    cities = find_city(city)

    if len(cities) == 0:
        click.echo(f"ERROR: City '{city}' was not found by the API", err=True)
        sys.exit(1)

    # TODO: multiple cities with similar names could be a valid scenario
    #  so there's a need to allow for providing more specific information
    if len(cities) > 1:
        click.echo(
            f"ERROR: More than 1 city was found for '{city}', please be more specific",
            err=True,
        )
        sys.exit(1)

    city_id = cities[0]["GAID"]
    city_name = cities[0]["Name"]

    click.echo(f"INFO: Searching street '{street}' in '{city_name}'", err=True)
    streets = find_street(street, city_id)

    if len(streets) == 0:
        click.echo(
            f"ERROR: Street '{street}' in '{city_name}' was not found by the API",
            err=True,
        )
        sys.exit(1)

    if len(streets) > 1:
        click.echo(
            f"ERROR: More than 1 street was found in '{city_name}', please be more specific",
            err=True,
        )
        sys.exit(1)

    street_id = streets[0]["GAID"]
    street_name = streets[0]["Name"]

    click.echo(
        f"INFO: Searching for outages in '{city_name}' at '{street_name}'...", err=True
    )
    from_date = from_.astimezone(datetime.timezone.utc)
    to_date = to.astimezone(datetime.timezone.utc)
    outages = get_outages(city_id, street_id, house, from_date, to_date)

    if not all_:
        outages = filter_outages(outages, city_name=city_name, street_name=street_name)

    if raw:
        raw_print(outages)
    else:
        pretty_print(outages)

    sys.exit(0)
