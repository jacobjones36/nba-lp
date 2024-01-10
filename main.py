from ortools.linear_solver import pywraplp
import pandas as pd
from ortools.sat.python import cp_model
import championship_team_data as cd
import curr_data as data
import financial as mc
import math

SALARY_CAP = 136000000
GAME_LENGTH = 48


def get_champ_avg():
    print(f"{sum(cd.get_points()) / 11} \n{sum(cd.get_rebounds()) / 11} \n {sum(cd.get_turnovers()) / 11}"
          f"\n{sum(cd.get_fg_attempts()) / 11}\n{sum(cd.get_fg_percent()) / 11}\n{sum(cd.get_assists()) / 11}")


class Optimizer():
    def __init__(self):
        self.player_vars = []
        self.max = 0
        self.possible_solutions = []
        self.possible_solution, self.indexes = m.get_possible_solutions()
        for i, sol in enumerate(self.possible_solution):
            self.curr_i = self.indexes[i]
            self.get_optimal_team(sol)

    def minutes_played(self):
        c = self.solver.Constraint(0, 48)
        pf = self.solver.Constraint(0, 48)
        pg = self.solver.Constraint(0, 48)
        sg = self.solver.Constraint(0, 48)
        sf = self.solver.Constraint(0, 48)
        for i, player in enumerate(self.player_vars):
            if data.get_positions()[self.curr_i[i]] == 'C':
                c.SetCoefficient(player, data.get_minutes_played()[self.curr_i[i]])
            elif data.get_positions()[self.curr_i[i]] == 'PF':
                pf.SetCoefficient(player, data.get_minutes_played()[self.curr_i[i]])
            elif data.get_positions()[self.curr_i[i]] == 'PG':
                pg.SetCoefficient(player, data.get_minutes_played()[self.curr_i[i]])
            elif data.get_positions()[self.curr_i[i]] == 'SG':
                sg.SetCoefficient(player, data.get_minutes_played()[self.curr_i[i]])
            else:
                sf.SetCoefficient(player, data.get_minutes_played()[self.curr_i[i]])

    def add_rebounds(self):
        r = self.solver.Constraint(44, math.inf)
        for i, player in enumerate(self.player_vars):
            r.SetCoefficient(player, data.get_rebounds()[self.curr_i[i]])

    def add_points(self):
        p = self.solver.Constraint(108.8, math.inf)
        for i, player in enumerate(self.player_vars):
            p.SetCoefficient(player, data.get_points()[self.curr_i[i]])

    def add_threes(self):
        t = self.solver.Constraint(30, math.inf)
        for i, player in enumerate(self.player_vars):
            t.SetCoefficient(player, data.get_three_attempts()[self.curr_i[i]])

    def add_fg_attempts(self):
        fga = self.solver.Constraint(0, 88)
        for i, player in enumerate(self.player_vars):
            fga.SetCoefficient(player, data.get_fg_attempted()[self.curr_i[i]])

    def add_turnovers(self):
        to = self.solver.Constraint(0, 13.2)
        for i, player in enumerate(self.player_vars):
            to.SetCoefficient(player, data.get_turnovers()[self.curr_i[i]])

    def add_assists(self):
        a = self.solver.Constraint(24.2, math.inf)
        for i, player in enumerate(self.player_vars):
            a.SetCoefficient(player, data.get_assists()[self.curr_i[i]])

    def add_objective(self):
        self.minutes_played()
        objective = self.solver.Objective()
        for i, player in enumerate(self.player_vars):
            objective.SetCoefficient(player, (data.get_points()[self.curr_i[i]]))
        objective.SetMaximization()

    def get_optimal_team(self, s):
        self.solver = pywraplp.Solver.CreateSolver("GLOP")
        if not self.solver:
            return
        self.player_vars = [self.solver.NumVar(0.01, 1.0, str(i)) for i in s]
        self.add_points()
        self.add_rebounds()
        self.add_assists()
        self.add_fg_attempts()
        self.add_objective()
        self.add_turnovers()
        self.add_threes()
        status = self.solver.Solve()
        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            if self.solver.Objective().Value() > self.max:
                print(f"\nmax of obj function: {self.solver.Objective().Value()}\n")
                self.max = self.solver.Objective().Value()
                r = []
                p = []
                to = []
                fga = []
                a = []
                t = []
                for i, player in enumerate(self.player_vars):
                    if player.solution_value() > 0:
                        print(f"{player}: {math.floor(data.get_minutes_played()[self.curr_i[i]] * player.solution_value())} mins")
                        r.append(player.solution_value() * data.get_rebounds()[self.curr_i[i]])
                        p.append(player.solution_value() * data.get_points()[self.curr_i[i]])
                        to.append(player.solution_value() * data.get_turnovers()[self.curr_i[i]])
                        fga.append(player.solution_value() * data.get_fg_attempted()[self.curr_i[i]])
                        a.append(player.solution_value() * data.get_assists()[self.curr_i[i]])
                        t.append(player.solution_value() * data.get_three_attempts()[self.curr_i[i]])

                print('\npoints: ', round(sum(p)))
                print('rebounds', round(sum(r)))
                print('turnovers', round(sum(to)))
                print('attempted', round(sum(fga)))
                print('assists', round(sum(a)))
                print('threes', round(sum(t)))


if __name__ == "__main__":
    cd = cd.cd()
    data = data.data()
    # get_champ_avg()
    m = mc.cp()
    o = Optimizer()
