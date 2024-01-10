from ortools.linear_solver import pywraplp
import pandas as pd
import championship_team_data as cd
from ortools.sat.python import cp_model
import curr_data as data
import heapq


SALARY_CAP = 136000000
data = data.data()
cd = cd.cd()


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.possible_solutions = []
        self.indexes = []

    def on_solution_callback(self):
        solution = []
        indices = []
        self.__solution_count += 1
        for i, v in enumerate(self.__variables):
            if self.Value(v) > 0:
                solution.append(v)
                indices.append(i)
        self.possible_solutions.append(solution)
        self.indexes.append(indices)
        # print(len(solution))


    def get_solutions(self):
        return self.possible_solutions, self.indexes


    def solution_count(self):
        return self.__solution_count

class cp:

    def __init__(self):
        self.model = cp_model.CpModel()
        self.player_vars = [self.model.NewIntVar(0, 1, player) for player in data.get_players()]
        self.prev = []
        self.rebounder = 0
        self.assister = 0
        self.pointers = 0
        self.attempts = 1
        self.set_positions()

    def set_positions(self):
        self.centers = []
        self.point_guards = []
        self.power_forwards = []
        self.shooting_guards = []
        self.small_forwards = []
        position = data.get_positions()
        for i, player in enumerate(self.player_vars):
            if position[i] == 'C':
                self.centers.append(i)
            elif position[i] == 'SG':
                self.shooting_guards.append(i)
            elif position[i] == 'PG':
                self.point_guards.append(i)
            elif position[i] == 'PF':
                self.power_forwards.append(i)
            elif position[i] == 'SF':
                self.small_forwards.append(i)



    def add_salary_cap_constraint(self):
        self.model.Add(sum([player * int(data.get_salaries()[i]) for i, player in enumerate(self.player_vars)]) <= SALARY_CAP)
        # constraint the sum of the teams salaries has to be greater than 0
        self.model.Add(sum([player * int(data.get_salaries()[i]) for i, player in enumerate(self.player_vars)]) > 100000000)

    def add_position_constraints(self):
        self.model.Add(sum(self.player_vars[i] for i in self.centers) <= 3)
        self.model.Add(sum(self.player_vars[i] for i in self.point_guards) <= 3)
        self.model.Add(sum(self.player_vars[i] for i in self.power_forwards) <= 3)
        self.model.Add(sum(self.player_vars[i] for i in self.small_forwards) <= 3)
        self.model.Add(sum(self.player_vars[i] for i in self.shooting_guards) <= 3)
        self.model.Add(sum(self.player_vars[i] for i in self.centers) > 2)
        self.model.Add(sum(self.player_vars[i] for i in self.point_guards) > 2)
        self.model.Add(sum(self.player_vars[i] for i in self.power_forwards) > 2)
        self.model.Add(sum(self.player_vars[i] for i in self.small_forwards) > 2)
        self.model.Add(sum(self.player_vars[i] for i in self.shooting_guards) > 2)

    def get_possible_solutions(self):
        self.add_position_constraints()
        self.add_salary_cap_constraint()
        solver = cp_model.CpSolver()
        solver.parameters.enumerate_all_solutions = True
        solver.parameters.max_time_in_seconds = 20.0
        solution_printer = VarArraySolutionPrinter(self.player_vars)
        status = solver.Solve(self.model, solution_printer)
        print(f"Status = {solver.StatusName(status)}")
        print(f"Number of solutions found: {solution_printer.solution_count()}")
        solutions, indexes = solution_printer.get_solutions()
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            return solutions, indexes
        else:
            return Exception('None found')

    def update_maximizer(self, i):
        if i == 0:
            self.pointers += 1
        elif i == 1:
            self.rebounder += 1
        elif i == 2:
            self.assister += 1
        elif i == 3:
            self.attempts = self.attempts / 2


