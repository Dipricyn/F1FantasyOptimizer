import enum
import io
import json
import urllib.request
from datetime import datetime
from typing import TypeAlias

from lxml import html


class Pick:
    """
    Class representing one driver or constructor.
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


PickData: TypeAlias = dict[int, Pick]
Team: TypeAlias = list[Pick]


def create_team_from_names(team: tuple[list[str], str], pick_data: PickData) -> Team:
    t = []
    for name in team[0]:
        pick = pick_data[find_pick_by_name(pick_data, name)]
        pick.td = name == team[1]
        t.append(pick)
    return t


def reset_points(pick_data: PickData):
    for pick in pick_data.values():
        pick.points = 0


def to_float(value, *, default=0.0) -> float:
    if not value:
        return default
    return float(value)


pick_data_URL: str = "https://fantasy.formula1.com/feeds/drivers/1_en.json"


def download_pick_data() -> PickData:
    with urllib.request.urlopen(pick_data_URL) as response:
        entries = json.loads(response.read())["Data"]["Value"]
        pick_data = dict()
        for entry in entries:
            pick_id = int(entry["PlayerId"])
            pick_data[pick_id] = Pick(
                pick_id=pick_id,
                pick_type=Pick.PickType[entry["PositionName"].upper()],
                name=entry["FUllName"],
                points=to_float(entry["OverallPpints"]),
                cost=to_float(entry["Value"]),
                team_id=int(entry["TeamId"]),
            )
        return pick_data


def find_pick_by_name(pick_data: PickData, name: str) -> int:
    for k, v in pick_data.items():
        if v.name == name:
            return k


EVENT_DATA_URL: str = "https://www.formula1.com/en/results/jcr:content/resultsarchive.html" \
                      "/{year}/races/{event_link}/{mode}.html"

Events: TypeAlias = dict[str, str]

EVENTS_OVERVIEW_DATA_URL: str = "https://www.formula1.com/en/results/jcr:content/resultsarchive.html/{year}/races.html"


def download_events_years() -> list[int]:
    with urllib.request.urlopen(EVENTS_OVERVIEW_DATA_URL.format(year=datetime.today().year)) as response:
        s = response.read()
        sio = io.StringIO(s.decode("UTF-8"))
        tree = html.parse(sio)
        years = tree.xpath("//select[@class='resultsarchive-filter-form-select' and @name='year']"
                           "/option/text()")
        return [int(y) for y in years]


def download_events(year: int) -> Events:
    events = dict()
    with urllib.request.urlopen(EVENTS_OVERVIEW_DATA_URL.format(year=year)) as response:
        s = response.read()
        sio = io.StringIO(s.decode("UTF-8"))
        tree = html.parse(sio)
        events_html = tree.xpath("//select[@class='resultsarchive-filter-form-select' and @name='meetingKey']"
                                 "/option[string(@value)]")
        for event in events_html:
            events[event.text] = event.attrib["value"]
    return events


def download_event_modes(events: Events, *, place: str, year: int) -> dict[str, str]:
    modes: dict[str, str] = dict()
    with urllib.request.urlopen(EVENT_DATA_URL.format(year=year, event_link=events[place], mode="race")) as response:
        s = response.read()
        sio = io.StringIO(s.decode("UTF-8"))
        tree = html.parse(sio)
        for mode in tree.xpath("//select[@class='resultsarchive-filter-form-select' and @name='resultType']/option"):
            modes[mode.text] = mode.attrib["value"]
    return modes


def download_event_data(events: Events, *, place: str, year: int, modes: list[str]) \
        -> dict[str, list[tuple[str, str]]]:
    event_data = dict()
    for mode in modes:
        with urllib.request.urlopen(EVENT_DATA_URL.format(year=year, event_link=events[place], mode=mode)) as response:
            s = response.read()
            sio = io.StringIO(s.decode("UTF-8"))
            tree = html.parse(sio)
            mode_data = []
            for entry in tree.xpath("//table[@class='resultsarchive-table']/tbody/tr"):
                pos = entry.xpath("td[2]/text()")[0]
                name_fields = entry.xpath("td[4]/descendant::*/text()")
                name = " ".join(filter(None, [name_fields[0], name_fields[1]]))
                mode_data.append((pos, name))
            event_data[mode] = mode_data
    return event_data
