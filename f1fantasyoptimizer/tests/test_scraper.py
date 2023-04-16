import pytest
import f1fantasyoptimizer.data as data


def test_f1_website():
    pick_data = data.download_pick_data()
    assert len(pick_data)

    seasons = data.download_seasons()
    assert len(seasons)

    season = max(seasons)  # get most recent year
    venues = data.download_venues(season)
    assert len(venues)

    venue_id = next(iter(venues.values()))
    event_modes = data.download_event_modes(venue_id=venue_id, season=season)
    assert len(event_modes)

    modes = list(event_modes.values())
    event_data = data.download_event_data(venue_id=venue_id, season=season, modes=modes)
    assert len(event_data)
