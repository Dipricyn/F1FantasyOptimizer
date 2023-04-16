import abc
import enum
import io
import json
import urllib.request
from datetime import datetime
from typing import Any, Optional, TypeAlias

from lxml import html

EVENT_DATA_URL: str = "https://www.formula1.com/en/results/jcr:content/resultsarchive.html" \
                      "/{year}/races/{event_link}/{mode}.html"

EVENTS_OVERVIEW_DATA_URL: str = "https://www.formula1.com/en/results/jcr:content/resultsarchive.html/{year}/races.html"

PICK_DATA_URL: str = "https://fantasy.formula1.com/feeds/drivers/1_en.json"


def to_float(value: str, *, default: float = 0.0) -> float:
    """
    Convenience function for converting a string to a float.

    Will return `default` if value is falsy.
    :param value: the value to convert to a float
    :param default: the value to return if `value` is falsy
    :return: `value` as a `float`
    """
    if not value:
        return default
    return float(value)


class Pick:
    """
    Class representing a driver or a constructor.
    """

    class PickType(enum.Enum):
        DRIVER = 0
        CONSTRUCTOR = 1

        def __str__(self):
            return self.name

    def __init__(self, pick_id: int, pick_type: PickType, name: str, points: float, cost: float, team_id: int, *,
                 td=False):
        self.pick_id = pick_id
        self.pick_type = pick_type
        self.name = name
        self.points = points
        self.cost = cost
        self.team_id = team_id
        self.td = td

    def __str__(self):
        return f"Pick({'[TD] ' if self.td else ''}{self.name}: {self.points} Pts, ${self.cost:.1f}M)"


class Mode(abc.ABC):
    """
    One of the modes of an event.

    For example: sprint race, qualifying, race, etc.
    """
    Name = str
    Id = str


class Venue(abc.ABC):
    """
    The place where the event took place.
    """
    Name = str
    Id = str


Season = int

Modes: TypeAlias = dict[Mode.Name, Mode.Id]
Venues: TypeAlias = dict[Venue.Name, Venue.Id]

EventData: TypeAlias = dict[Mode.Id, list[tuple[str, str]]]
PickData: TypeAlias = dict[int, Pick]
Team: TypeAlias = list[Pick]


def find_pick_by_name(pick_data: PickData, name: str) -> int:
    """
    Find the ID of a pick by their name.
    :param pick_data: object containing all information about all possible picks
    :param name: the name of the pick to find
    :return: the ID of the pick
    """
    for k, v in pick_data.items():
        if v.name == name:
            return k


def create_team_from_names(pick_names: tuple[list[str], str], pick_data: PickData) -> Team:
    """
    Create a team object from a list of names of drivers and constructors.

    The turbo driver is also specified by name.
    :param pick_names: tuple containing a list of names of drivers and constructors as well as the name of the turbo
        driver
    :param pick_data: object containing all information about all possible picks
    :return: the team consisting of picks described by `pick_names`
    """
    team = []
    for name in pick_names[0]:
        pick = pick_data[find_pick_by_name(pick_data, name)]
        pick.td = name == pick_names[1]
        if pick.td and pick.pick_type == Pick.PickType.CONSTRUCTOR:
            raise ValueError("The turbo driver cannot be a constructor, but `{}` was specified.".format(pick_names[1]))
        team.append(pick)
    return team


def reset_points(pick_data: PickData):
    """
    Set the points of all picks to `0`.
    :param pick_data: object containing all information about all possible picks
    """
    for pick in pick_data.values():
        pick.points = 0


def download_pick_data() -> PickData:
    """
    Download information about all possible picks from the F1Fantasy website.
    :return: object containing all information about all possible picks
    """
    with urllib.request.urlopen(PICK_DATA_URL) as response:
        entries = json.loads(response.read())["Data"]["Value"]
        pick_data = dict()
        for entry in entries:
            pick_id = int(entry["PlayerId"])
            pick_data[pick_id] = Pick(
                pick_id=pick_id,
                pick_type=Pick.PickType[entry["PositionName"].upper()],
                name=entry["FUllName"],  # [sic]
                points=to_float(entry["OverallPpints"]),  # [sic]
                cost=to_float(entry["Value"]),
                team_id=int(entry["TeamId"]),
            )
        return pick_data


def download_seasons() -> list[Season]:
    """
    Download all seasons for which information is provided by the website.
    :return: a list of all seasons
    """
    with urllib.request.urlopen(EVENTS_OVERVIEW_DATA_URL.format(year=datetime.today().year)) as response:
        s = response.read()
        sio = io.StringIO(s.decode())
        tree = html.parse(sio)
        years = tree.xpath("//select[@class='resultsarchive-filter-form-select' and @name='year']"
                           "/option/text()")
        return [Season(y) for y in years]


def download_venues(season: Season) -> Venues:
    """
    Download all venues for a given season.
    :param season: the season for which to download the list of venues
    :return: a dictionary consisting of all venues and their IDs for a given season
    """
    venues: Venues = dict()
    with urllib.request.urlopen(EVENTS_OVERVIEW_DATA_URL.format(year=season)) as response:
        s = response.read()
        sio = io.StringIO(s.decode())
        tree = html.parse(sio)
        venues_html = tree.xpath("//select[@class='resultsarchive-filter-form-select' and @name='meetingKey']"
                                 "/option[string(@value)]")
        for venue in venues_html:
            venue_name: Venue.Name = venue.text
            venue_id: Venue.Id = venue.attrib["value"]
            venues[venue_name] = venue_id
    return venues


def download_event_modes(*, season: Season, venue_id: Venue.Id) \
        -> dict[Mode.Name, Mode.Id]:
    """
    Download modes for a given venue in a given season.
    :param season: the season for which to download the data
    :param venue_id: the venue for which to download the data
    :return: a dictionary consisting of all modes and their IDs for a given venue in a given season
    """
    modes: Modes = dict()
    with urllib.request.urlopen(EVENT_DATA_URL.format(year=season, event_link=venue_id, mode="race")) as response:
        s = response.read()
        sio = io.StringIO(s.decode())
        tree = html.parse(sio)
        for mode in tree.xpath("//select[@class='resultsarchive-filter-form-select' and @name='resultType']/option"):
            modes[mode.text] = mode.attrib["value"]
    return modes


def download_event_data(*, season: Season, venue_id: Venue.Id, modes: list[Mode.Id]) \
        -> EventData:
    """
    Download placement data for a given list of modes of a given venue in a given season.
    :param season: the season for which to download the data
    :param venue_id: the venue for which to download the data
    :param modes: a list of modes for which to download placement data
    :return: dictionary containing all specified modes and for each specified mode a list of the placement of a driver
        and their name
    """
    event_data: EventData = dict()
    for mode in modes:
        with urllib.request.urlopen(EVENT_DATA_URL.format(year=season, event_link=venue_id, mode=mode)) as response:
            s = response.read()
            sio = io.StringIO(s.decode())
            tree = html.parse(sio)
            mode_data = []
            for entry in tree.xpath("//table[@class='resultsarchive-table']/tbody/tr"):
                pos = entry.xpath("td[2]/text()")[0]
                name_fields = entry.xpath("td[4]/descendant::*/text()")
                name = " ".join(filter(None, [name_fields[0], name_fields[1]]))
                mode_data.append((pos, name))
            event_data[mode] = mode_data
    return event_data
