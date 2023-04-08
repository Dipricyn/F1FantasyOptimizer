import pytest
import f1fantasyoptimizer.data as data


def test_f1_website():
    pick_data = data.download_pick_data()
    assert len(pick_data)

    years = data.download_events_years()
    assert len(years)

    year = max(years)  # get most recent year
    events = data.download_events(year)
    assert len(events)

    place = next(iter(events))
    event_modes = data.download_event_modes(events, place=place, year=year)
    assert len(event_modes)

    modes = list(event_modes.values())
    event_data = data.download_event_data(events, place=place, year=year, modes=modes)
    assert len(event_data)
