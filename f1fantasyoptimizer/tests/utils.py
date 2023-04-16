import f1fantasyoptimizer.data as data
from f1fantasyoptimizer.data import Pick


def print_pick_data(pick_data: data.PickData):
    print("{")
    for i, p in pick_data.items():
        print("    ", end='')
        print(f'{i}: Pick({p.pick_id}, Pick.PickType.{p.pick_type}, "{p.name}", {p.points}, {p.cost}, {p.team_id}, '
              f'td={p.td}),')
    print("}")


def get_pick_data():
    return {
        29: Pick(29, Pick.PickType.CONSTRUCTOR, "Red Bull Racing", 173.0, 27.2, 29, td=False),
        131: Pick(131, Pick.PickType.DRIVER, "Max Verstappen", 96.0, 26.9, 29, td=False),
        28: Pick(28, Pick.PickType.CONSTRUCTOR, "Mercedes", 89.0, 25.1, 28, td=False),
        110: Pick(110, Pick.PickType.DRIVER, "Lewis Hamilton", 35.0, 23.7, 28, td=False),
        25: Pick(25, Pick.PickType.CONSTRUCTOR, "Ferrari", 90.0, 22.1, 25, td=False),
        115: Pick(115, Pick.PickType.DRIVER, "Charles Leclerc", 16.0, 21.2, 25, td=False),
        124: Pick(124, Pick.PickType.DRIVER, "George Russell", 34.0, 18.6, 28, td=False),
        121: Pick(121, Pick.PickType.DRIVER, "Sergio Perez", 64.0, 18.0, 29, td=False),
        125: Pick(125, Pick.PickType.DRIVER, "Carlos Sainz", 31.0, 17.2, 25, td=False),
        117: Pick(117, Pick.PickType.DRIVER, "Lando Norris", 6.0, 11.2, 27, td=False),
        23: Pick(23, Pick.PickType.CONSTRUCTOR, "Alpine", 36.0, 10.1, 23, td=False),
        118: Pick(118, Pick.PickType.DRIVER, "Esteban Ocon", -10.0, 9.4, 23, td=False),
        27: Pick(27, Pick.PickType.CONSTRUCTOR, "McLaren", -2.0, 9.1, 27, td=False),
        12: Pick(12, Pick.PickType.DRIVER, "Fernando Alonso", 62.0, 8.3, 24, td=False),
        18: Pick(18, Pick.PickType.DRIVER, "Pierre Gasly", 26.0, 8.1, 23, td=False),
        13: Pick(13, Pick.PickType.DRIVER, "Valtteri Bottas", 11.0, 7.8, 21, td=False),
        129: Pick(129, Pick.PickType.DRIVER, "Lance Stroll", 3.0, 7.5, 24, td=False),
        1982: Pick(1982, Pick.PickType.DRIVER, "Oscar Piastri", -14.0, 7.0, 27, td=False),
        24: Pick(24, Pick.PickType.CONSTRUCTOR, "Aston Martin", 75.0, 6.7, 24, td=False),
        116: Pick(116, Pick.PickType.DRIVER, "Kevin Magnussen", 17.0, 6.7, 26, td=False),
        22: Pick(22, Pick.PickType.CONSTRUCTOR, "AlphaTauri", 32.0, 6.4, 22, td=False),
        21: Pick(21, Pick.PickType.CONSTRUCTOR, "Alfa Romeo", 38.0, 6.2, 21, td=False),
        11: Pick(11, Pick.PickType.DRIVER, "Alexander Albon", -4.0, 5.5, 210, td=False),
        26: Pick(26, Pick.PickType.CONSTRUCTOR, "Haas F1 Team", 25.0, 5.3, 26, td=False),
        210: Pick(210, Pick.PickType.CONSTRUCTOR, "Williams", 9.0, 5.1, 210, td=False),
        14: Pick(14, Pick.PickType.DRIVER, "Nyck De Vries", 15.0, 5.0, 22, td=False),
        134: Pick(134, Pick.PickType.DRIVER, "Zhou Guanyu", 21.0, 4.9, 21, td=False),
        130: Pick(130, Pick.PickType.DRIVER, "Yuki Tsunoda", 17.0, 4.8, 22, td=False),
        111: Pick(111, Pick.PickType.DRIVER, "Nico Hulkenberg", 0.0, 4.3, 26, td=False),
        126: Pick(126, Pick.PickType.DRIVER, "Logan Sargeant", 13.0, 4.0, 210, td=False),
    }


def get_team_names():
    driver0 = "Max Verstappen"
    driver1 = "Fernando Alonso"
    driver2 = "Sergio Perez"
    driver3 = "Lance Stroll"
    driver4 = "Zhou Guanyu"
    constructor0 = "Red Bull Racing"
    constructor1 = "Aston Martin"
    td = driver0
    team_names = ([driver0, driver1, driver2, driver3, driver4,
                   constructor0, constructor1], td)
    return team_names
