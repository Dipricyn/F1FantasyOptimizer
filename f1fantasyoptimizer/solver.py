from ortools.sat.python import cp_model

import f1fantasyoptimizer.data as data

# constants
BUDGET: float = 100  # mil. Dollars
NUMBER_OF_DRIVERS: int = 5
NUMBER_OF_CONSTRUCTORS: int = 2
CAPACITY: int = NUMBER_OF_DRIVERS + NUMBER_OF_CONSTRUCTORS

MAX_POINTS_PER_PICK: float = 500


def solve(pick_data: data.PickData) -> data.Team:
    # Preprocess pick data
    pick_data_list = list(pick_data.values())
    n_pick_data = len(pick_data_list)

    # Create model
    model = cp_model.CpModel()

    # Input variables
    # Flag indicating whether each driver is picked for the team or not
    d_select = [model.NewBoolVar('d') for _ in range(n_pick_data)]
    # Flag indicating which driver is the turbo driver
    t_select = [model.NewBoolVar('t') for _ in range(n_pick_data)]

    # Auxiliary variables
    # u = x * pts(x)
    u = [model.NewIntVar(-MAX_POINTS_PER_PICK * 10, MAX_POINTS_PER_PICK * 10, "u") for _ in range(n_pick_data)]
    # v = t * pts(x)
    v = [model.NewIntVar(-MAX_POINTS_PER_PICK * 10, MAX_POINTS_PER_PICK * 10, "v") for _ in range(n_pick_data)]

    for i in range(n_pick_data):
        # Multiply by 10 to convert the values to int
        model.AddMultiplicationEquality(u[i], [d_select[i], int(round(pick_data_list[i].points * 10))])

    for i in range(n_pick_data):
        # Multiply by 10 to convert the values to int
        model.AddMultiplicationEquality(v[i], [t_select[i], int(round(pick_data_list[i].points * 10))])

    # Team capacity constraint
    model.Add(sum(d_select) == CAPACITY)

    # Budget constraint
    # Multiply by 10 to convert the values to int
    model.Add(sum([d_select[i] * int(round(pick_data_list[i].cost * 10)) for i in range(n_pick_data)]) <= BUDGET * 10)

    # Turbo driver constraint:
    # Selected turbo driver must be one of the selected drivers
    for i in range(n_pick_data):
        model.AddImplication(t_select[i], d_select[i])

    # Turbo driver can't be a constructor
    model.Add(sum([t_select[i] for i in range(n_pick_data) if
                   pick_data_list[i].pick_type == data.Pick.PickType.CONSTRUCTOR]) == 0)
    # Turbo driver must be exactly 1 driver
    model.Add(
        sum([t_select[i] for i in range(n_pick_data) if pick_data_list[i].pick_type == data.Pick.PickType.DRIVER]) == 1)

    # Constructor constraint
    model.Add(sum([d_select[i] for i in range(n_pick_data)
                   if pick_data_list[i].pick_type == data.Pick.PickType.CONSTRUCTOR]) == NUMBER_OF_CONSTRUCTORS)

    # Maximize sum of points of selected drivers and selected turbo driver
    # u: Int = x * pts(x)  # points of selected drivers
    # v: Int = t * pts(x)  # points of selected turbo driver
    # t => x  # selected turbo driver must be one of the selected drivers
    # max(u + v)
    model.Maximize(sum([u[i] + v[i] for i in range(n_pick_data)]))

    # Create solver
    solver = cp_model.CpSolver()
    # solver.parameters.log_search_progress = True
    model.Proto().objective.scaling_factor = -1. / 10  # Inverse scaling for solver logging output
    # Solve model
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        # Create list of selected drivers
        picks = []
        for i in range(n_pick_data):
            if solver.Value(d_select[i]) == 1:
                pick = pick_data_list[i]
                pick.td = solver.Value(t_select[i]) == 1
                picks.append(pick)
        return picks
    else:
        raise RuntimeError(f"Model solving failed: {status}!")
