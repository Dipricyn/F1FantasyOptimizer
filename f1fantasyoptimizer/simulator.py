import f1fantasyoptimizer.data as data

RACE_POINTS: dict[str, int] = {
    "0": 25,
    "1": 18,
    "2": 15,
    "3": 12,
    "4": 10,
    "5": 8,
    "6": 6,
    "7": 4,
    "8": 2,
    "9": 1,
    "DNF": -20,
    "DQ": -25,
}


def simulate(pick_data: data.PickData, order: list[tuple[str, str]]):
    # Calculate drivers' points
    points = 10
    for i, (_, driver) in enumerate(order):
        pick_id = data.find_pick_by_name(pick_data, driver)
        # Qualifying
        pick_data[pick_id].points += points
        if points > 0:
            points -= 1
        # Race
        pick_data[pick_id].points += RACE_POINTS.get(str(i), 0)

    # Calculate constructors' points by adding points of their drivers
    for pick_id, pick in pick_data.items():
        if pick.pick_type == data.Pick.PickType.DRIVER:
            constructor_id = pick_data[pick.team_id].pick_id
            pick_data[constructor_id].points += pick.points


def calculate_team_totals(team: data.Team) -> dict[str, float]:
    total_points = 0
    total_cost = 0
    for pick in team:
        total_points += pick.points * (2 if pick.td else 1)
        total_cost += pick.cost
    return {
        "points": total_points,
        "cost": total_cost
    }
