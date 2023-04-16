#!/usr/bin/env python3
import f1fantasyoptimizer.data as data
import f1fantasyoptimizer.simulator as simulator
import f1fantasyoptimizer.solver as solver

# Select event for which to download event data
SEASON: data.Season = 2023
VENUE_NAME: data.Venue.Name = "Bahrain"

# Select a team which should also be evaluated
YOUR_TEAM = (["Max Verstappen", "Fernando Alonso", "Sergio Perez", "Lance Stroll", "Zhou Guanyu",
              "Red Bull Racing", "Aston Martin"], "Max Verstappen")

# MODE = None
MODE = "qualifying"


def print_team(picks: data.Team):
    picks = sorted(picks, key=lambda p: (str(p.pick_type), p.cost), reverse=True)
    for pick in picks:
        print(pick)
    total = simulator.calculate_team_totals(picks)
    print(f"Team total: {total['points']} Pts, ${total['cost']:.1f}M")


def print_pick_data(pick_data: data.PickData):
    print("Simulation result:")
    for pick in sorted(pick_data.values(), key=lambda p: p.points, reverse=True):
        print(f"{pick.name}: {pick.points} Pts")
    print()


def main():
    venues = data.download_venues(SEASON)
    pick_data = data.download_pick_data()

    if MODE:
        data.reset_points(pick_data)
        event_data = data.download_event_data(venue_id=venues[VENUE_NAME], season=SEASON, modes=[MODE])
        simulator.simulate(pick_data, event_data[MODE])
        print_pick_data(pick_data)

    print("Best team:")
    best_team = solver.solve(pick_data)
    print_team(best_team)
    print()

    print("Your team:")
    your_picks = data.create_team_from_names(YOUR_TEAM, pick_data)
    print_team(your_picks)
    print()


if __name__ == '__main__':
    main()
